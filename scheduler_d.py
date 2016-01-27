#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

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


def call_ansible():
    print('Tick! The time is: %s' % datetime.now())

    pb = './playbook.yml'
    i = './inventory.txt'

    pbe = PBExecutorWrapper(pb, i)
    pbe.run()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(call_ansible, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(60*60)
            print('main thread slept for an hour')

    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


