import sys

# Sukimas kairėn (rotate left)
# x - sukamas skaičius, n - kiek pozicijų sukti
# Grąžina x pasukta n pozicijų kairėn (32 bitų ribose)
def rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    # x << n stumia bitus kairėn, iš dešinės įpildo nulius
    # x >> (32 - n) stumia bitus dešinėn, kad gautume išbėgusius bitus
    # & 0xFFFFFFFF - išlaiko tik 32 bitus

# print(rol(1, 1))
# print(rol(1, 2))
# print(rol(8, 1))



# Pranešimo papildymas (padding)
# msg - originalus pranešimas kaip baitų seka
# Grąžina papildytą pranešimą, kurio ilgis 64 baitų kartotinis
def padding(msg):
    
    ilgis_bitais = len(msg) * 8 # Išsaugome originalų ilgį prieš bet kokį keitimą (baitus paverčiame į bitus)
    
    msg += b'\x80' # pridedame 0x80 baitą (10000000 dvejetainiu)
    # SHA-1 standarto reikalavimas - pažymime kur baigiasi tikras pranešimas ir prasideda padding
    
    # pridedame nulinius baitus kol ilgis % 64 == 56
    # 56 nes paskutiniai 8 baitai skirti ilgiui saugoti
    while len(msg) % 64 != 56:
        msg += b'\x00'
    
    # pridedame originalų ilgį bitais kaip 8 baitų skaičių
    # to_bytes(8, 'big') = paverčia į 8 baitus, "big endian" tvarka
    msg += ilgis_bitais.to_bytes(8, 'big')
    
    return msg

# rezultatas = padding(b"abc")
# print(len(rezultatas))
# print(rezultatas[0])
# print(rezultatas[1])
# print(rezultatas[2])



# Bloko padalijimas į 80 žodžių sąrašą
# 64 baitų blokas padalijamas į 16 žodžių, o vėliau išplečiamas iki 80 žodžių
# 1 žodis = 4 baitai = 32 bitai
# Grąžina sąrašą 80 žodžių
# Pirmieji 16 žodžių gaunami tiesiogiai iš bloko (4 baitai = 1 žodis)
# [b0][b1][b2][b3] -> žodis W[0]
# Žodžiai 16-79 gaunami išplečiant ankstesnius žodžius
def bloko_zodziai(blokas):
    W = [] # tuščias sąrašas kuriame kaupsime 80 žodžių
    
    # Turime 64 baitų bloką. Pjaustome jį į 16 gabalų po 4 baitus, ir kiekvieną gabalą paverčiame į vieną 32 bitų skaičių
    # Pirmieji 16 žodžių - tiesiog skaitome iš bloko
    for i in range(16):
        zodis = int.from_bytes(blokas[i*4 : i*4+4], 'big') # 4 baitus paverčia į vieną 32 bitų skaičių
        W.append(zodis)
    
    # Žodžiai 16-79 - Kiekvieną naują žodį gauname iš 4 ankstesnių žodžių - juos XOR'iname ir pasukame kairėn 1 bitu
    for i in range(16, 80):
        W.append(rol(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1))
    
    return W

# W = bloko_zodziai(padding(b"abc"))
# print(len(W))
# print(W[0])



# Vieno 64 baitų bloko apdorojimas
# h - sąrašas [H0, H1, H2, H3, H4] - dabartinės maišos reikšmės
# Grąžina atnaujintą sąrašą
def apdoroti_bloka(blokas, h):
    W = bloko_zodziai(blokas)
    
    # Nukopijuojame dabartines H reikšmes į laikinius kintamuosius
    # originalios h reikšmės turi išlikti nepakitusios, nes pabaigoje prie jų pridėsime rezultatą, a,b,c,d,e nuolat keisis per raundus
    a, b, c, d, e = h[0], h[1], h[2], h[3], h[4]
    
    for i in range(80):
        # Parenkame f ir K pagal raundo numerį
        if i <= 19: # 0-19
            f = (b & c) | ((~b) & d) # Jei b bitas = 1 - imame iš c, jei b bitas = 0 - imame iš d (choice funkcija)
            K = 0x5A827999
        elif i <= 39: # 20-39
            f = b ^ c ^ d # XOR visi trys vienodai svarbūs (parity funkcija)
            K = 0x6ED9EBA1
        elif i <= 59: # 40-59
            f = (b & c) | (b & d) | (c & d) # bent du iš trijų turi sutapti (majority funkcija)
            K = 0x8F1BBCDC
        else: # 60-79
            f = b ^ c ^ d # vėl XOR kaip ir 20-39 raunde (parity funkcija)
            K = 0xCA62C1D6
        
        # Skaičiuojame naują reikšmę, & 0xFFFFFFFF - išlaikome 32 bitus
        temp = (rol(a, 5) + f + e + K + W[i]) & 0xFFFFFFFF
        
        # Paslenkame kintamuosius
        e = d
        d = c
        c = rol(b, 30)
        b = a
        a = temp
    
    # Pridedame prie pradinių reikšmių
    return [
        (h[0] + a) & 0xFFFFFFFF,
        (h[1] + b) & 0xFFFFFFFF,
        (h[2] + c) & 0xFFFFFFFF,
        (h[3] + d) & 0xFFFFFFFF,
        (h[4] + e) & 0xFFFFFFFF,
    ]

