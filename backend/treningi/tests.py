from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Misica, Vaja, VajaMisica


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
