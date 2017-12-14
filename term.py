#!/bin/env python

import fcntl
import termios
import sys
import os


class Term:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(self.fd)
        self.newattr = termios.tcgetattr(self.fd)
        self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO

    def _open(self):
        termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def _close(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def get(self):
        try:
            self._open()
            ret = []
            c = None
            cc = []
            while not cc or c:
                try:
                    c = sys.stdin.read(1)
                    if c:
                        cc.append(c)
                except IOError: pass
            return ''.join(cc)
        finally:
            self._close()
