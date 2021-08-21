g_pbuf = []
g_ebuf = []

# a1 == plain character
#
for i in renage(1024):
    encrypt(g_pbuf[i], pub)

def encrypt(a1, *e):
    return mod_exp(a1, e, pq)

def mod_exp(a1, e, pq):
    v6 = 1
    while(e):
        v7 = e & 1 # v7 == 1 or 0
        e >>= 1
        if (v7 == 1):
            v6 = a1 * v6 % pq
        a1 = a1*a1 % pq
    return v6