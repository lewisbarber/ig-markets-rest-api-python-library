#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
IG Markets REST API Library for Python
http://labs.ig.com/rest-trading-api-reference
By Lewis Barber - 2014 - http://uk.linkedin.com/in/lewisbarber/
"""

import requests
import json
import logging
import traceback
import pandas as pd

class IGService:

    CLIENT_TOKEN = None
    SECURITY_TOKEN = None

    BASIC_HEADERS = None
    LOGGED_IN_HEADERS = None
    DELETE_HEADERS = None

    D_BASE_URL = {
        'live': 'https://api.ig.com/gateway/deal',
        'demo': 'https://demo-api.ig.com/gateway/deal'
    }

    API_KEY = None
    IG_USERNAME = None
    IG_PASSWORD = None

    def __init__(self, username, password, api_key, acc_type="demo"):
        """Constructor, calls the method required to connect to the API (accepts acc_type = LIVE or DEMO)"""
        self.API_KEY = api_key
        self.IG_USERNAME = username
        self.IG_PASSWORD = password

        try:
            self.BASE_URL = self.D_BASE_URL[acc_type.lower()]
        except:
            raise(Exception("Invalid account type specified, please provide LIVE or DEMO."))

        self.BASIC_HEADERS = { 
            'X-IG-API-KEY': self.API_KEY,
            'Content-Type': 'application/json', 
            'Accept': 'application/json; charset=UTF-8' 
        }

        self.parse_response = self.parse_response_with_exception

        self.return_dataframe = True

        #self.create_session()


    ########## PARSE_RESPONSE ##########

    def parse_response_without_exception(self, *args, **kwargs):
        """Parses JSON response
        returns dict
        no exception raised when error occurs"""
        response = json.loads(*args, **kwargs)
        return(response)

    def parse_response_with_exception(self, *args, **kwargs):
        """Parses JSON response
        returns dict
        exception raised when error occurs"""
        response = json.loads(*args, **kwargs)
        if 'errorCode' in response:
            raise(Exception(response['errorCode']))
        return(response)

    ############ END ############


    ########## ACCOUNT ##########

    def fetch_accounts(self):
        """Returns a list of accounts belonging to the logged-in client"""
        response = requests.get(self.BASE_URL + '/accounts', headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['accounts'])
        return(data)

    def fetch_account_activity_by_period(self, milliseconds):
        """Returns the account activity history for the last specified period"""
        response = requests.get(self.BASE_URL + '/history/activity/%s' % milliseconds, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['activities'])
        return(data)

    def fetch_transaction_history_by_type_and_period(self, milliseconds, trans_type):
        """Returns the transaction history for the specified transaction type and period"""
        response = requests.get(self.BASE_URL + '/history/transactions/%s/%s' % (trans_type, milliseconds), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['transactions'])
        return(data)

    ############ END ############



    ########## DEALING ##########

    def fetch_deal_by_deal_reference(self, deal_reference):
        """Returns a deal confirmation for the given deal reference"""
        response = requests.get(self.BASE_URL + '/confirms/%s' % deal_reference, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def fetch_open_positions(self):
        """Returns all open positions for the active account"""
        response = requests.get(self.BASE_URL  + '/positions', headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['positions'])
        return(data)

    def close_open_position(self, deal_id, direction, epic, expiry, level, order_type, quote_id, size):
        """Closes one or more OTC positions"""
        params = { 
            'dealId': deal_id, 
            'direction': direction, 
            'epic': epic, 
            'expiry': expiry, 
            'level': level,
            'orderType': order_type,
            'quoteId': quote_id,
            'size': size
        }

        response = requests.post(self.BASE_URL + '/positions/otc', data=json.dumps(params), headers=self.DELETE_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text)

    def create_open_position(self, currency_code, direction, epic, expiry, force_open, 
        guaranteed_stop, level, limit_distance, limit_level, order_type, quote_id, size, 
        stop_distance, stop_level):
        """Creates an OTC position"""
        params = { 
            'currencyCode': currency_code, 
            'direction': direction, 
            'epic': epic, 
            'expiry': expiry, 
            'forceOpen': force_open, 
            'guaranteedStop': guaranteed_stop,
            'level': level,
            'limitDistance': limit_distance,
            'limitLevel': limit_level,
            'orderType': order_type,
            'quoteId': quote_id,
            'size': size,
            'stopDistance': stop_distance,
            'stopLevel': stop_level
        }

        response = requests.post(self.BASE_URL + '/positions/otc', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text) # parse_response ?

    def update_open_position(self, limit_level, stop_level, deal_id):
        """Updates an OTC position"""
        params = {
            'limitLevel': limit_level,
            'stopLevel': stop_level
        }

        response = requests.put(self.BASE_URL + '/positions/otc/%s' % deal_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text) # parse_response ?

    def fetch_working_orders(self):
        """Returns all open working orders for the active account"""
        response = requests.get(self.BASE_URL  + '/workingorders', headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['workingOrders'])
        return(data)

    def create_working_order(self, currency_code, direction, epic, expiry, good_till_date, 
        guaranteed_stop, level, limit_distance, limit_level, size, stop_distance, stop_level,
        time_in_force, order_type):
        """Creates an OTC working order"""
        params = { 
            'currencyCode': currency_code, 
            'direction': direction, 
            'epic': epic, 
            'expiry': expiry, 
            'goodTillDate': good_till_date, 
            'guaranteedStop': guaranteed_stop,
            'level': level,
            'limitDistance': limit_distance,
            'limitLevel': limit_level,
            'size': size,
            'stopDistance': stop_distance,
            'stopLevel': stop_level,
            'timeInForce': time_in_force,
            'type': order_type
        }

        response = requests.post(self.BASE_URL + '/workingorders/otc', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text) # parse_response ?

    def delete_working_order(self, deal_id):
        """Deletes an OTC working order"""
        response = requests.post(self.BASE_URL + '/workingorders/otc/%s' % deal_id, data=json.dumps({}), headers=self.DELETE_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text) # parse_response ?

    def update_working_order(self, good_till_date, level, limit_distance, limit_level, 
        stop_distance, stop_level, time_in_force, order_type, deal_id):
        """Updates an OTC working order"""
        params = {
            'goodTillDate': good_till_date,
            'limitDistance': limit_distance,
            'level': level,
            'limitLevel': limit_level,
            'stopDistance': stop_distance,
            'stopLevel': stop_level,
            'timeInForce': time_in_force,
            'type': order_type
        }

        response = requests.put(self.BASE_URL + '/workingorders/otc/%s' % deal_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

        if response.status_code == 200:
            deal_reference = json.loads(response.text)['dealReference']
            return(self.fetch_deal_by_deal_reference(deal_reference))
        else:
            return(response.text) # parse_response ?

    ############ END ############



    ########## MARKETS ##########

    def fetch_client_sentiment_by_instrument(self, market_id):
        """Returns the client sentiment for the given instrument's market"""
        response = requests.get(self.BASE_URL + '/clientsentiment/%s' % market_id, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def fetch_related_client_sentiment_by_instrument(self, market_id):
        """Returns a list of related (also traded) client sentiment for the given instrument's market"""
        response = requests.get(self.BASE_URL + '/clientsentiment/related/%s' % market_id, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['clientSentiments'])
        return(data)

    def fetch_top_level_navigation_nodes(self):
        """Returns all top-level nodes (market categories) in the market navigation hierarchy."""
        response = requests.get(self.BASE_URL + '/marketnavigation', headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data['markets'] = pd.DataFrame(data['markets'])
            data['nodes'] = pd.DataFrame(data['nodes'])
        return(data)

    def fetch_sub_nodes_by_node(self, node):
        """Returns all sub-nodes of the given node in the market navigation hierarchy"""
        response = requests.get(self.BASE_URL + '/marketnavigation/%s' % node, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data['markets'] = pd.DataFrame(data['markets'])
            data['nodes'] = pd.DataFrame(data['nodes'])
        return(data)

    def fetch_market_by_epic(self, epic):
        """Returns the details of the given market"""
        response = requests.get(self.BASE_URL + '/markets/%s' % epic, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def search_markets(self, search_term):
        """Returns all markets matching the search term"""
        response = requests.get(self.BASE_URL + '/markets?searchTerm=%s' % search_term, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['markets'])
        return(data)

    def fetch_historical_prices_by_epic_and_date_range(self, epic, resolution, start_date, end_date):
        """Returns a list of historical prices for the given epic, resolution, multiplier and date range"""
        response = requests.get(self.BASE_URL + "/prices/{epic}/{resolution}/?startdate={start_date}&enddate={end_date}".format(epic=epic, resolution=resolution, start_date=start_date, end_date=end_date), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data['prices'] = pd.DataFrame(data['prices'])
        return(data)

    ############ END ############



    ######### WATCHLISTS ########

    def fetch_all_watchlists(self):
        """Returns all watchlists belonging to the active account"""
        response = requests.get(self.BASE_URL + '/watchlists', headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['watchlists'])
        return(data)

    def create_watchlist(self, name, epics):
        """Creates a watchlist"""
        params = { 
            'name': name, 
            'epics': epics
        }

        response = requests.post(self.BASE_URL + '/watchlists', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def delete_watchlist(self, watchlist_id):
        """Deletes a watchlist"""
        response = requests.post(self.BASE_URL + '/watchlists/%s' % watchlist_id, data=json.dumps({}), headers=self.DELETE_HEADERS)
        return(response.text)


    def fetch_watchlist_markets(self, watchlist_id):
        """Returns the given watchlist's markets"""
        response = requests.get(self.BASE_URL + '/watchlists/%s' % watchlist_id, headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        if self.return_dataframe:
            data = pd.DataFrame(data['markets'])
        return(data)


    def add_market_to_watchlist(self, watchlist_id, epic):
        """Adds a market to a watchlist"""
        params = { 
            'epic': epic
        }

        response = requests.put(self.BASE_URL + '/watchlists/%s' % watchlist_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def remove_market_from_watchlist(self, watchlist_id, epic):
        """Remove an market from a watchlist"""
        response = requests.post(self.BASE_URL + '/watchlists/%s/%s' % (watchlist_id, epic), data=json.dumps({}), headers=self.DELETE_HEADERS)
        return(response.text)

    ############ END ############



    ########### LOGIN ###########

    def logout(self):
        """Log out of the current session"""
        requests.post(self.BASE_URL + '/session', data=json.dumps({}), headers=self.DELETE_HEADERS)

    def create_session(self):
        """Creates a trading session, obtaining session tokens for subsequent API access"""
        params = { 
            'identifier': self.IG_USERNAME, 
            'password': self.IG_PASSWORD 
        }

        response = requests.post(self.BASE_URL  + '/session', data=json.dumps(params), headers=self.BASIC_HEADERS)

        data = self.parse_response(response.text)

        self._set_headers(response.headers, True)

        return(data)

    def switch_account(self, account_id, default_account):
        """Switches active accounts, optionally setting the default account"""
        params = { 
            'accountId': account_id, 
            'defaultAccount': default_account
        }

        response = requests.put(self.BASE_URL + '/session', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

        self._set_headers(response.headers, False)

        return self.parse_response(response.text)

    ############ END ############



    ########## GENERAL ##########
    
    def get_client_apps(self):
        """Returns a list of client-owned applications"""
        response = requests.get(self.BASE_URL + '/operations/application', headers=self.LOGGED_IN_HEADERS)

        return self.parse_response(response.text)

    def update_client_app(self, allowance_account_overall, allowance_account_trading, api_key, status):
        """Updates an application"""
        params = { 
            'allowanceAccountOverall': allowance_account_overall, 
            'allowanceAccountTrading': allowance_account_trading, 
            'apiKey': api_key, 
            'status': status
        }

        response = requests.put(self.BASE_URL + '/operations/application', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)

    def disable_client_app_key(self):
        """Disables the current application key from processing further requests. 
        Disabled keys may be reenabled via the My Account section on the IG Web Dealing Platform."""
        response = requests.put(self.BASE_URL + '/operations/application/disable', data=json.dumps({}), headers=self.LOGGED_IN_HEADERS)
        data = self.parse_response(response.text)
        return(data)
        
    ############ END ############



    ########## PRIVATE ##########

    def _set_headers(self, response_headers, update_cst):
        """Sets headers"""
        if update_cst == True:
            self.CLIENT_TOKEN = response_headers['CST']

        try:
            self.SECURITY_TOKEN = response_headers['X-SECURITY-TOKEN']
        except:
            self.SECURITY_TOKEN = None

        self.LOGGED_IN_HEADERS = { 
            'X-IG-API-KEY': self.API_KEY, 
            'X-SECURITY-TOKEN': self.SECURITY_TOKEN, 
            'CST': self.CLIENT_TOKEN, 
            'Content-Type': 'application/json', 
            'Accept': 'application/json; charset=UTF-8' 
        }

        self.DELETE_HEADERS = { 
            'X-IG-API-KEY': self.API_KEY, 
            'X-SECURITY-TOKEN': self.SECURITY_TOKEN, 
            'CST': self.CLIENT_TOKEN, 
            'Content-Type': 'application/json', 
            'Accept': 'application/json; charset=UTF-8',
            '_method': 'DELETE'
        }

    ############ END ############
