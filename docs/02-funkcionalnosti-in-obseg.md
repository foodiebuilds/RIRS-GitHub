# Funkcionalnosti in obseg

## Uporabniške vloge

Vsak registriran uporabnik je športnik. Vlogi trenerja in prehranskega svetovalca nista posebni vrsti računa: uporabnik ju dobi, ko mu športnik dovoli dostop do svojih podatkov. Ista oseba je lahko za enega športnika trener in prehranski svetovalec hkrati, za drugega pa samo eno od tega. Primer: Prehranski strokovnjak npr. ne more dostopati do npr. vaj, ki jih je športnik izvajal na treningu, ima pa dostop do primernih informacij npr. predvideno pokurjenih kalorij.

### 1. Športnik

**Lahko:**

- beleži treninge (vaja, serije, ponovitve, teža, trajanje, porabljene kalorije),
- beleži vnos vode in kalorij ter si nastavi dnevni cilj,
- gleda svojo statistiko in zemljevid mišic,
- sestavi svoj plan treningov,
- sprejme ali prilagodi plan, ki mu ga predlaga trener,
- planirane treninge označi kot opravljene ali izpuščene,
- povabi drugega uporabnika kot trenerja, prehranskega svetovalca ali oboje in mu dostop kadarkoli prekliče,
- beleži počutje za posamezen trening ali kadarkoli čez dan ter svojo težo,
- vse svoje vnose vidi na časovnici.

**Nima pravic:**

- ne vidi podatkov drugih uporabnikov (tudi podatkov svojega trenerja ali svetovalca ne),
- ne more izbrisati trenerjevega predloga plana – ob prilagoditvi se predlog ohrani, da trener vidi razliko,
- ne more spreminjati ali brisati komentarjev trenerja in svetovalca,
- ne more urejati seznama vaj.

### 2. Trener

**Lahko:**

- vse, kar lahko športnik, za svoje podatke,
- vidi treninge, plane, statistiko treningov, počutje in težo športnikov, ki so mu dali dostop,
- športniku predlaga plan treningov,
- vidi, kako je športnik njegov predlog prilagodil,
- komentira trening in vnose na časovnici, ki jih vidi.

**Nima pravic:**

- ne vidi športnikov, ki mu niso dali dostopa,
- ne vidi vnosa kalorij in vode, če mu športnik ni dal tudi dostopa prehranskega svetovalca,
- ne more spreminjati ali brisati športnikovih vnosov in ne more spremeniti plana, ki ga je športnik že sprejel ali prilagodil,
- ne more urejati seznama vaj.

### 3. Prehranski svetovalec

**Lahko:**

- vse, kar lahko športnik, za svoje podatke,
- vidi vnos kalorij in vode, porabljene kalorije na treningih, dnevne cilje, počutje in težo športnikov, ki so mu dali dostop,
- komentira vnose na časovnici, ki jih vidi,
- športniku predlaga dnevni cilj kalorij in vode.

**Nima pravic:**

- ne vidi športnikov, ki mu niso dali dostopa,
- ne vidi vaj, serij in planov, če mu športnik ni dal tudi dostopa trenerja,
- ne more spreminjati športnikovih vnosov in ne more sam spremeniti njegovega dnevnega cilja (lahko ga samo predlaga).

### 4. Administrator

**Lahko:**

- dodaja in ureja vaje in mišice ter za vsako vajo določi, katere mišice obremeni (glavne in pomožne),
- upravlja uporabniške račune (npr. blokira račun).

**Nima pravic:**

- ne vidi treningov, vnosa kalorij in vode, počutja ali teže uporabnikov,
- ne more dobiti dostopa do podatkov športnika in ne more delati v imenu drugega uporabnika.

## Predvidene funkcionalnosti

**MVP** (angl. *minimum viable product*) je prva različica aplikacije, ki že deluje in je uporabna, čeprav še nima vseh funkcionalnosti. Funkcionalnosti z oznako MVP bodo narejene najprej, ostale kasneje.

