# Events
Currently publishes market data events and trade events. Event classes are 
    
    MarketData
    TradeData 

# Strategies
Inherit the strategy class and annotate methods to subscribe to an event with

    class Printer(Strategy):    
        @Strategy.subscribe(EventType)
        def onEventTypeFunctionName(event: EventType):
            
            print(event)

And when an event is published ```onEventTypeFunctionName``` will be ran

