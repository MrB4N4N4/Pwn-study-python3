from pwn import *

"""
0x31337 >> hacker menu
[Protections]
-NX, Partial RELRO
[Bug]
    mem_arr[256] - always empty
    write_note.gets() - over flow
    select_menu > recursive > pile stack infinitely
    
    ToDo
    leak stack
    
[Address]

[Exploit]
"""

p = process("/root/Downloads/note")
#p = remote("pwnable.kr", 9019)


