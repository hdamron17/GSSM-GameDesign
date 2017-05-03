#! /usr/bin/env python

'''
Starts the game and gets all parts running in a way that they can interact
'''

import sys
from os.path import join as pathjoin, abspath, dirname, normpath

import engine


PROJECT_ROOT = normpath(pathjoin(dirname(abspath(sys.argv[0])), ".."))

def get_args():
    kwargs = {}
    for arg in sys.argv[1:]:
        split = arg.split("=", maxsplit=1)
        if len(split) > 1:
            key, value = split
            kwargs[key] = value
    return kwargs

def main():
    kwargs = get_args()
    engine.begin(**kwargs)

if __name__ == "__main__":
    main()