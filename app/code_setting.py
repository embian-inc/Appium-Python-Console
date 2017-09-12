#-*- coding: utf-8 -*-

import sys

class PS1LineCounter:
    def __init__(self):
        self.count = 0

    def __str__(self):
        self.count += 1
        return '[APC {:3d}] >> '.format(self.count)
        # return '\001\033[94m\002[APC {:3d}] >> \001\033[0m\002'.format(self.count)

class PS2LineCounter:
    def __str__(self):
        return '          .. '
        # return '\001\033[94m\002          .. \001\033[0m\002'
