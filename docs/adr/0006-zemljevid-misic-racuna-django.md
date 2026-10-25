---
status: accepted
date: 2026-10-15
---

# Zemljevid mišic računa Django, nariše ga knjižnica

## Kontekst in problem

Statistika prikaže zemljevid mišic: telo spredaj in zadaj, kjer so mišice obarvane glede na to, koliko so bile trenirane v izbranem obdobju. Določiti je bilo treba, kje se obremenitev mišic izračuna in s čim se telo nariše.

## Obravnavane možnosti

* Izračun v Djangu, risanje s knjižnico `body-muscles`
* Izračun v Djangu, risanje s knjižnico `react-body-highlighter`
* Izračun in risanje v brskalniku (JavaScript)

## Odločitev

Izbrana možnost: »Izračun v Djangu, risanje s knjižnico `body-muscles`«, ker je pravilo štetja tako na enem mestu, knjižnica pa deluje z navadnim JavaScriptom. Django za izbrano obdobje sešteje serije po mišicah (glavna mišica 1, pomožna 0,5) in jih preračuna na lestvico 0–10, ki jo uporablja knjižnica. Knjižnica `body-muscles` (licenca Apache 2.0) ima pogled spredaj in zadaj, barvno lestvico intenzivnosti ter že 70+ mišic in imenovane skupine mišic. Knjižnica `react-body-highlighter` je komponenta za React, ki ga aplikacija ne uporablja, licenca pa na njeni strani ni navedena.

### Posledice

* Dobro, ker JavaScript na strani samo nariše podatke, ki jih Django vstavi v stran.
* Dobro, ker je knjižnica pripravljena tudi za kasnejši podrobnejši model telesa.
* Slabo, ker je projekt odvisen od knjižnice `body-muscles`, ki ima eno samo različico (1.0.0) in enega vzdrževalca. Datoteko knjižnice je zato treba hraniti v projektu.
