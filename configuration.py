#! /usr/bin/python3
from cryptopia_api import Api
import configparser
import logging
import os

config = dict()
parser = None

def _create(configfile):
    with open(configfile,"w+") as _:
        pass

def _save(configfile):
    with open(configfile, 'w+') as conf:
        parser.write(conf)
        return True
    return False

def set_values(exchange,key,value):
    try:
        if parser is None:
            parser = read(exchange)
        parser.set(exchange,key,value)
        return True
    except:
        # Maybe is good idea a logger
        return False

def get_values(exchange,key):
    while (parser is None):
        readConfig(exchange)
    try:
        value = parser.get(exchange,key)
        return value
    except:
        return False

def readConfig(configfile = "trading.conf"):
    global config
    global readed
    config['CONF_FILE'] = os.path.join(os.path.dirname(__file__),configfile)
    createFile = not os.path.isfile(config['CONF_FILE'])
    parser = configparser.ConfigParser(allow_no_value=True)
    if createFile:
        _create(config['CONF_FILE'])
        set_values(configparser.DEFAULTSECT, 'public_key', None)
        set_values(configparser.DEFAULTSECT, 'private_key', None)
        set_values(configparser.DEFAULTSECT, 'watch_pairs', None)
    parser.read(config['CONF_FILE'])
    readed = True
    return parser

def read(exchange = ''):
    """ Easy human-readable configuration """
    global config
    global parser
    if not parser:
        parser = readConfig()
    if not parser.has_section(exchange):
        parser.add_section(exchange)
        print("You entered a New exchange.")
        #if not config[exchange][0]:
        key0 = input("Insert PUBLIC API KEY for exchange "+exchange+" ")
        key1 = input("Insert PRIVATE API KEYfor exchange "+exchange+" ")
        set_values(exchange,'public_key', key0)
        set_values(exchange,'private_key', key1)

    config[exchange] = dict(parser[exchange])
    return config

if __name__ == "__main__":
    # Testing
    config = read("nuevo exchange")
    print(get_values("cryptopia","public_key"))
    #cryptopia = Api(*config[exchange])
