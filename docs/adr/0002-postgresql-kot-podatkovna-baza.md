---
status: accepted
date: 2026-10-15
---

# PostgreSQL kot podatkovna baza

## Kontekst in problem

Podatki so med seboj močno povezani (uporabnik → trening → serija → vaja → mišica), dostopi, plani in cilji pa imajo stanja, ki jih mora baza zanesljivo hraniti. Zato je potrebna relacijska baza, ki jo Django podpira.

## Obravnavane možnosti

* PostgreSQL
* SQLite

## Odločitev

Izbrana možnost: »PostgreSQL«, ker je samostojen strežnik, kot bi ga aplikacija uporabljala tudi v resničnem okolju. Django ga podpira brez dodatnih orodij, potreben je samo gonilnik `psycopg`.

### Posledice

* Dobro, ker baze kasneje ni treba menjati, kar bi bilo pri SQLite lahko potrebno.
* Slabo, ker mora vsak razvijalec namestiti PostgreSQL, ustvariti prazno bazo in podatke za povezavo vpisati v datoteko `.env`. SQLite bi bil ena datoteka brez namestitve.
