---
status: accepted
date: 2026-10-15
---

# Ločen frontend in backend

## Kontekst in problem

Aplikacija potrebuje strani za vnos in pregled podatkov ter logiko za pravice, stanja in izračune (npr. zemljevid mišic). Odločiti se je bilo treba, ali bosta frontend in backend ločena ali skupaj.

## Obravnavane možnosti

* Ločen frontend in backend
* Skupen frontend in backend v eni Django aplikaciji

## Odločitev

Izbrana možnost: »Ločen frontend in backend«, ker predmet zahteva ločen frontend in backend. Frontend (Django predloge, HTML, CSS ter JavaScript knjižnici `body-muscles` in Chart.js), backend pa (Python, Django). Django ima že vgrajene uporabnike, prijavo, delo z bazo, migracije in administracijo, zato tega ni treba pisati na novo.

### Posledice

* Dobro, ker rešitev ustreza zahtevi predmeta in strukturi repozitorija.
* Dobro, ker ostanejo že izbrane tehnologije in ni treba pisati API-ja med frontendom in backendom.
* Slabo, ker je treba v Djangu nastaviti, da predloge in statične datoteke išče v mapi `frontend/`.
* Slabo, ker strani še vedno sestavi Django, zato frontenda ni mogoče zagnati brez backenda.
* Slabo, ker za kasnejšo mobilno aplikacijo zdaj ni API-ja. Djangu se lahko doda REST API, obstoječa logika in baza pa ostaneta.
