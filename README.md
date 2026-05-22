# Algoritmo informacija

Algoritmo pavadinimas: SHA-1 (Secure Hash Algorithm 1)
Programos varianto numeris: 14
Programavimo kalba: Python 3
Realizuotas variantas: Pilnas SHA-1 algoritmas pagal FIPS PUB 180-4 standartą

# Kas įgyvendinta

- Algoritmas įgyvendintas pilnai.
- Pranešimo papildymas (padding) pagal SHA-1 standartą: pridedamas 0x80 baitas, nuliniai baitai ir originalaus pranešimo ilgis bitais (8 baitai, big-endian tvarka).
- Bloko padalijimas į 80 žodžių sąrašą: pirmieji 16 žodžių skaitomi tiesiogiai iš bloko, žodžiai W[16]-W[79] gaunami išplečiant ankstesnius žodžius naudojant XOR ir sukimą kairėn (ROL).
- 32 bitų sukimas kairėn (ROL operacija).
- Pagrindinis kompresijos algoritmas su 80 raundų: naudojamos 4 skirtingos f funkcijos ir 4 konstantos K pagal raundo numerį (0-19, 20-39, 40-59, 60-79).
- Skaičiavimas dideliems failams (keli 64 baitų blokai).
- Failų skaitymas baitais.
- Rezultato išvedimas į ekraną šešioliktainiu formatu.
- Rezultato įrašymas į išvesties failą.
- Komandinės eilutės parametrų apdorojimas.
- Klaidų valdymas (nerastas failas, trūkstami parametrai).

# Kaip paleisti programą

Programą galima paleisti dviem būdais: naudojant Python interpretatorių arba tiesiogiai per sukompiliuotą failą (jei naudojate Linux)

## 1 Būdas: Naudojant Python (veikia visose operacinėse sistemose)
Šiam būdui reikalingas įdiegtas Python 3
- Paleidimas:
	- `python3 sha1.py <įvesties_failas> [išvesties_failas]`
- Parametrai:
	- `<įvesties_failas>` – failas, kurio SHA-1 maišą skaičiuojame (privalomas parametras)
	- `[išvesties_failas]` – failas, į kurį įrašyti rezultatą (neprivalomas parametras)
- Pavyzdžiai:
	- Išvesti tik į ekraną:  
		- `python3 sha1.py tekstas.txt`
	- Išvesti į ekraną ir į failą:  
		- `python3 sha1.py tekstas.txt rezultatas.txt`

## 2 Būdas: Naudojant sukompiliuotą failą (tik Linux/AMD64)

Aplanke esantis failas `sha1.bin` yra sukompiliuotas naudojant "Nuitka". Jis veikia tiesiogiai, be papildomo "Python" diegimo, tačiau yra skirtas tik 64-bitų Linux (`linux/amd64`) operacinėms sistemoms.

- Paleidimas:
	- `./sha1.bin <įvesties_failas> [išvesties_failas]`
- Parametrai:
	- `<įvesties_failas>` – failas, kurio SHA-1 maišą skaičiuojame (privalomas parametras)
	- `[išvesties_failas]` – failas, į kurį įrašyti rezultatą (neprivalomas parametras)
- Pavyzdžiai:
	- Išvesti tik į ekraną:
		- `⁠./sha1.bin tekstas.txt`
	- Išvesti į ekraną ir į failą:
		- `⁠./sha1.bin tekstas.txt rezultatas.txt`

# Iššūkiai
Sunku buvo suvokti 80 raundų kompresijos funkcijos logiką: kodėl kiekviename raunde naudojamos skirtingos f funkcijos (AND/OR/XOR kombinacijos), ir kokią prasmę turi kintamųjų pasislinkimas po kiekvieno raundo (e=d, d=c, c=rol(b,30) ir t.t.).
Taip pat reikėjo suprasti Python-specifinę bitų aritmetiką - Python skaičiai neturi dydžio ribos, todėl reikėjo nuolat maskuoti rezultatus su & 0xFFFFFFFF, kad išlaikytume 32 bitų ribą, kurios reikalauja SHA-1 standartas.

# Informacijos šaltiniai
1. Wikipedia - SHA-1 aprašymas ir algoritmo struktūra: https://en.wikipedia.org/wiki/SHA-1
2. NIST FIPS PUB 180-4 - oficiali SHA-1 specifikacija: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf