# Uporabniške zgodbe

## US-01 – Registracija in prijava

- **Povezana funkcionalnost:** 1 – Registracija in prijava (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim ustvariti račun in se prijaviti z uporabniškim imenom ali e-pošto, da so moji podatki shranjeni pod mojim računom in jih poleg mene vidijo samo osebe, ki jim dam dostop.
- **Acceptance criteria:**
  - Registracija zahteva ime, uporabniško ime, e-pošto in geslo. Nov račun je račun športnika.
  - Če uporabniško ime ali e-pošta že obstaja, račun ni ustvarjen in sistem pokaže, katero polje je že zasedeno.
  - Prijava deluje z uporabniškim imenom in geslom ali z e-pošto in geslom.
  - Ob napačnem uporabniškem imenu, e-pošti ali geslu sistem uporabnika ne prijavi in pokaže sporočilo »Napačni podatki za prijavo«.
  - Uporabnik, ki mu je administrator blokiral račun, se ne more prijaviti.

## US-02 – Beleženje treninga

- **Povezana funkcionalnost:** 2 – Hitro beleženje treninga (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim med treningom vpisati vaje in serije, da imam natančen zapis treninga brez počasnega vpisovanja v Excel.
- **Acceptance criteria:**
  - Vajo izberem s seznama vaj, za vsako serijo vpišem število ponovitev in težo v kg.
  - K treningu vpišem trajanje v minutah in porabljene kalorije.
  - Pri vsakem preteklem treningu, tudi pri zadnjem, je gumb »Kopiraj trening«. En klik ustvari nov trening z istimi vajami in serijami, številke lahko pred shranjevanjem popravim.
  - Shranjen trening se prikaže na seznamu preteklih treningov in na časovnici.
  - Na seznam vaj ne morem dodati nove vaje ali obstoječe spremeniti, izbiram samo med vajami, ki jih je vnesel administrator.

## US-03 – Zemljevid obremenitve mišic

- **Povezana funkcionalnost:** 3 – Zemljevid obremenitve mišic (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim za izbrano obdobje videti, koliko sem obremenil posamezne mišice, da vidim, katere mišične skupine treniram premalo.
- **Acceptance criteria:**
  - Zemljevid prikaže telo spredaj in zadaj, vsaka mišica je obarvana glede na obremenitev na lestvici 0–10.
  - Vsaka opravljena serija v obdobju prišteje 1 glavni mišici vaje in 0,5 vsaki pomožni mišici. Najbolj obremenjena mišica dobi 10, ostale sorazmerno manj (primer: prsa 12 točk → 10, triceps 6 točk → 5).
  - Mišice, ki v obdobju niso bile trenirane, so sive. Vsaka trenirana mišica ima vrednost najmanj 1, zato nikoli ni siva.
  - Privzeto obdobje je zadnjih 7 dni. Izberem lahko tudi zadnjih 30 dni ali poljuben razpon od–do.
  - Če v obdobju ni nobenega treninga, so vse mišice sive in prikaže se sporočilo »V tem obdobju ni zabeleženih treningov«.

## US-04 – Voda in obroki z dnevnim ciljem

- **Povezana funkcionalnost:** 4 – Voda in obroki z dnevnim ciljem (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim z enim klikom zabeležiti vodo in na kratko vpisati obroke, da vidim, koliko mi do dnevnega cilja še manjka.
- **Acceptance criteria:**
  - En klik na gumb »+250 ml« doda 250 ml vode k današnjemu vnosu.
  - Obrok vnesem z besednim opisom in oceno kalorij (npr. »piščanec z rižem in solata«, 650 kcal).
  - Dnevni cilj kalorij in vode si nastavim sam. Nov cilj velja od dneva, ko ga nastavim.
  - Za današnji dan je prikazano, koliko kalorij in vode sem že vnesel in koliko manjka do cilja (npr. »1,5 l od 2,5 l, manjka 1 l«).
  - Za pretekle dni se vnos primerja s ciljem, ki je veljal tisti dan, ne s trenutnim ciljem.

## US-05 – Dostop za trenerja in prehranskega svetovalca

- **Povezana funkcionalnost:** 5 – Dostop za trenerja in prehranskega svetovalca (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim drugega uporabnika povabiti kot trenerja, prehranskega svetovalca ali oboje in mu dostop kadarkoli preklicati, da sam odločam, kdo vidi moje podatke.
- **Acceptance criteria:**
  - Povabilo pošljem z uporabniškim imenom obstoječega uporabnika in izberem vrsto dostopa: trener, prehranski svetovalec ali oboje. Za neobstoječe uporabniško ime sistem pokaže sporočilo, da uporabnik ne obstaja.
  - Povabljeni povabilo sprejme ali zavrne. Dokler ga ne sprejme, ne vidi nobenih mojih podatkov.
  - Po sprejemu se moje ime povabljenemu prikaže na seznamu »Moji športniki«.
  - Trener vidi samo moje treninge, plane, statistiko treningov, počutje in težo. Prehranski svetovalec vidi samo vnos kalorij in vode, porabljene kalorije na treningih, dnevne cilje, počutje in težo.
  - Po preklicu dostopa povabljeni ne vidi več nobenih mojih podatkov in me ni več na njegovem seznamu »Moji športniki«.

## US-06 – Plan treningov z različicami

- **Povezana funkcionalnost:** 6 – Plan treningov z različicami (MVP)
- **Uporabniška vloga:** trener
- **Uporabniška zgodba:** Kot trener želim športniku predlagati tedenski plan treningov in videti, kako ga je prilagodil in katere treninge je opravil, da lahko pripravim naslednji plan.
- **Acceptance criteria:**
  - Trener za izbrani teden pripravi plan po dnevih: treninge in pri vsakem vaje s številom serij in ponovitev. Plan pošlje športniku kot predlog. Športnik brez trenerja si plan pripravi sam na enak način.
  - Športnik predlog sprejme ali prilagodi. Prilagoditev ustvari novo različico plana, trenerjev predlog pa ostane shranjen in ga športnik ne more izbrisati.
  - Trener vidi primerjavo predloga in prilagojene različice po vajah (dodane, odstranjene in spremenjene vaje, serije in ponovitve) ter datum predloga in datum spremembe.
  - Pri vsakem planiranem treningu trener vidi, ali ga je športnik označil kot opravljenega ali izpuščenega. Pri opravljenem lahko odpre trening, ki ga je športnik zabeležil (vaje, serije, teže).
  - Ko športnik predlog sprejme ali prilagodi, ga trener ne more več spreminjati.

## US-07 – Časovnica in počutje

- **Povezana funkcionalnost:** 7 – Časovnica in počutje (MVP)
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim beležiti počutje in težo ter vse svoje vnose videti na časovnici po dnevih, da imamo s trenerjem in svetovalcem pregled nad mojim dnem na enem mestu.
- **Acceptance criteria:**
  - Počutje ocenim na lestvici 1–5 za posamezen trening ali za poljuben del dneva. Težo vpišem v kg.
  - Časovnica prikaže vse moje vnose (treningi, voda, obroki, počutje, teža in komentarji) po dnevih, znotraj dneva po času.
  - Trener na moji časovnici vidi samo treninge, počutje in težo. Prehranski svetovalec vidi samo vodo, obroke, počutje, težo in pri treningih samo porabljene kalorije.
  - Trener in prehranski svetovalec lahko komentirata vnos, ki ga vidita. Komentar se prikaže pod vnosom z imenom avtorja in časom in ga vidi vsak, ki vidi ta vnos.
  - Komentarjev trenerja in prehranskega svetovalca ne morem spremeniti ali izbrisati.

## US-08 – Graf napredka pri vaji

- **Povezana funkcionalnost:** 8 – Graf napredka pri posamezni vaji
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim za izbrano vajo videti graf napredka skozi čas, da vidim, ali teže pri vaji naraščajo.
- **Acceptance criteria:**
  - Vajo izberem s seznama vaj, ki sem jih že izvajal.
  - Graf za vsak trening z izbrano vajo prikaže največjo težo v eni seriji (kg).
  - Graf za vsak trening z izbrano vajo prikaže skupni volumen: za vsako serijo ponovitve × teža, sešteto za vse serije (npr. 3 serije po 8 ponovitev z 80 kg = 1920 kg).
  - Če sem vajo izvajal na manj kot dveh treningih, se namesto grafa prikaže sporočilo, da za prikaz napredka še ni dovolj podatkov.
  - Trener, ki ima do mene dostop trenerja, vidi enak graf.

## US-09 – Izpolnjevanje plana

- **Povezana funkcionalnost:** 9 – Izpolnjevanje plana
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim videti, kolikšen del planiranih treningov sem opravil v vsakem tednu, da vem, kako dosledno sledim planu.
- **Acceptance criteria:**
  - Za vsak teden s planom je prikazan odstotek: opravljeni planirani treningi / vsi planirani treningi v tednu × 100 (npr. 3 od 4 = 75 %).
  - Izpuščeni in neoznačeni planirani treningi štejejo kot neopravljeni.
  - Trening, ki ni povezan s planiranim treningom, se v odstotek ne šteje.
  - Tedni brez plana so prikazani z oznako »ni plana«, ne z 0 %.
  - Trener, ki ima do mene dostop trenerja, vidi enak prikaz.

## US-10 – Osebni rekordi

- **Povezana funkcionalnost:** 10 – Samodejno zaznavanje osebnih rekordov pri vajah
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim samodejno videti svoje osebne rekorde pri vajah, da napredek vidim brez pregledovanja starih treningov.
- **Acceptance criteria:**
  - Osebni rekord pri vaji je največja teža v eni seriji te vaje.
  - Ko shranim trening, v katerem je teža pri vaji višja od dosedanjega rekorda, sistem pokaže sporočilo (npr. »Nov osebni rekord: počep 85 kg«).
  - Na seznamu osebnih rekordov je pri vsaki vaji rekord in datum, ko je bil dosežen.
  - Če popravim ali izbrišem serijo, v kateri je bil rekord, se rekord ponovno izračuna iz preostalih serij.

## US-11 – Opozorilo za netrenirano mišično skupino

- **Povezana funkcionalnost:** 11 – Opozorilo, ko mišična skupina ni bila trenirana 7 ali več dni
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim dobiti opozorilo, ko mišične skupine nisem treniral 7 ali več dni, da je ne zanemarim.
- **Acceptance criteria:**
  - Na strani »Statistika« je opozorilo za vsako mišično skupino, ki 7 ali več dni ni bila v nobeni seriji kot glavna ali pomožna mišica.
  - Opozorilo vsebuje ime mišične skupine in število dni od zadnjega treninga (npr. »Meča: 9 dni brez treninga«).
  - Ko shranim trening s serijo, ki to mišično skupino obremeni, opozorilo izgine.
  - Za mišično skupino, ki je še nikoli nisem treniral, opozorilo pravi »še ni bila trenirana«.
  - Trener, ki ima do mene dostop trenerja, vidi enaka opozorila.

## US-12 – Samodejna ocena porabljenih kalorij

- **Povezana funkcionalnost:** 12 – Samodejna ocena porabljenih kalorij
- **Uporabniška vloga:** športnik
- **Uporabniška zgodba:** Kot športnik želim samodejno oceno porabljenih kalorij na treningu, da mi jih ni treba ocenjevati in vpisovati ročno.
- **Acceptance criteria:**
  - Pri vnosu treninga sistem izračuna oceno porabljenih kalorij iz trajanja treninga, vaj v treningu in moje zadnje vpisane teže.
  - Ocena se izpiše v polju za porabljene kalorije, pred shranjevanjem jo lahko popravim.
  - Če teže še nisem vpisal, sistem ocene ne izračuna in me pozove, naj vpišem težo.
  - Pri enakem trajanju in enakih vajah je ocena za težjega športnika višja.

## US-13 – Predlog dnevnega cilja

- **Povezana funkcionalnost:** 13 – Predlog dnevnega cilja kalorij in vode s strani svetovalca
- **Uporabniška vloga:** prehranski svetovalec
- **Uporabniška zgodba:** Kot prehranski svetovalec želim športniku predlagati dnevni cilj kalorij in vode, da ima cilj, ki ustreza njegovi prehrani.
- **Acceptance criteria:**
  - Za športnika, ki mi je dal dostop prehranskega svetovalca, vnesem predlog cilja (kcal in ml vode) in datum, od katerega naj velja.
  - Športnik predlog sprejme ali zavrne. Dokler se ne odloči, velja njegov dosedanji cilj.
  - Sprejet predlog postane športnikov dnevni cilj od navedenega datuma, prejšnji cilj ostane shranjen za pretekle dni.
  - Vidim, ali je športnik predlog sprejel ali zavrnil.
  - Športnikovega cilja ne morem spremeniti sam, lahko ga samo predlagam.

## US-14 – Pregled športnikov

- **Povezana funkcionalnost:** 14 – Pregled vseh športnikov, ki so trenerju ali svetovalcu dali dostop, z zadnjo aktivnostjo
- **Uporabniška vloga:** trener ali prehranski svetovalec
- **Uporabniška zgodba:** Kot trener ali prehranski svetovalec želim na enem mestu videti vse športnike, ki so mi dali dostop, in njihovo zadnjo aktivnost, da hitro vidim, koga moram pregledati.
- **Acceptance criteria:**
  - Seznam »Moji športniki« prikaže vse športnike, ki so mi dali dostop, in vrsto dostopa (trener, prehranski svetovalec ali oboje).
  - Pri vsakem športniku sta datum in vrsta zadnjega vnosa, ki ga smem videti (npr. trener: »zadnji trening 18. 10.«).
  - Seznam lahko razvrstim po imenu ali po datumu zadnje aktivnosti.
  - Športnikov, ki so dostop preklicali, in povabil, ki jih še nisem sprejel, na seznamu ni.
  - Klik na športnika odpre njegove podatke, ki jih smem videti.

## US-15 – Urejanje vaj in mišic

- **Povezana funkcionalnost:** 15 – Urejanje seznama vaj in mišic
- **Uporabniška vloga:** administrator
- **Uporabniška zgodba:** Kot administrator želim urejati seznam vaj in mišic ter pri vsaki vaji določiti, katere mišice obremeni, da športniki izbirajo med pravilno opisanimi vajami in da se zemljevid mišic pravilno izračuna.
- **Acceptance criteria:**
  - Vajo dodam z imenom in opisom ter ji določim vsaj eno glavno mišico in poljubno število pomožnih mišic.
  - Mišico dodam z imenom in pogledom (spredaj ali zadaj).
  - Ko pri vaji spremenim mišice, zemljevid mišic vseh športnikov upošteva nove podatke, tudi za pretekle treninge.
  - Treningov, vnosa kalorij in vode, počutja ali teže uporabnikov ne vidim.
