#!/usr/bin/env python

import requests as r
import hashlib

import asyncio
import websockets


secret = "6a14dfa700ec440f9fd10fa58753a23a"

def signContext(context: str):
    return hashlib.sha512(secret).update(context))

def authenticate(uri):
    challenge = r.get("https://socket/bittrex.com/signalr?apiKey=e729d9ce8b2b4b3a92140e560df550f2")
    context = challenge.text()
    sig = signContext(context)






asyncio.get_event_loop().run_until_complete(
        authenticate('https://'))


