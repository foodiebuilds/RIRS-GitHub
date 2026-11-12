---
status: accepted
date: 2026-11-11
---

# Mišične skupine povezane z deli telesa v knjižnici

## Kontekst in problem

V podatkovnem modelu (`03-podatkovni-model.md`) so mišice večje mišične skupine (npr. prsa, ramena, kvadriceps) s pogledom spredaj ali zadaj. Knjižnica `body-muscles` (ADR-0006) pa nariše 89 manjših delov telesa, levo in desno posebej. Ena skupina zato obsega več delov telesa, nekatere (npr. ramena) tudi na obeh pogledih. Odločiti se je bilo treba, kje je zapisano, kateri deli telesa spadajo k skupini.

## Obravnavane možnosti

* Polje z oznakami delov telesa pri mišici (`Misica.oznake`)
* Preslikava skupin v kodi (slovar v Pythonu)
* Mišice v bazi kot posamezni deli telesa iz knjižnice

## Odločitev

Izbrana možnost: »Polje z oznakami delov telesa pri mišici (`Misica.oznake`)«, ker mišične skupine ostanejo take kot v podatkovnem modelu in na zemljevidu mišic (W2), povezavo z deli telesa pa lahko administrator spremeni brez spremembe kode. Posamezni deli telesa kot mišice so med kasnejšimi nadgradnjami (podrobnejši model telesa v `02-funkcionalnosti-in-obseg.md`).

### Posledice

* Dobro, ker je 15 mišičnih skupin enakih kot na wireframu W2, vaje pa se povezujejo s skupinami kot v podatkovnem modelu.
* Dobro, ker test preveri, da vsaka oznaka obstaja v datoteki knjižnice in da noben del telesa ni v dveh skupinah.
* Slabo, ker polja ni v podatkovnem modelu iz 1. naloge.
* Slabo, ker knjižnica neznane oznake ne prikaže in ne javi napake. Test preveri samo oznake v začetnih podatkih, zato napačno oznako, vpisano v adminu, opazimo šele na zemljevidu.
