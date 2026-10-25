---
status: accepted
date: 2026-10-15
---

# Django namesto ločenega frontenda in backenda

## Kontekst in problem

Aplikacija potrebuje strani za vnos in pregled podatkov ter logiko za pravice, stanja in izračune (npr. zemljevid mišic). Odločiti se je bilo treba, ali bo uporabniški vmesnik ločena aplikacija, ki z backendom komunicira prek REST API-ja, ali pa bo vse v eni Django aplikaciji.

## Obravnavane možnosti

* Ena Django aplikacija (Django predloge)
* Ločen frontend (React, TypeScript) in backend z REST API-jem (Spring Boot, Kotlin)

## Odločitev

Izbrana možnost: »Ena Django aplikacija (Django predloge)«, ker je ena aplikacija v enem jeziku za ta obseg dovolj in je enostavnejša za razvoj. Django ima že vgrajene uporabnike, prijavo, delo z bazo, migracije in administracijo, zato tega ni treba pisati na novo. Python že poznam.

### Posledice

* Dobro, ker je vsa logika na enem mestu in v enem jeziku (Python).
* Dobro, ker ni treba pisati in vzdrževati API-ja med frontendom in backendom.
* Slabo, ker Django ob vsakem oddanem obrazcu vrne novo stran, zato so strani manj interaktivne kot pri ločenem frontendu.
* Slabo, ker za kasnejšo mobilno aplikacijo zdaj ni API-ja. Djangu se lahko doda REST API, obstoječa logika in baza pa ostaneta.
