---
status: accepted
date: 2026-10-15
---

# Trener in prehranski svetovalec nista posebni vrsti računa, ampak dostop med dvema uporabnikoma

## Kontekst in problem

Med vlogami v aplikaciji so športnik, trener in prehranski svetovalec. Športnik lahko drugega uporabnika povabi kot trenerja, kot prehranskega svetovalca ali kot oboje. Povabljeni vidi samo podatke, ki spadajo k njegovi vlogi, športnik pa lahko dostop kadarkoli prekliče. Določiti je bilo treba, kje sta vlogi trenerja in svetovalca zapisani.

## Obravnavane možnosti

* Vloga kot dostop med dvema uporabnikoma (tabela Dostop)
* Trener in prehranski svetovalec kot posebni vrsti računa

## Odločitev

Izbrana možnost: »Vloga kot dostop med dvema uporabnikoma (tabela Dostop)«, ker je ista oseba lahko športnik, trener in svetovalec, pravice pa se preverjajo po vrsti in stanju dostopa.

### Posledice

* Dobro, ker uporabnik za vse vloge potrebuje samo en račun.
* Dobro, ker trener in svetovalec vidita samo podatke športnikov, ki so jima dali AKTIVEN dostop, in samo podatke svoje vrste dostopa.
* Slabo, ker je preverjanje pravic bolj zapleteno: pri vsaki zahtevi za podatke drugega uporabnika je treba preveriti vrsto in stanje dostopa.
