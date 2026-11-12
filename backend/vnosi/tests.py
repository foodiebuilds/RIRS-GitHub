from datetime import datetime, time, timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from dostop.models import Dostop
from treningi.models import Trening
from uporabniki.models import Uporabnik

from .models import DnevniCilj, Komentar, Vnos, cilj_za_dan


def uporabnik(ime):
    return Uporabnik.objects.create_user(ime, f"{ime}@primer.si", "Geslo-12345", ime=ime.capitalize())


class VodaInObrokiTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)

    def test_us04_ac1_gumb_doda_250_ml_vode(self):
        self.assertRedirects(self.client.post("/prehrana/voda/"), "/prehrana/")
        self.client.post("/prehrana/voda/")
        self.assertEqual(list(Vnos.objects.values_list("tip", "kolicina")), [("VODA", 250), ("VODA", 250)])
        self.assertContains(self.client.get("/prehrana/"), "voda 250 ml", count=2)

    def test_us04_ac2_obrok_z_opisom_in_kalorijami(self):
        odgovor = self.client.post("/prehrana/", {"opis": "piščanec z rižem in solata", "kcal": 650})
        self.assertRedirects(odgovor, "/prehrana/")
        v = Vnos.objects.get()
        self.assertEqual((v.uporabnik, v.tip, v.kolicina, v.opis), (self.ana, "OBROK", 650, "piščanec z rižem in solata"))
        self.assertContains(self.client.get("/prehrana/"), "piščanec z rižem in solata, 650 kcal")

    def test_us04_ac2_obrok_zahteva_opis_in_kalorije(self):
        self.client.post("/prehrana/", {"opis": "", "kcal": 650})
        self.client.post("/prehrana/", {"opis": "jabolko", "kcal": ""})
        self.assertFalse(Vnos.objects.exists())

    def test_vsak_vidi_samo_svoje_vnose(self):
        self.client.post("/prehrana/voda/")
        self.client.force_login(uporabnik("tomaz"))
        self.assertNotContains(self.client.get("/prehrana/"), "voda 250 ml")


class DnevniCiljTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)

    def test_us04_ac3_cilj_velja_od_danes(self):
        self.assertRedirects(self.client.post("/prehrana/cilj/", {"kcal": 2200, "voda_ml": 2500}), "/prehrana/")
        self.client.post("/prehrana/cilj/", {"kcal": 3000000000, "voda_ml": 2500})  # prevelika številka se ne shrani
        c = DnevniCilj.objects.get()
        self.assertEqual((c.sportnik, c.avtor, c.kcal, c.voda_ml), (self.ana, self.ana, 2200, 2500))
        self.assertEqual((c.velja_od, c.status), (timezone.localdate(), "AKTIVEN"))
        self.assertContains(self.client.get("/prehrana/"), "2200 kcal, 2500 ml vode")

    def test_us04_ac3_nov_cilj_zamenja_starega_ki_ostane_shranjen(self):
        vceraj = timezone.localdate() - timedelta(days=1)
        star = DnevniCilj.objects.create(
            sportnik=self.ana, avtor=self.ana, kcal=2000, voda_ml=2000, velja_od=vceraj, status="AKTIVEN"
        )
        self.client.post("/prehrana/cilj/", {"kcal": 2200, "voda_ml": 2500})
        star.refresh_from_db()
        self.assertEqual(star.status, "ZAMENJAN")
        self.assertEqual(cilj_za_dan(self.ana, vceraj), star)
        self.assertEqual(cilj_za_dan(self.ana, timezone.localdate()).kcal, 2200)

    def test_brez_cilja(self):
        self.assertIsNone(cilj_za_dan(self.ana, timezone.localdate()))
        self.assertContains(self.client.get("/prehrana/"), "Cilj še ni nastavljen.")


class NapredekDoCiljaTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        self.danes = timezone.localdate()

    def cilj(self, dan, kcal, voda_ml, status="AKTIVEN"):
        DnevniCilj.objects.create(
            sportnik=self.ana, avtor=self.ana, kcal=kcal, voda_ml=voda_ml, velja_od=dan, status=status
        )

    def vnos(self, tip, kolicina, dan):
        cas = timezone.make_aware(datetime.combine(dan, time(12, 0)))
        Vnos.objects.create(uporabnik=self.ana, tip=tip, kolicina=kolicina, cas=cas)

    def test_us04_ac4_danes_vneseno_in_manjka(self):
        self.cilj(self.danes, 2200, 2500)
        for _ in range(6):
            self.client.post("/prehrana/voda/")
        self.client.post("/prehrana/", {"opis": "kosilo", "kcal": 1200})
        odgovor = self.client.get("/prehrana/")
        self.assertContains(odgovor, "1,5 l od 2,5 l, manjka 1 l")
        self.assertContains(odgovor, "1200 kcal od 2200 kcal, manjka 1000 kcal")

    def test_us04_ac5_pretekli_dan_s_ciljem_ki_je_takrat_veljal(self):
        vceraj = self.danes - timedelta(days=1)
        self.cilj(vceraj - timedelta(days=5), 2000, 2000, status="ZAMENJAN")
        self.cilj(self.danes, 2200, 2500)
        self.vnos("VODA", 1500, vceraj)
        vceraj_pregled = self.client.get("/prehrana/").context["pretekli_dnevi"][0]
        self.assertEqual(vceraj_pregled["dan"], vceraj)
        self.assertEqual(vceraj_pregled["voda"], "1,5 l od 2 l, manjka 0,5 l")

    def test_vnos_po_polnoci_sodi_v_nov_dan(self):
        # 00:30 po lokalnem času (Europe/Ljubljana) je v UTC še prejšnji dan.
        cas = timezone.make_aware(datetime.combine(self.danes, time(0, 30)))
        Vnos.objects.create(uporabnik=self.ana, tip="VODA", kolicina=250, cas=cas)
        self.assertContains(self.client.get("/prehrana/"), "Voda: 0,25 l (cilj ni nastavljen)")


class StranPrehranaTest(TestCase):
    def test_meni_in_naslov_prehrana_kot_na_wireframih(self):
        self.client.force_login(uporabnik("ana"))
        odgovor = self.client.get("/prehrana/")
        self.assertContains(odgovor, "<title>Prehrana</title>", html=True)
        self.assertContains(odgovor, '<a href="/prehrana/">Prehrana</a>', html=True)


class PrehranaZaSvetovalcaTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.sara = uporabnik("sara")
        self.danes = timezone.localdate()
        DnevniCilj.objects.create(
            sportnik=self.ana, avtor=self.ana, kcal=2200, voda_ml=2500, velja_od=self.danes, status="AKTIVEN"
        )
        Vnos.objects.create(uporabnik=self.ana, tip="VODA", kolicina=1500)
        self.client.force_login(self.sara)

    def dostop(self, vrsta):
        Dostop.objects.create(sportnik=self.ana, strokovnjak=self.sara, vrsta=vrsta, status="AKTIVEN")

    def test_us05_ac4_svetovalec_vidi_cilj_in_napredek(self):
        self.dostop("PREHRANSKI_SVETOVALEC")
        odgovor = self.client.get(f"/prehrana/{self.ana.pk}/")
        self.assertContains(odgovor, "1,5 l od 2,5 l, manjka 1 l")
        self.assertContains(odgovor, "2200 kcal, 2500 ml vode")
        self.assertNotContains(odgovor, "Nastavi cilj od danes")  # samo branje
        self.assertNotContains(odgovor, "+250 ml")
        self.assertContains(self.client.get("/moji-sportniki/"), f'href="/prehrana/{self.ana.pk}/"')

    def test_us05_ac4_trener_in_brez_dostopa_ne_vidita(self):
        self.assertEqual(self.client.get(f"/prehrana/{self.ana.pk}/").status_code, 404)
        self.dostop("TRENER")
        self.assertEqual(self.client.get(f"/prehrana/{self.ana.pk}/").status_code, 404)
        self.assertNotContains(self.client.get("/moji-sportniki/"), f'href="/prehrana/{self.ana.pk}/"')


class PocutjeInTezaTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)

    def test_us07_ac1_pocutje_za_del_dneva(self):
        self.assertRedirects(self.client.post("/casovnica/pocutje/", {"ocena": "4"}), "/casovnica/")
        v = Vnos.objects.get()
        self.assertEqual((v.uporabnik, v.tip, v.kolicina, v.trening), (self.ana, "POCUTJE", 4, None))

    def test_us07_ac1_pocutje_za_trening(self):
        t = Trening.objects.create(uporabnik=self.ana, trajanje_min=60, porabljene_kcal=400)
        self.client.post("/casovnica/pocutje/", {"ocena": "5", "trening": t.pk})
        self.assertEqual(Vnos.objects.get().trening, t)

    def test_us07_ac1_ocena_od_1_do_5_in_samo_svoj_trening(self):
        tuj = Trening.objects.create(uporabnik=uporabnik("tomaz"), trajanje_min=60, porabljene_kcal=400)
        self.client.post("/casovnica/pocutje/", {"ocena": "6"})
        self.client.post("/casovnica/pocutje/", {"ocena": "0"})
        self.client.post("/casovnica/pocutje/", {"ocena": "3", "trening": tuj.pk})
        self.assertFalse(Vnos.objects.exists())

    def test_us07_ac1_teza_v_kg(self):
        self.client.post("/casovnica/teza/", {"teza_kg": "78.5"})
        v = Vnos.objects.get()
        self.assertEqual((v.tip, v.kolicina), ("TEZA", 78.5))
        self.assertContains(self.client.get("/casovnica/"), "teža 78,5 kg")