# Pagrindinė SHA-1 funkcija
# pranesimas - baitų seka (bytes)
# Grąžina SHA-1 maišos reikšmę kaip hex eilutę (40 simbolių)
def sha1(pranesimas):
    # Pradinės SHA-1 konstantos
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    
    # Padding, pranešimas papildomas iki 64 baitų kartotinio
    paddintas = padding(pranesimas)
    
    # Apdorojame kiekvieną 64 baitų bloką
    for i in range(0, len(paddintas), 64):
        blokas = paddintas[i : i+64]
        h = apdoroti_bloka(blokas, h) # Kiekvieno bloko rezultatas h perduodamas į kitą bloką
    
    # Sujungiam 5 žodžius į vieną hex eilutę
    return ''.join(f'{x:08x}' for x in h)

# print(sha1(b"abc"))
# print(sha1(b""))
# print(sha1(b"Labas pasauli"))



# Programa paleidžiama iš komandinės eilutės
# Naudojimas: python3 sha1.py <įvesties_failas> [išvesties_failas]
# įvesties_failas - failas kurio maišą skaičiuojame (privalomas)
# išvesties_failas - failas į kurį rašome rezultatą (neprivalomas)
def main():
    # Tikriname ar nurodytas bent įvesties failas
    if len(sys.argv) < 2:
        print("")
        print("Klaida: nenurodytas įvesties failas")
        print("")
        print("Naudojimas:")
        print("Jeigu per Python interpretatorių:")
        print("     python3 sha1.py <įvesties_failas> [išvesties_failas]")
        print("     Pavyzdys: python3 sha1.py tekstas.txt rezultatas.txt")
        print("Jeigu per vykdomąjį failą:")
        print("     ./sha1.bin <įvesties_failas> [išvesties_failas]")
        print("     Pavyzdys: ./sha1.bin tekstas.txt rezultatas.txt")
        return
    
    ivesties_failas = sys.argv[1]
    
    # Bandome atidaryti ir perskaityti failą baitais
    try:
        with open(ivesties_failas, 'rb') as f:
            duomenys = f.read()
    except FileNotFoundError:
        print(f"Klaida: failas '{ivesties_failas}' nerastas.")
        return
    except Exception as e:
        print(f"Klaida skaitant failą: {e}")
        return
    
    # Skaičiuojame maišą
    maisas = sha1(duomenys)
    print(f"SHA-1({ivesties_failas}) = {maisas}")
    # Atkomentuoti jei norite matyti maišą didžiosiomis raidėmis:
    # print(f"SHA-1({ivesties_failas}) = {maisas.upper()}")
    
    # Jei nurodytas išvesties failas - įrašome rezultatą
    if len(sys.argv) >= 3:
        isvesties_failas = sys.argv[2]
        try:
            with open(isvesties_failas, 'w') as f:
                f.write(maisas + '\n')
            print(f"Rezultatas taip pat įrašytas į '{isvesties_failas}'")
        except Exception as e:
            print(f"Klaida rašant į failą: {e}")
            return

main()

# main() -> nuskaito failą baitais -> sha1() -> padding() -> apdoroti_bloka() -> bloko_zodziai() -> rol() -> grąžina maišos reikšmę -> išveda rezultatą į ekraną ir į failą
