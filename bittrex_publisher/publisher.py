#!/usr/bin/python
# /examples/ticker_updates.py

# Sample script showing how subscribe_to_exchange_deltas() works.

# Overview:
# ---------
# 1) Creates a custom ticker_updates_container dict.
# 2) Subscribes to N tickers and starts receiving market data.
# 3) When information is received, checks if the ticker is
#    in ticker_updates_container and adds it if not.
# 4) Disconnects when it has data information for each ticker.

import sys
from bittrex_websocket.websocket_client import BittrexSocket
from time import sleep
import json


key = "e729d9ce8b2b4b3a92140e560df550f2"
secret = "6a14dfa700ec440f9fd10fa58753a23a"

def main():
    class MySocket(BittrexSocket):

        async def on_public(self, msg):
            #name = msg['M']
            tickers = ['BTC-USD']
            data = map(lambda item: {item.get("M"): item}, list(filter(lambda item: item.get('M') in tickers, msg.get('D'))))
            sys.stdout.write("\n".join([f'\r Price delta: {data.get(exchange).get("PD")} exchange: {exchange} base volume: {data.get(exchange).get("m")}' for exchange in ticker_updates_container]))
            sys.stdout.flush()
            #if name not in ticker_updates_container:
            #    ticker_updates_container[name] = msg
            #    print(json.dumps(msg))

    # Create container
    ticker_updates_container = {}
    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log()
    # Define tickers
    tickers = ['USD-BTC']
    # Subscribe to ticker information
    ws.authenticate(key, secret)
    for ticker in tickers:
        sleep(0.01)
#        ws.subscribe_to_exchange_deltas([ticker])
        ws.subscribe_to_summary_lite_deltas()

    # Users can also subscribe without introducing delays during invoking but
    # it is the recommended way when you are subscribing to a large list of tickers.
    # ws.subscribe_to_exchange_deltas(tickers)

    while True:
        sleep(0.1)
if __name__ == "__main__":
    main()
