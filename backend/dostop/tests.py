from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Dostop


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
