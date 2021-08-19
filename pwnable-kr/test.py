from pwn import *

r = remote("pwnable.kr", 9011)

"""
Exploit echo2 succeed in local.
Apply it remote environment!!
First I need to test FSB-64bit using "%1$lx"
"""

