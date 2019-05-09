#! /usr/bin/env python

'''
Starts the game and gets all parts running in a way that they can interact
'''

import sys

from engine import begin


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
    begin(**kwargs)

if __name__ == "__main__":
    main()