#!/usr/bin/python3

"""
Crypto Crew Technologies (thebotguy@usa.com)

Disclaimer: This does not guarantee profit and you can still lose money if your
sell order does not fill. (A sell order set too high may not be filled)

It is all dependent on the volume of the pump and how much you are intending to liquidate.
Build up your profits gradually and do not be too greedy, else you can be caught holding
the bag. Do proper preparation to know how much to use and where to set your buy/sell at!

This program is for educational use only and is provided AS IS. Check the LICENSE file of this repository.
"""

import json
import signal
import sys
import time
from cryptopia_api import Api

# Get these from (link here)
def get_secret(secret_file):
    """Grabs API key and secret from file and returns them"""

    with open(secret_file) as secrets:
        secrets_json = json.load(secrets)
        secrets.close()

    return str(secrets_json['key']), str(secrets_json['secret'])

def sigint_handler():
    """Handler for ctrl+c"""
    print ('\n[!] CTRL+C pressed. Exiting...')
    sys.exit(0)

EXIT_CYCLE = False
while not EXIT_CYCLE:

    # setup api
    KEY, SECRET = get_secret("secrets.json")
    API = Api(KEY, SECRET)

    # do before entering coin to save the API call during the pump
    BALANCE_BTC, ERROR = API.get_balance('BTC')
    if ERROR is not None:
        print (ERROR)
        break
    AVAILABLE_BTC = BALANCE_BTC['Available']

    signal.signal(signal.SIGINT, sigint_handler)
    print ('Crypto Crew Technologies Welcomes you to our Pump Trade Bot!\n')
    print ('Buy and Sell orders will be instantly placed on Cryptopia at \
           a specified % above the ASK price.\n')

    TRAINING = input("   Live Mode (1) = Real orders will be placed.'\n\
                         Training Mode (2) = No real orders will be placed.\n\n\
                         Enter 1 for Live Mode or 2 for Training Mode - (1 or 2) ?: ")
    ALLOW_ORDERS = False # Set to True to enable limit trading...
    if TRAINING == "2":
        ALLOW_ORDERS = False
        print ('\nTraining Mode Active! No real orders will be placed.\n')
        print ('Press CTRL+C to exit at anytime.\n')
    elif TRAINING == "1":
        ALLOW_ORDERS = True
        print ('\nLive Mode Active! Real orders will be placed.\n\n\
               Press CTRL+C to exit at anytime.\n')
    print ('You have {} BTC available.'.format(AVAILABLE_BTC))
    PUMP_BALANCE = float(input("How much BTC would you like to use?: "))
    while PUMP_BALANCE > AVAILABLE_BTC:
        print ('You can\'t invest more than {}'.format(AVAILABLE_BTC))
        PUMP_BALANCE = float(input("How much BTC would you like to use?: "))

    PUMP_BUY = float(input("\nBuy Above Current Ask by what %: "))
    PUMP_SELL = float(input("Sell Above Current Ask by what %: "))
    print ('\n*Orders will send immediately after entering coin ticker symbol. \
           Assure accuracy!\nType in one case only, i.e. XVG or xvg, not Xvg\n')
    PUMP_COIN = input("Coin Ticker Symbol: ")

    COIN_PRICE, ERROR = API.get_market(PUMP_COIN + "_BTC")
    if ERROR is not None:
        print (ERROR)
        break
    ASK_PRICE = COIN_PRICE['AskPrice']

    COIN_SUMMARY, ERROR = API.get_market(PUMP_COIN + "_BTC")
    if ERROR is not None:
        print (ERROR)
        break
    LAST_PRICE = COIN_SUMMARY['LastPrice']
    CLOSE_PRICE = COIN_SUMMARY['Close']

    if LAST_PRICE > CLOSE_PRICE + 0.20 * CLOSE_PRICE:
        print ('\nYou joined too late or this was pre-pumped! \
               Close Price : {:.8f} . Last Price : {:.8f}'.format(CLOSE_PRICE, LAST_PRICE))
        LATE = input("Still want to continue? (y/n): ")
        if LATE == "y" or LATE == "yes":
            print ('\nYou joined this pump despite warning, good luck!')
        else:
            print ('\nOk! Trade has been exited. No order placed.')
            break
    else:
        print ('\nEntry point acceptable!')

    ASK_BUY = ASK_PRICE + (PUMP_BUY/100 * ASK_PRICE)
    ASK_SELL = ASK_PRICE + (PUMP_SELL/100 * ASK_PRICE)

    print ('\nUsing {:.8f} BTC to buy {} .'.format(PUMP_BALANCE, PUMP_COIN))
    print ('Current ASK price for {} is {:.8f} BTC.'.format(PUMP_COIN, ASK_PRICE))
    print ('\nASK + {}% (your specified buy point) for {} is {:.8f} \
           BTC.'.format(PUMP_BUY, PUMP_COIN, ASK_BUY))
    print ('ASK + {}% (your specified sell point) for {} is {:.8f} \
           BTC.'.format(PUMP_SELL, PUMP_COIN, ASK_SELL))


    # calculates the number of PUMP_COIN(s) to buy, taking into
    # consideration Cryptopia's 0.20% fee.
    NUM_COINS = (PUMP_BALANCE - (PUMP_BALANCE*0.00201)) / ASK_BUY

    BUY_PRICE = ASK_BUY * NUM_COINS
    SELL_PRICE = ASK_SELL * NUM_COINS
    PROFIT = SELL_PRICE - BUY_PRICE

    print ('\n[+] Buy order placed for {:.8f} {} coins at {:.8f} BTC \
           each for a total of {} BTC'.format(NUM_COINS, PUMP_COIN, ASK_BUY, BUY_PRICE))

    if ALLOW_ORDERS:
        # For security, this is a simulator:
        #TRADE, ERROR = API.submit_trade(PUMP_COIN + '/BTC', 'Buy', ASK_BUY, NUM_COINS)
        ERROR = PUMP_COIN + '/BTC', 'Buy', ASK_BUY, NUM_COINS
        if ERROR is not None:
            print (ERROR)
            break
        print (TRADE)
    else:
        print ("[!] Training Mode Active. No real orders are being placed.")

    print ('\n[+] Placing sell order at {:.8f} (+{}%)...'.format(ASK_SELL, PUMP_SELL))

    if ALLOW_ORDERS:
        COINS_OWNED, ERROR = API.get_balance(PUMP_COIN)[0]['Available']
        if ERROR is not None:
            print (ERROR)
            break
        while COINS_OWNED == 0:
            time.sleep(0.1)
            COINS_OWNED, ERROR = API.get_balance(PUMP_COIN)[0]['Available']
            if ERROR is not None:
                print (ERROR)
                break
        # This is very dangerous
        # TRADE, ERROR = API.submit_trade(PUMP_COIN + '/BTC', 'Sell', ASK_SELL, NUM_COINS)
        ERROR = PUMP_COIN + '/BTC', 'Sell', ASK_SELL, NUM_COINS
        if ERROR is not None:
            print (ERROR)
            break
    else:
        print ("[!] Training Mode Active. No real orders are being placed.")

    print ('\n[+] Sell order placed of {:.8f} {} coins at {:.8f} BTC each for \
          a total of {:.8f} BTC'.format(NUM_COINS, PUMP_COIN, ASK_SELL, SELL_PRICE))

    print ('[*] PROFIT if sell order fills: {:.8f} BTC'.format(PROFIT))

    print ('\nCheck Cryptopia to assure order has been filled!\n')
    print ('Adjust your order manually in Cryptopia if you observe the pump \
          is weak and did not reach your sell limit.')

    print ('\nBrought To You By Crypto Crew Technologies - Happy Profits!')


    if __name__ == "__main__":
        ANSWER = input("\nWould you like to restart the {} Trade Bot? (y/n) ").format(PUMP_COIN)
        if ANSWER.lower().strip() in "n no".split():
            EXIT_CYCLE = True
