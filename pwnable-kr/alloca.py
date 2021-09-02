from pwn import *

"""Bugs & Ideas
[Protections]
 - partial RELRO, NX
[Info]
 - base_esp : ebp-0x8
 - size : (input + 0x4 + 0xf + 0xf) // 0xf * 0x10
[Bug]
 - buffer size input : not filtering negative number
[Address]
 - buffer_add : 0x804a050 > stack
 - buffer_size : 0x804a048
 - callme : 0x80485ab
 - g_canary : 0x804a04c
 - canary(nagative) : buffer(esp-0x10*n - input), n = input + 0x4 + 0xf + 0xf / 0xf * 0x10
 
[Exploit]
 ?? awesome negative integer of size might input my canary(callme) in to stack.
"""