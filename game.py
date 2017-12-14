#!/bin/env python

"""
+----+----+----+----+
|  1 |  2 |  3 |  4 |
+----+----+----+----+
|  5 |  6 |  7 |  8 |
+----+----+----+----+
|  9 | 10 | 11 | 12 |
+----+----+----+----+
| 13 | 14 | 15 |    |
+----+----+----+----+
"""

import random
from functools import reduce
from term import Term

EX  = list(range(1, 16))
EX.append('')

def load():
    rdms = []
    while len(rdms) < 15:
        n = str(random.randint(1, 15))
        if n not in rdms:
            rdms.append(n)
    rdms.append("")
    rdms = [rdms[ns*4:(ns+1)*4] for ns in range(4)]
    return rdms

def clean():
    print(chr(27) + "[2J")

def paint(r):
    clean()
    line = "+----+----+----+----+"
    print(line)
    for rl in r:
        print("| %s |" % (" | ".join([d.rjust(2) for d in rl])))
        print(line)

def validate(r):
    rr = [ n and int(n) for n in reduce(lambda x,y: x+y, r) ]
    return rr == EX

def main():
    l = load()
    t = Term()
    x, y = 3, 3
    
    pos = {
        '\x1b[A': (+1, 0), # up
        '\x1b[B': (-1, 0), # down
        '\x1b[C': (0, -1), # right
        '\x1b[D': (0, +1), # left
    }

    playing = True

    while playing:
        paint(l)
        k = t.get()
        m = pos.get(k)
        if not m:
            continue

        xx, yy = m
        xx += x
        yy += y
        if xx < 0 or xx > 3 or yy < 0 or yy > 3:
            continue

        l[x][y] = l[xx][yy]
        l[xx][yy] = ''
        x, y = xx, yy

        playing = not validate(l)

    paint(l)
    print("You Win!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Game over")