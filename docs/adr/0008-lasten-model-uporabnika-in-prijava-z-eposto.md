---
status: accepted
date: 2026-11-11
---

# Lasten model uporabnika in prijava z e-pošto

## Kontekst in problem

Uporabnik ima v podatkovnem modelu (`03-podatkovni-model.md`) ime, uporabniško ime, enolično e-pošto, geslo in sistemsko vlogo (UPORABNIK ali ADMIN). Prijava mora delovati z uporabniškim imenom ali z e-pošto, blokiran račun pa se ne sme prijaviti (US-01). Vgrajen Django uporabnik nima polja za ime v eni vrstici in ne zahteva enolične e-pošte. Odločiti se je bilo treba, kako se uporabnik shrani in kako se preveri prijava z e-pošto.

## Obravnavane možnosti

* Lasten model uporabnika na osnovi Djangovega uporabnika (`AbstractUser`) in dodaten način preverjanja prijave z e-pošto
* Vgrajen Django uporabnik in ločena tabela s profilom (ime), enoličnost e-pošte preverja samo obrazec

## Odločitev

Izbrana možnost: »Lasten model uporabnika na osnovi Djangovega uporabnika (`AbstractUser`) in dodaten način preverjanja prijave z e-pošto«, ker sta ime in enolična e-pošta tako v isti tabeli kot ostali podatki uporabnika, enoličnost pa preveri baza, pri e-pošti ne glede na velike in male črke (tudi za račune iz admina). Model je nastavljen pred prvo migracijo, ker ga Django kasneje težko zamenja. Polja iz podatkovnega modela so preslikana na obstoječa polja Djanga: uporabnisko_ime je `username`, geslo_hash je `password`, ustvarjen je `date_joined`, sistemska vloga ADMIN je `is_staff`, blokiran račun pa ima `is_active` nastavljen na ne. Prijavo z uporabniškim imenom preveri vgrajen Django način, prijavo z e-pošto pa dodaten način, ki tudi zavrne blokiran račun.

### Posledice

* Dobro, ker ni dodatne tabele in ni podvojenih polj za vlogo ali blokiran račun.
* Dobro, ker blokiran račun zavrneta oba načina prijave.
* Slabo, ker imajo nekatera polja v bazi Djangova imena (`username`, `password`, `date_joined`, `is_staff`) in ne imen iz podatkovnega modela.
* Slabo, ker mora biti model nastavljen pred prvo migracijo; kasnejša zamenjava bi zahtevala ročno prilagajanje baze.
