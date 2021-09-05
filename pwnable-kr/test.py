from pwn import *
from time import sleep
#(((esp-((((size+34)//16)*16) & 0xffffffff))+0xf)>>4<<4&0xffffffff) == ebp+0x8

ebp = 0xffffd0d8
esp = ebp - 0x8
size = 0
target = [ebp + 8, ebp-4, ebp+4]

while True:
    print("[*] Trying: ", size)
    buf = size + 34
    buf = (buf//16) * 16
    buf = esp - buf
    buf = (buf+0xf) >> 4 << 4
    if buf+size == target[1]:
        print("[+] Found: ", size)
        break
    size -= 1
    sleep(0.1)

