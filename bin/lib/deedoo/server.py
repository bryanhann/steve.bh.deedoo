#!/usr/bin/env python3
import time
import sys
import datetime
from pathlib import Path

import deedoo.stoppers as SS
import deedoo.util as UTIL

ALARMS = []
DINGS = []

def poll_once(stop):
    SS.killed()
    assert stop
    if stop in ALARMS:
        return True
    if SS.found(stop):
        UTIL.say( f'stopped' )
        ALARMS.append(stop)
        return True
    return False

def poll(stop, seconds):
    slices = 10
    for _ in range(seconds*slices):
        if poll_once(stop):
            return True
        time.sleep(1.0/slices)

def run_server(DEBUG=False):
    SS.init()
    while True:
        SS.killed()
        now=Now(DEBUG)
        now.main()
        time.sleep(.5)

class Now:
    MISSES=20
    def __init__(self, DEBUG=False):
        dt = datetime.datetime.now()
        self.DEBUG=DEBUG
        self.dt = dt
        self.hh = dt.strftime("%H")
        self.mm = dt.strftime("%M")
        self.show = dt.strftime("%H%M")
        self._alarm_sleep = 5
        self._ding = self.dt.minute % 5 == 0
        self._alarm = self.dt.minute % 15 == 0

        if self.DEBUG:
            self.show = dt.strftime("%H%M%S")
            self._alarm_sleep=1
            self._ding = self.dt.second % 5 == 0
            self._alarm = self.dt.second % 15 == 0

        self.stop=UTIL.hash(self.show)
        self.stopfile = SS.file4stop(self.stop)


    def _phone(self):
        if self.mm=='00':
            return f"{self.hh} hundred"
        else:
            return f"{self.hh} {self.mm}"

    def main(self):
        if self.DEBUG:
            UTIL.errout(str(self)+'    ' +'\n')
        if self._ding:
            self.ding()
        if self._alarm:
            self.alarm()

    def ding(self):
        if not self.stop in DINGS:
            DINGS.append(self.stop)
            UTIL.say(f"The time is {self._phone()}")

    def alarm(self):
        seconds = self._alarm_sleep
        for count in range(self.MISSES, 0, -1):
            if poll(self.stop, seconds):
                return
            UTIL.say( f'deedoo {count}' )
        UTIL.say('giving up')
        exit()

    def __repr__(s):
        b = f"{s.stop=}"
        c = f"{s._ding=}"
        d = f"{s._alarm=}"
        t = s.dt.strftime('%H:%M:%S')
        return f"{t} {b} {c} {d}"




