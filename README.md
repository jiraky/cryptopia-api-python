# Authors
## Cryptopia python API by CC Tech
* The Bot Guy (thebotguy@protonmail.com)
* @jiraky90
* @rutrus

## Overview
This wrapper provides a friendly way to call Cryptopia API from a Python 2.7 script.
Requires requests 2.8.1

## Usage
Just import it and use it.
``` python
from cryptopia_api import Api

#later...
api_wrapper = Api(MY_PUBLIC_KEY, MY_SECRET_KEY)

#call a request to the api, like balance in BTC...
balance, error = api_wrapper.get_balance('BTC')
if error is not None:
    #handle error
    print 'ERROR: %s' % error
else:
    #ok
    print 'Request successfull. Balance in BTC = %f' % balance
```

Check cryptopia API docs for the parameters of each call: a more detailed wiki will be added here soon!
