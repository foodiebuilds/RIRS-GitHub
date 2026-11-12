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
