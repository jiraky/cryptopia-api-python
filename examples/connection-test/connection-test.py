#! /usr/bin/python2
# -*- coding: utf-8 -*-
from cryptopia_api import Api
import configparser
import os

def readConfig(exchange = ''):
    """ Easy human-readable configuration """
    global config
    save = False
    config={}
    config['CONF_FILE'] = os.path.join(os.path.dirname(__file__),'trading.conf')
    parser = configparser.ConfigParser(allow_no_value=True)
    # These avoid error if not exists in conf
    parser.set(configparser.DEFAULTSECT, 'public_key', None)
    parser.set(configparser.DEFAULTSECT, 'private_key', None)
    parser.read(config['CONF_FILE'])
    if not parser.has_section(exchange):
        parser.add_section(exchange)
        save = (raw_input("Save? Y/N").lower() == 'y') or True # always save
        #if not config[exchange][0]:
        key0 = raw_input("Insert PUBLIC API KEY for exchange "+exchange+" ")
        key1 = raw_input("Insert PRIVATE API KEYfor exchange "+exchange+" ")
        parser.set(exchange,'public_key', key0)
        parser.set(exchange,'private_key', key1)
    if save:
        with open(config['CONF_FILE'], 'w+') as conf:
            parser.write(conf)
    config[exchange] = (parser.get(exchange,'public_key'),parser.get(exchange,'private_key'))
    return config

exchange = "cryptopia"
config = readConfig(exchange)
cryptopia = Api(*config[exchange])

#call a request to the api, like balance in BTC...
balance, error = cryptopia.get_balance('CREA')
if error:
    print ('ERROR: %s' % error)
else:
    print ('Request successful. My Balance: {}'.format(balance))
