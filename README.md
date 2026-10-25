# KarRabimZaGym

Spletna aplikacija za beleženje napredka v fitnesu in za sodelovanje s trenerjem in prehranskim svetovalcem. Športnik beleži treninge (vaje, serije, porabljene kalorije), počutje ter vnos kalorij in vode. Trener in prehranski svetovalec imata, če jima športnik to dovoli, vpogled v njegove podatke in jih lahko komentirata. Trener lahko športniku predlaga plan treningov.

## Tehnologije

| Del | Tehnologije |
|---|---|
| Frontend | Django predloge (HTML, CSS), JavaScript knjižnici `body-muscles` (zemljevid mišic) in Chart.js (grafi) |
| Backend | Python, Django |
| Podatkovna baza | PostgreSQL (gonilnik `psycopg`) |
| Avtentikacija | vgrajen Django sistem za uporabnike |
| Lokalni razvoj | Python, lokalno nameščen PostgreSQL, Git in GitHub |
| Drugo | Django admin za administratorja |

## Dokumentacija

- [Zasnova rešitve](docs/01-zasnova-resitve.md)
- [Funkcionalnosti in obseg](docs/02-funkcionalnosti-in-obseg.md)
- [Podatkovni model](docs/03-podatkovni-model.md)
- [Arhitektura in tehnološki sklad](docs/04-arhitektura-in-tehnoloski-sklad.md)
- [Uporabniške zgodbe](docs/05-uporabniske-zgodbe.md)
- [Wireframes](docs/06-wireframes.md)
- [Arhitekturne odločitve (ADR)](docs/adr/)
