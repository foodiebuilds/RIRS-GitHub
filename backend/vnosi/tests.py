from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from uporabniki.models import Uporabnik

from .models import DnevniCilj, Vnos, cilj_za_dan


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
