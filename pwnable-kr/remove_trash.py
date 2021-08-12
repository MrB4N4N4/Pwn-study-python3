#!/usr/bin/env pyton

import os

def exec_bash(cmd):
    for c in cmd:
        os.system(c)

cmd = [
    "rm .gdb_history",
    "rm core",
    "rm peda*",
]
exec_bash(cmd)