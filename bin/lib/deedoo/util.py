import hashlib
import sys
import os
def sayspell(text):
    aa = ''.join( f"{ch}. " for ch in text )
    say(aa)
def say(text):
    os.system(f'say {text}')
def hash(text):
    a=hashlib.md5()
    a.update(text.encode())
    return a.hexdigest()[:4]

def errout(text):
    back = '\b'*(len(text)+10)
    sys.stderr.write(text + back)
    sys.stderr.flush()

