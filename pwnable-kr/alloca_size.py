from time import sleep

ebp_m = 0xffffd0d8
esp = ebp_m - 0x8
result = []

for size in range(-200, 0):
    print("[*] Trying: ", size)
    buf = size + 34
    buf = (buf//16) * 16
    buf = esp - buf
    buf = (buf+0xf) >> 4 << 4
    ebp_c = buf - 0x18
    print("buf: ", hex(buf))
    print("ebp_c: ", hex(ebp_c))

    if buf + size == ebp_m - 0x4:
        print("[+] Found: ", size)
        result.append(size)
    if ebp_c-0x14 == ebp_m - 0x4:
        print("[+] Found: ", size)
        result.append(size)
    if ebp_c-0x10 == ebp_m - 0x4:
        print("[+] Found: ", size)
        result.append(size)
    size -= 1
    sleep(0.1)
    print()

print(result)
