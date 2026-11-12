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

## Lokalni zagon

Potrebni so Python 3.12 ali novejši, PostgreSQL 15 ali novejši in Git. Ukazi so za Windows (cmd).

1. Prenesi repozitorij in pojdi v mapo `backend`:

   ```
   git clone https://github.com/foodiebuilds/RIRS-GitHub.git
   cd RIRS-GitHub\backend
   ```

2. Ustvari virtualno okolje in namesti pakete:

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ustvari bazo v PostgreSQL (pot do `psql.exe` je odvisna od nameščene različice):

   ```
   "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE karrabimzagym;"
   ```

4. Kopiraj `.env.example` v `.env` in v `.env` vpiši geslo uporabnika `postgres` (`DB_PASSWORD`):

   ```
   copy .env.example .env
   ```

5. Ustvari tabele in račun administratorja:

   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Zaženi aplikacijo:

   ```
   python manage.py runserver
   ```

Aplikacija teče na `http://127.0.0.1:8000`, administracija na `http://127.0.0.1:8000/admin`.

Testi: `python manage.py test` (v mapi `backend`, z aktivnim virtualnim okoljem).
