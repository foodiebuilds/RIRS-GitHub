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


class RegistracijaTest(TestCase):
    podatki = {
        "ime": "Ana",
        "username": "ana",
        "email": "ana@primer.si",
        "password1": "Mocno-Geslo-123",
        "password2": "Mocno-Geslo-123",
    }

    def test_us01_ac1_registracija_ustvari_racun_sportnika(self):
        odgovor = self.client.post("/registracija/", self.podatki)
        self.assertRedirects(odgovor, "/prijava/")
        u = Uporabnik.objects.get(username="ana")
        self.assertEqual((u.ime, u.email), ("Ana", "ana@primer.si"))
        self.assertFalse(u.is_staff)
        self.assertTrue(u.check_password("Mocno-Geslo-123"))

    def test_us01_ac1_registracija_zahteva_vsa_polja(self):
        for polje in ("ime", "username", "email", "password1"):
            odgovor = self.client.post("/registracija/", {**self.podatki, polje: ""})
            self.assertIn(polje, odgovor.context["form"].errors)
        self.assertFalse(Uporabnik.objects.exists())

    def test_us01_ac2_zasedeno_uporabnisko_ime(self):
        Uporabnik.objects.create_user("ana", "druga@primer.si", "Geslo-12345", ime="Ana")
        odgovor = self.client.post("/registracija/", self.podatki)
        self.assertEqual(list(odgovor.context["form"].errors), ["username"])
        self.assertEqual(Uporabnik.objects.count(), 1)

    def test_us01_ac2_zasedena_e_posta(self):
        Uporabnik.objects.create_user("drugi", "ana@primer.si", "Geslo-12345", ime="Drugi")
        odgovor = self.client.post("/registracija/", self.podatki)
        self.assertEqual(list(odgovor.context["form"].errors), ["email"])
        self.assertEqual(Uporabnik.objects.count(), 1)

    def test_us01_ac3_nov_racun_se_lahko_prijavi(self):
        self.client.post("/registracija/", self.podatki)
        odgovor = self.client.post("/prijava/", {"username": "ana@primer.si", "password": "Mocno-Geslo-123"})
        self.assertRedirects(odgovor, "/")


class EpostaVelikeCrkeTest(TestCase):
    def test_us01_ac3_prijava_z_e_posto_ne_glede_na_velike_crke(self):
        Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        odgovor = self.client.post("/prijava/", {"username": "Ana@Primer.si", "password": "Geslo-12345"})
        self.assertRedirects(odgovor, "/")

    def test_us01_ac2_zasedena_e_posta_z_drugacnimi_velikimi_crkami(self):
        Uporabnik.objects.create_user("drugi", "Ana@primer.si", "Geslo-12345", ime="Drugi")
        podatki = {**RegistracijaTest.podatki, "email": "Ana@Primer.si"}
        odgovor = self.client.post("/registracija/", podatki)
        self.assertEqual(list(odgovor.context["form"].errors), ["email"])
        self.assertEqual(Uporabnik.objects.count(), 1)

    def test_us01_ac2_e_posta_je_enolicna_ne_glede_na_velike_crke(self):
        Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        with self.assertRaises(IntegrityError):
            Uporabnik.objects.create_user("ana2", "ANA@primer.si", "Geslo-12345", ime="Ana")