| # | Funkcionalnost | MVP |
| --- | --- | --- |
| 1 | Registracija in prijava z uporabniškim imenom/e-mailom in geslom. | MVP |
| 2 | Hitro beleženje treninga: izbira vaje, vnos serij (ponovitve, teža etc.), trajanja in porabljenih kalorij; gumb »ponovi zadnji trening«. | MVP |
| 3 | Zemljevid obremenitve mišic: slika telesa spredaj in zadaj. Za izbrano obdobje sistem iz opravljenih serij izračuna obremenitev vsake mišice (glavna mišica vaje šteje 1, pomožna 0,5), vrednosti preračuna na lestvico 0–10 glede na najbolj obremenjeno mišico in mišice ustrezno obarva. Mišice, ki v obdobju niso bile trenirane, so posebej označene. | MVP |
| 4 | Voda in obroki z dnevnim ciljem: hitri gumbi za vodo (npr. +250 ml), obrok se vnese z besednim opisom in ocenjenimi kalorijami, prikaz, koliko manjka do dnevnega cilja. | MVP |
| 5 | Dostop za trenerja in prehranskega svetovalca: povabilo → sprejem → preklic. Od vrste dostopa je odvisno, katere podatke povabljeni vidi. | MVP |
| 6 | Plan treningov z različicami: športnik sestavi svoj plan, ali trener predlaga plan → športnik ga sprejme ali prilagodi. Prilagoditev ustvari novo različico plana, trenerjev predlog pa ostane shranjen. Trener vidi primerjavo obeh različic po vajah (dodane, odstranjene in spremenjene vaje, serije, ponovitve). Športnik treninge označi kot opravljene ali izpuščene, opravljen trening pa se poveže s planiranim, da je vidno, ali je bil narejen po planu. | MVP |
| 7 | Časovnica in počutje: športnik beleži počutje za posamezen trening ali ob poljubnem delu dneva ter težo. Vsi vnosi (treningi, voda, kalorije, počutje, teža, komentarji) se prikažejo na časovnici po dnevih. Trener in svetovalec na časovnici vidita samo vnose, ki spadajo k njuni vrsti dostopa, in jih lahko komentirata. | MVP |
| 8 | Graf napredka pri posamezni vaji (največja teža in skupni volumen skozi čas). | |
| 9 | Izpolnjevanje plana: odstotek opravljenih treningov po tednih. | |
| 10 | Samodejno zaznavanje osebnih rekordov pri vajah. | |
| 11 | Opozorilo, ko mišična skupina ni bila trenirana 7 ali več dni. | |
| 12 | Samodejna ocena porabljenih kalorij iz trajanja treninga, vrste vaj in teže športnika (namesto ročnega vnosa). | |
| 13 | Predlog dnevnega cilja kalorij in vode s strani svetovalca, ki ga športnik sprejme ali zavrne. | |
| 14 | Pregled vseh športnikov, ki so trenerju ali svetovalcu dali dostop, z zadnjo aktivnostjo. | |
| 15 | Urejanje seznama vaj in mišic (administrator). | |

Domensko specifične funkcionalnosti v MVP (ne samo CRUD): 3, 4, 5, 6, 7. Najbolj zahtevni sta 3 (izračun obremenitve mišic) in 6 (različice plana in njihova primerjava).

Predviden delovni proces: trener predlaga plan → športnik ga sprejme ali prilagodi → trener vidi spremembe → športnik opravlja ali izpušča treninge → športnik sproti/dnevno vnaša podatke → trener ima vedno vpogled, pregleda in predlaga nov plan.

## Kasnejše potencialne nadgradnje

- baza živil s kalorijami in makrohranili namesto besednega opisa obroka in ročne ocene kalorij,
- jedilnik, ki ga prehranski svetovalec predlaga športniku (podobno kot plan treningov),
- skeniranje črtne kode živila (ni taka prioriteta),
- namestitev aplikacije na telefon (PWA) in beleženje brez povezave, ki se sinhronizira, ko je povezava spet na voljo,
- predloge planov, ki jih trener lahko uporabi za več športnikov,
- obvestila (opomnik za vodo, nov predlog plana, nov komentar),
- uvoz podatkov iz pametne ure,
- klepet med športnikom in trenerjem ali svetovalcem.
- podrobnejši model telesa: posamezne mišice (namesto večjih mišičnih skupin), ki jih administrator združuje v večje skupine (npr. prsa, hrbet, noge); zemljevid mišic lahko prikaže skupino ali posamezno mišico.

## Out of scope

- plačila in naročnine trenerju ali svetovalcu,
- zdravstveni nasveti in diagnoze – aplikacija samo beleži, ne svetuje,
- javni profili in deljenje treningov z drugimi uporabniki (ni družbeno omrežje),
- samodejno sestavljanje planov treningov.
