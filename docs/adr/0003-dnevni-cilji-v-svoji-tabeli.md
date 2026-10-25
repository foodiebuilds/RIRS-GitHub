---
status: accepted
date: 2026-10-15
---

# Dnevni cilji v svoji tabeli

## Kontekst in problem

Športnik si nastavi dnevni cilj kalorij in vode, prehranski svetovalec mu ga lahko predlaga. Cilji se s časom spreminjajo, graf vode in kalorij pa prikazuje vnos glede na dnevni cilj. Določiti je bilo treba, kako se cilji shranijo.

## Obravnavane možnosti

* Cilji v svoji tabeli (DnevniCilj)
* Cilj kot polji pri uporabniku (cilj_kcal, cilj_voda_ml) in ločena tabela za svetovalčeve predloge

## Odločitev

Izbrana možnost: »Cilji v svoji tabeli (DnevniCilj)«, ker tabela hrani tudi stare cilje in svetovalčeve predloge. Vsak cilj ima datum, od katerega velja, in stanje (npr. PREDLAGAN, AKTIVEN, ZAMENJAN).

### Posledice

* Dobro, ker grafi za pretekle dni primerjajo vnos s ciljem, ki je veljal tisti dan.
* Dobro, ker za svetovalčeve predloge ni potrebna dodatna tabela.
* Slabo, ker je treba za vsak dan poiskati cilj, ki je takrat veljal, in ob novem cilju starega označiti kot ZAMENJAN.
