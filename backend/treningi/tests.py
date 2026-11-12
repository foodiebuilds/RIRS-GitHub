from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Misica, Trening, Vaja, VajaMisica


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
