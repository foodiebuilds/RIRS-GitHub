from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Vnos


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
