#! /usr/bin/python3
import configparser
import logging
import os

config = dict()
parser = None

def _create(configfile):
    with open(configfile,"w+") as _:
        pass

def _save(configfile = "trading.conf"):
    with open(configfile, 'w+') as conf:
        parser.write(conf)
        return True
    return False

def _readConfig(configfile = "trading.conf"):
    global config
    global parser
    config['CONF_FILE'] = os.path.join(os.path.dirname(__file__),configfile)
    parser = configparser.ConfigParser(allow_no_value=True)
    createFile = not os.path.isfile(config['CONF_FILE'])
    if createFile:
        _create(config['CONF_FILE'])
        set_values(configparser.DEFAULTSECT, 'public_key', None)
        set_values(configparser.DEFAULTSECT, 'private_key', None)
        set_values(configparser.DEFAULTSECT, 'watch_pairs', None)
    parser.read(config['CONF_FILE'])
    return parser

def set_values(exchange,key,value):
    try:
        if parser is None:
            read(exchange)
        parser.set(exchange,key,value)
        return _save()
    except:
        # Maybe is good idea a logger
        return False

def get_values(exchange,key):
    if parser is None:
        _readConfig(exchange)
    try:
        value = parser.get(exchange,key)
        return value
    except:
        return False
    
def read(exchange = ''):
    """ Easy human-readable configuration """
    global config
    global parser
    if not parser:
        parser = _readConfig()
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