def ob(dan, ura, minuta=0):
    return timezone.make_aware(datetime.combine(dan, time(ura, minuta)))


class CasovnicaTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        self.danes = timezone.localdate()
        self.vceraj = self.danes - timedelta(days=1)
        Trening.objects.create(uporabnik=self.ana, zacetek=ob(self.danes, 18), trajanje_min=60, porabljene_kcal=400)
        Vnos.objects.create(uporabnik=self.ana, tip="VODA", kolicina=250, cas=ob(self.danes, 9))
        Vnos.objects.create(uporabnik=self.ana, tip="OBROK", kolicina=650, opis="kosilo", cas=ob(self.danes, 13))
        Vnos.objects.create(uporabnik=self.ana, tip="POCUTJE", kolicina=4, cas=ob(self.vceraj, 20))
        Vnos.objects.create(uporabnik=self.ana, tip="TEZA", kolicina=78, cas=ob(self.vceraj, 7))

    def test_us07_ac2_vsi_vnosi_po_dnevih_znotraj_dneva_po_casu(self):
        dnevi = self.client.get("/casovnica/").context["dnevi"]
        self.assertEqual([dan for dan, _ in dnevi], [self.danes, self.vceraj])
        danes = [p.get("vnos", p.get("trening")) for p in dnevi[0][1]]
        self.assertEqual([getattr(x, "tip", "TRENING") for x in danes], ["VODA", "OBROK", "TRENING"])
        self.assertEqual([p["vnos"].tip for p in dnevi[1][1]], ["TEZA", "POCUTJE"])

    def test_us07_ac2_prikaz(self):
        odgovor = self.client.get("/casovnica/")
        for besedilo in ["voda 250 ml", "obrok: kosilo, 650 kcal", "trening 60 min · 400 kcal", "počutje 4/5", "teža 78 kg"]:
            self.assertContains(odgovor, besedilo)

    def test_samo_svoji_vnosi(self):
        self.client.force_login(uporabnik("tomaz"))
        self.assertEqual(self.client.get("/casovnica/").context["dnevi"], [])


class CasovnicaZaStrokovnjakaTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.tomaz = uporabnik("tomaz")
        danes = timezone.localdate()
        self.trening = Trening.objects.create(uporabnik=self.ana, zacetek=ob(danes, 18), trajanje_min=60, porabljene_kcal=400)
        for tip, kolicina in [("VODA", 250), ("OBROK", 650), ("POCUTJE", 4), ("TEZA", 78)]:
            Vnos.objects.create(uporabnik=self.ana, tip=tip, kolicina=kolicina, opis="kosilo" if tip == "OBROK" else "")
        self.client.force_login(self.tomaz)

    def dostop(self, vrsta, status="AKTIVEN"):
        Dostop.objects.create(sportnik=self.ana, strokovnjak=self.tomaz, vrsta=vrsta, status=status)

    def vidno(self):
        odgovor = self.client.get(f"/casovnica/{self.ana.pk}/")
        self.assertEqual(odgovor.status_code, 200)
        postavke = [p for _, dan in odgovor.context["dnevi"] for p in dan]
        return {("TRENING-kcal" if p["samo_kcal"] else "TRENING") if "trening" in p else p["vnos"].tip for p in postavke}

    def test_us07_ac3_trener_vidi_treninge_pocutje_in_tezo(self):
        self.dostop("TRENER")
        self.assertEqual(self.vidno(), {"TRENING", "POCUTJE", "TEZA"})

    def test_us07_ac3_svetovalec_vidi_vodo_obroke_pocutje_tezo_in_kcal_treningov(self):
        self.dostop("PREHRANSKI_SVETOVALEC")
        self.assertEqual(self.vidno(), {"TRENING-kcal", "VODA", "OBROK", "POCUTJE", "TEZA"})
        odgovor = self.client.get(f"/casovnica/{self.ana.pk}/")
        self.assertContains(odgovor, "porabljene kalorije: 400 kcal")
        self.assertNotContains(odgovor, "60 min")

    def test_brez_aktivnega_dostopa_404(self):
        self.assertEqual(self.client.get(f"/casovnica/{self.ana.pk}/").status_code, 404)
        self.dostop("TRENER", status="POVABLJEN")
        self.assertEqual(self.client.get(f"/casovnica/{self.ana.pk}/").status_code, 404)

    def test_strokovnjak_ne_vidi_obrazcev_za_vnos(self):
        self.dostop("TRENER")
        self.assertNotContains(self.client.get(f"/casovnica/{self.ana.pk}/"), "Zabeleži počutje")

    def test_povezava_s_seznama_moji_sportniki(self):
        self.dostop("TRENER")
        self.assertContains(self.client.get("/moji-sportniki/"), f'href="/casovnica/{self.ana.pk}/"')


class KomentarjiTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.trener = uporabnik("tomaz")
        self.svetovalec = uporabnik("sara")
        Dostop.objects.create(sportnik=self.ana, strokovnjak=self.trener, vrsta="TRENER", status="AKTIVEN")
        Dostop.objects.create(
            sportnik=self.ana, strokovnjak=self.svetovalec, vrsta="PREHRANSKI_SVETOVALEC", status="AKTIVEN"
        )
        self.trening = Trening.objects.create(uporabnik=self.ana, trajanje_min=60, porabljene_kcal=400)
        self.obrok = Vnos.objects.create(uporabnik=self.ana, tip="OBROK", kolicina=650, opis="kosilo")
        self.url = f"/casovnica/{self.ana.pk}/komentar/"

    def komentiraj(self, kdo, besedilo, **postavka):
        self.client.force_login(kdo)
        return self.client.post(self.url, {"besedilo": besedilo, **postavka})

    def test_us07_ac4_trener_komentira_trening(self):
        odgovor = self.komentiraj(self.trener, "Povečaj težo pri počepu.", trening=self.trening.pk)
        self.assertRedirects(odgovor, f"/casovnica/{self.ana.pk}/")
        k = Komentar.objects.get()
        self.assertEqual((k.avtor, k.sportnik, k.trening, k.vnos), (self.trener, self.ana, self.trening, None))

    def test_us07_ac4_komentar_z_avtorjem_vidi_vsak_ki_vidi_vnos(self):
        self.komentiraj(self.trener, "Povečaj težo pri počepu.", trening=self.trening.pk)
        self.komentiraj(self.svetovalec, "Dodaj zelenjavo.", vnos=self.obrok.pk)
        for gledalec, url in [(self.ana, "/casovnica/"), (self.svetovalec, f"/casovnica/{self.ana.pk}/")]:
            self.client.force_login(gledalec)
            odgovor = self.client.get(url)
            self.assertContains(odgovor, "Tomaz, ")  # avtor in čas
            self.assertContains(odgovor, "Povečaj težo pri počepu.")
        self.client.force_login(self.trener)
        self.assertNotContains(self.client.get(f"/casovnica/{self.ana.pk}/"), "Dodaj zelenjavo.")  # obroka ne vidi

    def test_us07_ac4_samo_vnosi_ki_jih_vidi(self):
        self.assertEqual(self.komentiraj(self.trener, "x", vnos=self.obrok.pk).status_code, 404)
        self.assertEqual(self.komentiraj(uporabnik("tujec"), "x", trening=self.trening.pk).status_code, 404)
        tuj = Trening.objects.create(uporabnik=uporabnik("bor"), trajanje_min=30, porabljene_kcal=200)
        self.assertEqual(self.komentiraj(self.trener, "x", trening=tuj.pk).status_code, 404)  # trening drugega športnika
        self.assertFalse(Komentar.objects.exists())

    def test_us07_ac5_sportnik_ne_komentira_in_ne_spreminja(self):
        self.assertEqual(self.komentiraj(self.ana, "x", trening=self.trening.pk).status_code, 404)
        self.komentiraj(self.trener, "Povečaj težo.", trening=self.trening.pk)
        self.client.force_login(self.ana)
        self.assertNotContains(self.client.get("/casovnica/"), "Komentiraj")

    def test_komentar_na_trening_ali_vnos_ne_oboje(self):
        with self.assertRaises(IntegrityError):
            Komentar.objects.create(
                avtor=self.trener, sportnik=self.ana, trening=self.trening, vnos=self.obrok, besedilo="x"
            )
