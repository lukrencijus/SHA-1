def rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

print(rol(1, 1))
print(rol(1, 2))
print(rol(8, 1))
