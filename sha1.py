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
