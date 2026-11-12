import re
from datetime import datetime, time, timedelta

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from dostop.models import Dostop
from uporabniki.models import Uporabnik

from .models import Misica, Serija, Trening, Vaja, VajaMisica
from .zemljevid import obremenitev_misic


def uporabnik(ime):
    return Uporabnik.objects.create_user(ime, f"{ime}@primer.si", "Geslo-12345", ime=ime.capitalize())


class ZacetniPodatkiTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def test_vaje_in_misice_so_nalozene(self):
        self.assertEqual(Misica.objects.count(), 15)
        for ime in ["Počep", "Izpadni korak", "Meča stoje", "Dvig bokov"]:  # vaje z wireframa W1
            self.assertTrue(Vaja.objects.filter(ime=ime).exists(), ime)

    def test_vsaka_vaja_ima_glavno_misico(self):
        for vaja in Vaja.objects.all():
            self.assertTrue(VajaMisica.objects.filter(vaja=vaja, tip="GLAVNA").exists(), vaja.ime)

    def test_vsaka_misica_je_v_vsaj_eni_vaji(self):
        for misica in Misica.objects.all():
            self.assertTrue(VajaMisica.objects.filter(misica=misica).exists(), misica.ime)

    def test_us02_ac5_vaje_ureja_samo_administrator(self):
        self.client.force_login(uporabnik("ana"))
        self.assertEqual(self.client.get("/admin/treningi/vaja/add/").status_code, 302)
        admin = Uporabnik.objects.create_superuser("admin", "admin@primer.si", "Geslo-12345", ime="Admin")
        self.client.force_login(admin)
        self.assertEqual(self.client.get("/admin/treningi/vaja/add/").status_code, 200)
        self.assertEqual(self.client.get("/admin/treningi/vaja/1/change/").status_code, 200)


def podatki_treninga(serije, trajanje="60", kcal="420"):
    """POST podatki za stran Treningi: serije = [(vaja_id, ponovitve, teza), ...]."""
    podatki = {
        "trajanje_min": trajanje,
        "porabljene_kcal": kcal,
        "serije-TOTAL_FORMS": "9",
        "serije-INITIAL_FORMS": "0",
        "serije-MIN_NUM_FORMS": "1",
        "serije-MAX_NUM_FORMS": "1000",
    }
    for i, (vaja, ponovitve, teza) in enumerate(serije):
        podatki.update({f"serije-{i}-vaja": vaja, f"serije-{i}-ponovitve": ponovitve, f"serije-{i}-teza_kg": teza})
    return podatki


class VnosTreningaTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        self.pocep = Vaja.objects.get(ime="Počep")
        self.dvig = Vaja.objects.get(ime="Dvig bokov")

    def test_us02_ac1_ac2_trening_z_vajami_serijami_trajanjem_in_kcal(self):
        serije = [(self.pocep.pk, "8", "80"), (self.pocep.pk, "8", "80"), (self.dvig.pk, "10", "60.5")]
        odgovor = self.client.post("/treningi/", podatki_treninga(serije))
        self.assertRedirects(odgovor, "/treningi/")
        t = Trening.objects.get()
        self.assertEqual((t.uporabnik, t.trajanje_min, t.porabljene_kcal), (self.ana, 60, 420))
        self.assertEqual(
            list(t.serije.values_list("zaporedna_st", "vaja__ime", "ponovitve", "teza_kg")),
            [(1, "Počep", 8, 80.0), (2, "Počep", 8, 80.0), (3, "Dvig bokov", 10, 60.5)],
        )

    def test_us02_ac1_vsaj_ena_serija_in_pravilne_vrednosti(self):
        self.client.post("/treningi/", podatki_treninga([]))
        self.client.post("/treningi/", podatki_treninga([(self.pocep.pk, "0", "80")]))
        self.client.post("/treningi/", podatki_treninga([(self.pocep.pk, "3000000000", "80")]))
        self.client.post("/treningi/", podatki_treninga([(self.pocep.pk, "8", "80")], trajanje="3000000000"))
        self.client.post("/treningi/", podatki_treninga([(self.pocep.pk, "8", "80")], trajanje=""))
        self.assertFalse(Trening.objects.exists())

    def test_us02_ac5_samo_vaje_s_seznama(self):
        self.client.post("/treningi/", podatki_treninga([(9999, "8", "80")]))
        self.assertFalse(Trening.objects.exists())


class PretekliTreningiTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        self.pocep = Vaja.objects.get(ime="Počep")

    def test_us02_ac4_shranjen_trening_je_na_seznamu(self):
        serije = [(self.pocep.pk, "8", "80"), (self.pocep.pk, "8", "82.5")]
        self.client.post("/treningi/", podatki_treninga(serije, trajanje="55", kcal="380"))
        odgovor = self.client.get("/treningi/")
        self.assertContains(odgovor, "55 min · 380 kcal")
        self.assertContains(odgovor, "Počep: 8 × 80 kg, 8 × 82,5 kg")

    def test_novejsi_najprej_in_samo_svoji(self):
        prvi = Trening.objects.create(uporabnik=self.ana, trajanje_min=40, porabljene_kcal=300)
        drugi = Trening.objects.create(uporabnik=self.ana, trajanje_min=50, porabljene_kcal=350)
        Trening.objects.create(uporabnik=uporabnik("tomaz"), trajanje_min=99, porabljene_kcal=999)
        self.assertEqual(list(self.client.get("/treningi/").context["pretekli"]), [drugi, prvi])


class KopirajTreningTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        pocep = Vaja.objects.get(ime="Počep")
        self.dvig = Vaja.objects.get(ime="Dvig bokov")
        self.vzor = Trening.objects.create(uporabnik=self.ana, trajanje_min=55, porabljene_kcal=380)
        for st, (vaja, ponovitve, teza) in enumerate([(pocep, 8, 80), (pocep, 8, 80), (self.dvig, 10, 60)], 1):
            Serija.objects.create(trening=self.vzor, vaja=vaja, zaporedna_st=st, ponovitve=ponovitve, teza_kg=teza)

    def test_us02_ac3_gumb_pri_vsakem_preteklem_treningu(self):
        drugi = Trening.objects.create(uporabnik=self.ana, trajanje_min=30, porabljene_kcal=200)
        odgovor = self.client.get("/treningi/")
        for t in (self.vzor, drugi):
            self.assertContains(odgovor, f'action="/treningi/kopiraj/{t.pk}/"')

    def test_us02_ac3_obrazec_je_izpolnjen_s_kopijo(self):
        odgovor = self.client.get(f"/treningi/kopiraj/{self.vzor.pk}/")
        formset = odgovor.context["serije_formset"]
        self.assertEqual(
            [(f.initial["vaja"], f.initial["ponovitve"], f.initial["teza_kg"]) for f in formset.initial_forms],
            [(s.vaja_id, s.ponovitve, s.teza_kg) for s in self.vzor.serije.all()],
        )
        self.assertEqual(odgovor.context["trening_form"].initial["trajanje_min"], 55)
        self.assertEqual(Trening.objects.count(), 1)  # nov trening nastane šele ob shranjevanju

    def test_us02_ac3_popravljene_stevilke_in_odstranjena_serija(self):
        podatki = podatki_treninga([], trajanje="60", kcal="400")
        podatki["serije-INITIAL_FORMS"] = "3"
        for i, s in enumerate(self.vzor.serije.all()):
            podatki.update({f"serije-{i}-vaja": s.vaja_id, f"serije-{i}-ponovitve": s.ponovitve, f"serije-{i}-teza_kg": s.teza_kg})
        podatki["serije-1-teza_kg"] = "85"  # popravljena teža
        podatki["serije-2-DELETE"] = "on"  # odstranjena serija
        self.assertRedirects(self.client.post(f"/treningi/kopiraj/{self.vzor.pk}/", podatki), "/treningi/")
        nov = Trening.objects.exclude(pk=self.vzor.pk).get()
        self.assertEqual((nov.trajanje_min, nov.porabljene_kcal), (60, 400))
        self.assertEqual(list(nov.serije.values_list("ponovitve", "teza_kg")), [(8, 80.0), (8, 85.0)])
        self.assertEqual(self.vzor.serije.count(), 3)  # vzor ostane nespremenjen

    def test_tujega_treninga_ni_mogoce_kopirati(self):
        self.client.force_login(uporabnik("tomaz"))
        self.assertEqual(self.client.get(f"/treningi/kopiraj/{self.vzor.pk}/").status_code, 404)


class ObremenitevMisicTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.prsa = Misica.objects.create(ime="prsa", pogled="SPREDAJ")
        self.triceps = Misica.objects.create(ime="triceps", pogled="ZADAJ")
        self.meca = Misica.objects.create(ime="meča", pogled="ZADAJ")
        self.potisk = Vaja.objects.create(ime="Potisk s prsi na klopi")
        VajaMisica.objects.create(vaja=self.potisk, misica=self.prsa, tip="GLAVNA")
        VajaMisica.objects.create(vaja=self.potisk, misica=self.triceps, tip="POMOZNA")
        self.danes = timezone.localdate()

    def trening(self, vaja, st_serij, dan=None, kdo=None):
        zacetek = timezone.make_aware(datetime.combine(dan or self.danes, time(10, 0)))
        t = Trening.objects.create(uporabnik=kdo or self.ana, zacetek=zacetek, trajanje_min=60, porabljene_kcal=400)
        for st in range(1, st_serij + 1):
            Serija.objects.create(trening=t, vaja=vaja, zaporedna_st=st, ponovitve=8, teza_kg=60)

    def obremenitev(self, od=None, do=None):
        return obremenitev_misic(self.ana, od or self.danes - timedelta(days=6), do or self.danes)

    def test_us03_ac2_primer_iz_zgodbe(self):
        # 12 serij potiska: prsa 12 točk -> 10, triceps 6 točk -> 5
        self.trening(self.potisk, 12)
        o = self.obremenitev()
        self.assertEqual((o[self.prsa], o[self.triceps]), (10, 5))

    def test_us03_ac3_netrenirana_0_trenirana_vsaj_1(self):
        meca_stoje = Vaja.objects.create(ime="Meča stoje")
        VajaMisica.objects.create(vaja=meca_stoje, misica=self.meca, tip="POMOZNA")
        self.trening(self.potisk, 30)
        o = self.obremenitev()
        self.assertEqual(o[self.meca], 0)
        self.trening(meca_stoje, 1)  # 0,5 točke od 30 -> zaokroženo 0, a najmanj 1
        self.assertEqual(self.obremenitev()[self.meca], 1)

    def test_us03_ac4_samo_izbrano_obdobje_in_samo_svoji_treningi(self):
        self.trening(self.potisk, 3, dan=self.danes - timedelta(days=7))  # izven zadnjih 7 dni
        self.trening(self.potisk, 3, kdo=uporabnik("tomaz"))
        self.assertEqual(self.obremenitev()[self.prsa], 0)
        self.assertEqual(self.obremenitev(od=self.danes - timedelta(days=29))[self.prsa], 10)

    def test_us03_ac5_brez_treningov_vse_0(self):
        self.assertEqual(set(self.obremenitev().values()), {0})

    def test_sprememba_misic_vaje_velja_tudi_za_pretekle_treninge(self):
        self.trening(self.potisk, 2)
        VajaMisica.objects.filter(misica=self.triceps).update(tip="GLAVNA")
        self.assertEqual(self.obremenitev()[self.triceps], 10)


class ZemljevidMisicStranTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)
        self.danes = timezone.localdate()

    def trening(self, ime_vaje, st_serij, dan):
        zacetek = timezone.make_aware(datetime.combine(dan, time(10, 0)))
        t = Trening.objects.create(uporabnik=self.ana, zacetek=zacetek, trajanje_min=60, porabljene_kcal=400)
        vaja = Vaja.objects.get(ime=ime_vaje)
        for st in range(1, st_serij + 1):
            Serija.objects.create(trening=t, vaja=vaja, zaporedna_st=st, ponovitve=8, teza_kg=60)

    def test_oznake_misic_obstajajo_v_knjiznici(self):
        pot = settings.FRONTEND_DIR / "static/js/body-muscles/body-muscles.umd.min.js"
        oznake_knjiznice = set(re.findall(r'id:"([a-z-]+)"', pot.read_text(encoding="utf-8")))
        uporabljene = [o for m in Misica.objects.all() for o in m.oznake.split(",")]
        self.assertEqual(len(uporabljene), len(set(uporabljene)))  # nobena oznaka ni v dveh skupinah
        self.assertLessEqual(set(uporabljene), oznake_knjiznice)

    def test_us03_ac1_stran_s_pogledom_spredaj_in_zadaj(self):
        Misica.objects.filter(ime="prsa").update(oznake="chest-upper-left, chest-upper-right")  # presledek iz admina
        self.trening("Potisk s prsi", 4, self.danes)
        odgovor = self.client.get("/statistika/misice/")
        self.assertContains(odgovor, 'id="spredaj"')
        self.assertContains(odgovor, 'id="zadaj"')
        stanje = odgovor.context["stanje"]
        self.assertEqual(stanje["chest-upper-left"], {"intensity": 10, "selected": False})
        self.assertEqual(stanje["chest-upper-right"]["intensity"], 10)
        self.assertEqual(stanje["triceps-long-right"]["intensity"], 5)
        self.assertNotIn("quads-left", stanje)  # netrenirana mišica ostane siva

    def test_us03_ac3_netrenirane_so_nastete(self):
        self.trening("Potisk s prsi", 4, self.danes)
        odgovor = self.client.get("/statistika/misice/")
        imena = [m.ime for m in odgovor.context["netrenirane"]]
        self.assertIn("kvadriceps", imena)
        self.assertNotIn("prsa", imena)
        self.assertEqual([(m.ime, v) for m, v in odgovor.context["najbolj_obremenjene"]][0], ("prsa", 10))

    def test_us03_ac4_privzeto_7_dni_lahko_30_ali_od_do(self):
        self.trening("Počep", 3, self.danes - timedelta(days=10))
        odgovor = self.client.get("/statistika/misice/")
        self.assertEqual((odgovor.context["od"], odgovor.context["do"]), (self.danes - timedelta(days=6), self.danes))
        self.assertNotIn("quads-left", odgovor.context["stanje"])
        self.assertIn("quads-left", self.client.get("/statistika/misice/?dni=30").context["stanje"])
        dan = self.danes - timedelta(days=10)
        odgovor = self.client.get(f"/statistika/misice/?od={dan.isoformat()}&do={dan.isoformat()}")
        self.assertEqual(odgovor.context["od"], dan)
        self.assertIn("quads-left", odgovor.context["stanje"])

    def test_napacno_obdobje_obdrzi_privzeto(self):
        odgovor = self.client.get(f"/statistika/misice/?od={self.danes.isoformat()}&do={(self.danes - timedelta(days=3)).isoformat()}")
        self.assertContains(odgovor, "mora biti pred datumom")
        self.assertEqual(odgovor.context["od"], self.danes - timedelta(days=6))

    def test_us03_ac5_brez_treningov_sporocilo(self):
        odgovor = self.client.get("/statistika/misice/")
        self.assertContains(odgovor, "V tem obdobju ni zabeleženih treningov")
        self.assertEqual(odgovor.context["stanje"], {})


class ZemljevidZaTreneraTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def setUp(self):
        self.ana = uporabnik("ana")
        self.tomaz = uporabnik("tomaz")
        t = Trening.objects.create(uporabnik=self.ana, trajanje_min=60, porabljene_kcal=400)
        Serija.objects.create(trening=t, vaja=Vaja.objects.get(ime="Počep"), zaporedna_st=1, ponovitve=8, teza_kg=80)
        self.client.force_login(self.tomaz)
        self.url = f"/statistika/misice/{self.ana.pk}/"

    def dostop(self, vrsta):
        Dostop.objects.create(sportnik=self.ana, strokovnjak=self.tomaz, vrsta=vrsta, status="AKTIVEN")

    def test_us05_ac4_trener_vidi_statistiko_treningov(self):
        self.dostop("TRENER")
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.context["stanje"]["quads-left"]["intensity"], 10)
        self.assertContains(odgovor, "zemljevid mišic – Ana")
        self.assertContains(self.client.get("/moji-sportniki/"), f'href="{self.url}"')

    def test_us05_ac4_svetovalec_in_brez_dostopa_ne_vidita(self):
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.dostop("PREHRANSKI_SVETOVALEC")
        self.assertEqual(self.client.get(self.url).status_code, 404)
