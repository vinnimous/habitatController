import relay

relay.setup()
while True:
    try:
        relay.DAYLIGHT()
    except:
        print ("Whoops, something went wrong")
