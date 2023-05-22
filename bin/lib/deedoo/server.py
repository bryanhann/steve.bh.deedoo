#!/usr/bin/env python3
import time
import sys
import datetime
from pathlib import Path

import deedoo.stoppers as SS
import deedoo.util as UTIL

ALARM_LIST = []
ANNOUNCE_LIST = []

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
        self.f_announce = self.dt.minute % 5 == 0
        self.f_alarm = self.dt.minute % 15 == 0

        if self.DEBUG:
            self.show=self.hhmmss
            self.alarm_sleep=1
            self.f_announce = self.dt.second % 5 == 0
            self.f_alarm = self.dt.second % 15 == 0

        self.stop=UTIL.hash(self.show)
        self.stopfile = SS.file4stop(self.stop)


    def _phone(self):
        if self.mm=='00':
            return f"{self.hh} hundred"
        else:
            return f"{self.hh} {self.mm}"

    def main(self):
        self.debug_report()
        self.announce()
        self.alarm()

    def announce(self):
        if not self.f_announce:
            return
        if self.stop in ANNOUNCE_LIST:
            return
        ANNOUNCE_LIST.append(self.stop)
        UTIL.say(f"The time is {self._phone()}")

    def alarm(self):
        if not self.f_alarm:
            return
        if self.stop in ALARM_LIST:
            return
        ALARM_LIST.append(self.stop)
        for count in range(self.MISSES, 0, -1):
            if SS.killed():
                return
            if SS.found(self.stop):
                return
            UTIL.say( str(count) )
            UTIL.sayspell(self.stop)
            time.sleep(self.alarm_sleep)

    def debug_report(self):
        if not self.DEBUG:
            return
        a = self.hhmmss
        b = self.stop
        c = self.f_announce
        d = self.f_alarm
        e = str(self.stopfile)
        UTIL.errout( f"{a} {b} {c} {d} {e}" )

