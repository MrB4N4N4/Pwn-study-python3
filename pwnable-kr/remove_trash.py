#!/usr/bin/env pyton
import os


def exec_bash(cmd):
    for c in cmd:
        try:
            os.system(c)
        except e:
            pass


command = [
    "rm .gdb_history",
    "rm core",
    "rm peda*",
]
exec_bash(command)
