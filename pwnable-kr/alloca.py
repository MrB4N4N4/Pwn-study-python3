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

