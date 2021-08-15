from pwn import *

"""
Exploit plan
<buglist>
    select menu input> -1, 0

<set_key>
    p(v6) # 16
    q(v7) # 16
    pub[] 
    v4 = p * q > 255 ( 2 ^ 8) # 256
    v5 = (p - 1) * (q - 1) # 225
    v1(e)  # 226
    v2(d)  # 1
    
    _condition_
    v1 < v5     &&
    v2 < v5     &&
    e * d % v5 != 1
    
    RSA_rbp = 0x7fffffffdf00
"""

p = process("/root/Downloads/rsa_calculator")


