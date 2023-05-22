#!/usr/bin/env python3
from pathlib import Path
import os

STOPPERS=Path('/TMP/deedoo.stoppers')
KILL_PATH   = Path.home()/'die'
KILL_DEVICE = Path("/Volumes/SeagateBlue")


def create(stop):
    file4stop(stop).touch()

def found(stop):
    return file4stop(stop).exists()

def file4stop(stop):
    return STOPPERS/stop

def files():
    """return list of stopfiles"""
    return list( STOPPERS.glob("*") )


def init():
    if not STOPPERS.is_dir():
        STOPPERS.mkdir()
    for file in files():
        os.remove(file)
    if KILL_PATH.exists():
        print( "removing killpath" )
        os.remove(str(KILL_PATH))

def killed():
    if KILL_PATH.exists(): exit("SERVER KILLED")
    if not KILL_DEVICE.exists(): exit("SERVER KILLED")
    return False
