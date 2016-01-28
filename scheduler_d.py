#!/usr/bin/env python
__author__ = 'Samuel Flores'

if __name__ == '__main__':
    # explicitly append the ./src directory to the current path.
    # PyCharm does this implicitly but it is better to have it explicit
    # this makes the tool work the same in tests and in CLI
    import sys
    import inspect
    from os.path import dirname, join, realpath
    # when in CLI use inspect to locate the source directory
    src_dir = join(dirname(realpath(inspect.getfile(inspect.currentframe()))), 'src')
    sys.path.append(src_dir)

from pbwrapper import PBExecutorWrapper

pb = './playbook.yml'
i = './inventory.txt'

pbe = PBExecutorWrapper(pb, i)
pbe.run()

