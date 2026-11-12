from django.db import IntegrityError
from django.test import TestCase

from .models import Uporabnik


class ModelUporabnikaTest(TestCase):
    def test_us01_ac1_nov_racun_je_racun_sportnika(self):
        u = Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        self.assertEqual(u.ime, "Ana")
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)

    def test_us01_ac2_e_posta_je_enolicna(self):
        Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        with self.assertRaises(IntegrityError):
            Uporabnik.objects.create_user("ana2", "ana@primer.si", "Geslo-12345", ime="Ana")


class PrijavaTest(TestCase):
    def setUp(self):
        self.ana = Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")

    def prijava(self, ime, geslo):
        return self.client.post("/prijava/", {"username": ime, "password": geslo})

    def test_us01_ac3_prijava_z_uporabniskim_imenom(self):
        self.assertRedirects(self.prijava("ana", "Geslo-12345"), "/")
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.ana.pk)

    def test_us01_ac3_prijava_z_e_posto(self):
        self.assertRedirects(self.prijava("ana@primer.si", "Geslo-12345"), "/")
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.ana.pk)

    def test_us01_ac4_napacni_podatki(self):
        for ime, geslo in [("ana", "napacno"), ("ana@primer.si", "napacno"), ("neobstaja", "Geslo-12345")]:
            odgovor = self.prijava(ime, geslo)
            self.assertContains(odgovor, "Napačni podatki za prijavo")
            self.assertNotIn("_auth_user_id", self.client.session)

    def test_us01_ac5_blokiran_racun_se_ne_more_prijaviti(self):
        self.ana.is_active = False
        self.ana.save()
        for ime in ("ana", "ana@primer.si"):
            self.prijava(ime, "Geslo-12345")
            self.assertNotIn("_auth_user_id", self.client.session)

    def test_domov_samo_za_prijavljene_in_odjava(self):
        self.assertRedirects(self.client.get("/"), "/prijava/?next=/")
        self.client.force_login(self.ana)
        self.assertContains(self.client.get("/"), "Pozdravljen, Ana")
        self.assertRedirects(self.client.post("/odjava/"), "/prijava/")
        self.assertNotIn("_auth_user_id", self.client.session)


class EpostaVelikeCrkeTest(TestCase):
    def test_us01_ac3_prijava_z_e_posto_ne_glede_na_velike_crke(self):
        Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        odgovor = self.client.post("/prijava/", {"username": "Ana@Primer.si", "password": "Geslo-12345"})
        self.assertRedirects(odgovor, "/")
