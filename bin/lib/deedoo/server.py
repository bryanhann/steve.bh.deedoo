#!/usr/bin/env python3
import time
import sys
import datetime
from pathlib import Path

import deedoo.stoppers as SS
import deedoo.util as UTIL

ALARM_LIST = []
DING_LIST = []

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
        self.hhmm = dt.strftime("%H%M")
        self.hhmmss = dt.strftime("%H%M%S")
        self.hour = dt.hour
        self.minute = dt.minute
        self.second = dt.second
        self.show = self.hhmm
        self.alarm_sleep = 5
        self._ding = self.dt.minute % 5 == 0
        self._alarm = self.dt.minute % 15 == 0

        if self.DEBUG:
            self.show=self.hhmmss
            self.alarm_sleep=1
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
        self.debug_report()
        self.ding()
        self.alarm()

    def ding(self):
        if not self._ding:
            return
        if self.stop in DING_LIST:
            return
        DING_LIST.append(self.stop)
        UTIL.say(f"The time is {self._phone()}")

    def alarm(self):
        if not self._alarm:
            return
        if self.stop in ALARM_LIST:
            return
        ALARM_LIST.append(self.stop)
        for count in range(self.MISSES, 0, -1):
            if SS.killed():
                return
            if SS.found(self.stop):
                UTIL.say( f'stopped' )
                return
            UTIL.say( str(count) )
            UTIL.sayspell(self.stop)
            time.sleep(self.alarm_sleep)

    def __repr__(s):
        b = f"{s.stop=}"
        c = f"{s._ding=}"
        d = f"{s._alarm=}"
        t = s.dt.strftime('%H:%M:%S')
        return f"{t} {b} {c} {d}"

    def debug_report(self):
        if self.DEBUG:
            UTIL.errout(str(self)+'    ')
