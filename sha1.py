# Sukimas kairėn (rotate left)
# x - sukamas skaičius, n - kiek pozicijų sukti
# Grąžina x pasukta n pozicijų kairėn (32 bitų ribose)
def rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

print(rol(1, 1))
print(rol(1, 2))
print(rol(8, 1))

# Pranešimo papildymas (padding)
# msg - originalus pranešimas kaip baitų seka
# Grąžina papildytą pranešimą, kurio ilgis 64 baitų kartotinis
def padding(msg):
    
    ilgis_bitais = len(msg) * 8 # originalus ilgis bitais
    
    msg += b'\x80' # pridedame 0x80 baitą (10000000 dvejetainiu)
    
    # pridedame nulinius baitus kol ilgis % 64 == 56
    # 56 nes paskutiniai 8 baitai skirti ilgiui saugoti
    while len(msg) % 64 != 56:
        msg += b'\x00'
    
    # pridedame originalų ilgį bitais kaip 8 baitų skaičių
    # to_bytes(8, 'big') = paverčia į 8 baitus, "big endian" tvarka
    msg += ilgis_bitais.to_bytes(8, 'big')
    
    return msg

rezultatas = padding(b"abc")
print(len(rezultatas))
print(rezultatas[0])
print(rezultatas[1])
print(rezultatas[2])

# Bloko padalijimas į 80 žodžių sąrašą
# blokas - 64 baitų bytes objektas
# Grąžina sąrašą 80 žodžių (32 bitų skaičių)
# Pirmieji 16 žodžių gaunami tiesiogiai iš bloko (4 baitai = 1 žodis)
# [b0][b1][b2][b3] -> žodis W[0]
# Žodžiai 16-79 gaunami išplečiant ankstesnius žodžius
def bloko_zodziai(blokas):
    W = []
    
    # Pirmieji 16 žodžių - tiesiog skaitome iš bloko
    for i in range(16):
        zodis = int.from_bytes(blokas[i*4 : i*4+4], 'big')
        W.append(zodis)
    
    # Žodžiai 16-79 - išplečiame
    for i in range(16, 80):
        W.append(rol(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1))
    
    return W

W = bloko_zodziai(padding(b"abc"))
print(len(W))
print(W[0])
