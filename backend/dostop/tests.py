from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Dostop
from .pravice import VSI_PODATKI, vidni_podatki


def uporabnik(ime):
    return Uporabnik.objects.create_user(ime, f"{ime}@primer.si", "Geslo-12345", ime=ime.capitalize())


class PovabiloTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.tomaz = uporabnik("tomaz")
        self.client.force_login(self.ana)

    def povabi(self, ime, vrsta):
        return self.client.post("/dostop/", {"uporabnisko_ime": ime, "vrsta": vrsta})

    def test_us05_ac1_povabilo_trenerja(self):
        self.assertRedirects(self.povabi("tomaz", "TRENER"), "/dostop/")
        d = Dostop.objects.get()
        self.assertEqual((d.sportnik, d.strokovnjak, d.vrsta, d.status), (self.ana, self.tomaz, "TRENER", "POVABLJEN"))

    def test_us05_ac1_povabilo_za_oboje_ustvari_dve_vrstici(self):
        self.povabi("tomaz", "OBOJE")
        self.assertEqual(
            sorted(Dostop.objects.values_list("vrsta", flat=True)), ["PREHRANSKI_SVETOVALEC", "TRENER"]
        )

    def test_us05_ac1_neobstojec_uporabnik(self):
        odgovor = self.povabi("nihce", "TRENER")
        self.assertContains(odgovor, "Uporabnik s tem uporabniškim imenom ne obstaja.")
        self.assertFalse(Dostop.objects.exists())

    def test_povabilo_sebe_in_dvojno_povabilo_nista_mogoca(self):
        self.assertContains(self.povabi("ana", "TRENER"), "Sebe ne moreš povabiti.")
        self.povabi("tomaz", "TRENER")
        self.assertContains(self.povabi("tomaz", "OBOJE"), "že povabljen ali ima dostop")
        self.assertEqual(Dostop.objects.count(), 1)

    def test_seznam_dostopov_vidi_samo_sportnik(self):
        self.povabi("tomaz", "TRENER")
        self.assertContains(self.client.get("/dostop/"), "Tomaz (tomaz)")
        self.client.force_login(self.tomaz)
        self.assertNotContains(self.client.get("/dostop/"), "Tomaz (tomaz)")


class SprejemInPreklicTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.tomaz = uporabnik("tomaz")
        self.trener = Dostop.objects.create(sportnik=self.ana, strokovnjak=self.tomaz, vrsta="TRENER")
        self.svetovalec = Dostop.objects.create(
            sportnik=self.ana, strokovnjak=self.tomaz, vrsta="PREHRANSKI_SVETOVALEC"
        )

    def stanje(self, dostop):
        dostop.refresh_from_db()
        return dostop.status

    def moji_sportniki(self):
        self.client.force_login(self.tomaz)
        return self.client.get("/moji-sportniki/")

    def test_us05_ac2_dokler_ni_sprejeto_ni_na_seznamu(self):
        odgovor = self.moji_sportniki()
        self.assertEqual(list(odgovor.context["povabila"]), [self.trener, self.svetovalec])
        self.assertEqual(list(odgovor.context["aktivni"]), [])

    def test_us05_ac2_zavrnitev(self):
        self.client.force_login(self.tomaz)
        self.client.post(f"/moji-sportniki/povabilo/{self.trener.pk}/zavrni/")
        self.assertEqual(self.stanje(self.trener), "PREKLICAN")

    def test_us05_ac3_po_sprejemu_na_seznamu_moji_sportniki(self):
        self.client.force_login(self.tomaz)
        for d in (self.trener, self.svetovalec):
            self.client.post(f"/moji-sportniki/povabilo/{d.pk}/sprejmi/")
            self.assertEqual(self.stanje(d), "AKTIVEN")
        odgovor = self.moji_sportniki()
        self.assertContains(odgovor, "Ana (ana)")
        self.assertContains(odgovor, "prehranski svetovalec, trener")

    def test_us05_ac5_po_preklicu_ni_vec_na_seznamu(self):
        Dostop.objects.update(status="AKTIVEN")
        self.client.force_login(self.ana)
        for d in (self.trener, self.svetovalec):
            self.assertRedirects(self.client.post(f"/dostop/{d.pk}/preklici/"), "/dostop/")
            self.assertEqual(self.stanje(d), "PREKLICAN")
        self.assertNotContains(self.moji_sportniki(), "Ana (ana)")

    def test_samo_povabljeni_odgovori_in_samo_sportnik_preklice(self):
        tujec = uporabnik("tujec")
        self.client.force_login(tujec)
        self.assertEqual(self.client.post(f"/moji-sportniki/povabilo/{self.trener.pk}/sprejmi/").status_code, 404)
        self.assertEqual(self.client.post(f"/dostop/{self.trener.pk}/preklici/").status_code, 404)
        self.client.force_login(self.tomaz)
        self.assertEqual(self.client.post(f"/dostop/{self.trener.pk}/preklici/").status_code, 404)
        self.assertEqual(self.stanje(self.trener), "POVABLJEN")

    def test_neznan_odgovor_na_povabilo_ne_spremeni_nicesar(self):
        self.client.force_login(self.tomaz)
        self.assertEqual(self.client.post(f"/moji-sportniki/povabilo/{self.trener.pk}/xyz/").status_code, 404)
        self.assertEqual(self.stanje(self.trener), "POVABLJEN")

    def test_po_preklicu_lahko_znova_povabi(self):
        self.trener.status = "PREKLICAN"
        self.trener.save()
        self.client.force_login(self.ana)
        odgovor = self.client.post("/dostop/", {"uporabnisko_ime": "tomaz", "vrsta": "TRENER"})
        self.assertRedirects(odgovor, "/dostop/")
        self.assertEqual(Dostop.objects.filter(vrsta="TRENER", status="POVABLJEN").count(), 1)


class PraviceTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.tomaz = uporabnik("tomaz")

    def dostop(self, vrsta, status="AKTIVEN"):
        return Dostop.objects.create(sportnik=self.ana, strokovnjak=self.tomaz, vrsta=vrsta, status=status)

    def test_lastnik_vidi_vse(self):
        self.assertEqual(vidni_podatki(self.ana, self.ana), VSI_PODATKI)

    def test_us05_ac4_trener(self):
        self.dostop("TRENER")
        self.assertEqual(vidni_podatki(self.tomaz, self.ana), {"treningi", "plani", "pocutje", "teza"})

    def test_us05_ac4_prehranski_svetovalec(self):
        self.dostop("PREHRANSKI_SVETOVALEC")
        self.assertEqual(
            vidni_podatki(self.tomaz, self.ana), {"voda", "obroki", "kcal_treningov", "cilji", "pocutje", "teza"}
        )

    def test_us05_ac4_trener_in_svetovalec(self):
        self.dostop("TRENER")
        self.dostop("PREHRANSKI_SVETOVALEC")
        self.assertEqual(vidni_podatki(self.tomaz, self.ana), VSI_PODATKI)

    def test_us05_ac2_pred_sprejemom_nic(self):
        self.dostop("TRENER", status="POVABLJEN")
        self.assertEqual(vidni_podatki(self.tomaz, self.ana), set())

    def test_us05_ac5_po_preklicu_nic(self):
        self.dostop("TRENER", status="PREKLICAN")
        self.assertEqual(vidni_podatki(self.tomaz, self.ana), set())

    def test_brez_dostopa_nic_in_dostop_ne_velja_obratno(self):
        self.dostop("TRENER")
        self.assertEqual(vidni_podatki(uporabnik("tujec"), self.ana), set())
        self.assertEqual(vidni_podatki(self.ana, self.tomaz), set())
