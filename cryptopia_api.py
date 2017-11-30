#! /usr/bin/python3
""" This is a wrapper for Cryptopia.co.nz API """

# TODO
# - Log all actions
# - Timer connections

import requests
import hashlib
import urllib
import urllib.parse
import base64
import hmac
#import logging
import json
import time
import re
from collections import OrderedDict
import configuration

__version__ = "20171130"

class Api(object):
    """ Represents a wrapper for cryptopia API """

    def __init__(self, key = None, secret = None):
        self.key = key or configuration.get_values("cryptopia","public_key")
        self.secret = secret or configuration.get_values("cryptopia","public_key")
        self.public = {
            'GetCurrencies',
            'GetTradePairs',
            'GetMarkets',
            'GetMarket',
            'GetMarketHistory',
            'GetMarketOrders',
            'GetMarketOrderGroups'}
        self.private = {
            'GetBalance',
            'GetDepositAddress',
            'GetOpenOrders',
            'GetTradeHistory',
            'GetTransactions',
            'SubmitTrade',
            'CancelTrade',
            'SubmitTip',
            'SubmitWithdraw',
            'SubmitTransfer'}

    def api_query(self, feature_requested, get_parameters=None, post_parameters=None):
        """ Performs a generic api request """
        time.sleep(1)
        if feature_requested in self.private:
            url = "https://www.cryptopia.co.nz/api/" + feature_requested + "/"
            post_data = json.dumps(post_parameters)
            headers = self.secure_headers(url=url, post_data=post_data)
            req = requests.post(url, data=post_data, headers=headers)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            try:
                # Remove bad format and encoding "iso-8859-1"
                matched = re.match(r"[^{]*({.*}).*",req.text).group(1)
                req = json.loads(matched)
            except:
                print(req.text)
            if req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                error = req
            return (result, error)
        elif feature_requested in self.public:
            url = "https://www.cryptopia.co.nz/Api/" + feature_requested + "/" + \
                  '/'.join(i for i in get_parameters.values()
                           ) if get_parameters != None else ""
            req = requests.get(url, params=get_parameters)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            matched = re.match(r"[^{]*({.*}).*",req.text).group(1)
            req = json.loads(matched)
            if req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                if req['Message'] is None:
                    error = "Unknown response error"
                else:
                    error = req['Message']
            return (result, error)
        else:
            return None, "Unknown feature"

    def get_currencies(self):
        """ Gets all the currencies """
        return self.api_query(feature_requested='GetCurrencies')

    def get_tradepairs(self):
        """ GEts all the trade pairs """
        return self.api_query(feature_requested='GetTradePairs')

    def get_markets(self, baseMarket = None, hours = None):
        """ Gets data for all markets """
        get_parameters = OrderedDict({})
        if baseMarket:
            get_parameters['market'] = baseMarket
        if hours:
            get_parameters['hours'] = str(hours)
        return self.api_query(feature_requested='GetMarkets',get_parameters=get_parameters)

    def get_market(self, market, hours = None):
        """ Gets market data """
        get_parameters=OrderedDict({'market': market})
        if hours: get_parameters['hours'] = str(hours)
        return self.api_query(feature_requested='GetMarket',
                              get_parameters=get_parameters)

    def get_history(self, market, hours = None):
        """ Gets the full order history for the market (all users) """
        get_parameters = OrderedDict({'market': market})
        if hours:
            get_parameters['hours'] = str(hours)
        return self.api_query(feature_requested='GetMarketHistory',
                                get_parameters=get_parameters)

    def get_orders(self, market):
        """ Gets the user history for the specified market """
        return self.api_query(feature_requested='GetMarketOrders',
                              get_parameters={'market': market})

    def get_ordergroups(self, markets):
        """ Gets the order groups for the specified market """
        return self.api_query(feature_requested='GetMarketOrderGroups',
                              get_parameters={'markets': markets})

    def get_balance(self, currency):
        """ Gets the balance of the user in the specified currency """
        result, error = self.api_query(feature_requested='GetBalance',
                                       post_parameters={'Currency': currency})
        if error is None:
            result = result[0]
        return (result, error)

    def get_openorders(self, market):
        """ Gets the open order for the user in the specified market """
        return self.api_query(feature_requested='GetOpenOrders',
                              post_parameters={'Market': market})

    def get_deposit_address(self, currency):
        """ Gets the deposit address for the specified currency """
        return self.api_query(feature_requested='GetDepositAddress',
                              post_parameters={'Currency': currency})

    def get_tradehistory(self, market):
        """ Gets the trade history for a market """
        return self.api_query(feature_requested='GetTradeHistory',
                              post_parameters={'Market': market})

    def get_transactions(self, transaction_type):
        """ Gets all transactions for a user """
        return self.api_query(feature_requested='GetTransactions',
                              post_parameters={'Type': transaction_type})

    def submit_trade(self, market, trade_type, rate, amount):
        """ Submits a trade """
        return self.api_query(feature_requested='SubmitTrade',
                              post_parameters={'Market': market,
                                               'Type': trade_type,
                                               'Rate': rate,
                                               'Amount': amount})

    def cancel_trade(self, trade_type, order_id, tradepair_id):
        """ Cancels an active trade """
        return self.api_query(feature_requested='CancelTrade',
                              post_parameters={'Type': trade_type,
                                               'OrderID': order_id,
                                               'TradePairID': tradepair_id})

    def submit_tip(self, currency, active_users, amount):
        """ Submits a tip """
        return self.api_query(feature_requested='SubmitTip',
                              post_parameters={'Currency': currency,
                                               'ActiveUsers': active_users,
                                               'Amount': amount})

    def submit_withdraw(self, currency, address, amount):
        """ Submits a withdraw request """
        return self.api_query(feature_requested='SubmitWithdraw',
                              post_parameters={'Currency': currency,
                                               'Address': address,
                                               'Amount': amount})

    def submit_transfer(self, currency, username, amount):
        """ Submits a transfer """
        return self.api_query(feature_requested='SubmitTransfer',
                              post_parameters={'Currency': currency,
                                               'Username': username,
                                               'Amount': amount})

    def secure_headers(self, url, post_data):
        """ Creates secure header for cryptopia private api. """
        nonce = str(int(time.time()))
        md5 = hashlib.md5()
        md5.update(post_data.encode("utf-8"))
        rcb64 = base64.b64encode(md5.digest())
        quoteplus = urllib.parse.quote_plus(url).lower()
        signature = bytearray()
        signature += (self.key + "POST" + quoteplus + nonce).encode() + rcb64 #.encode("utf8")
        sign = base64.b64encode(
            hmac.new(base64.b64decode( self.secret), signature,
            hashlib.sha256).digest())
        header_value = "amx " + self.key + ":" + sign.decode("utf8") + ":" + nonce
        return {'Authorization': header_value, 'Content-Type': 'application/json; charset=utf-8'}

# Better use loggin
#print("API Version ",__version__)
