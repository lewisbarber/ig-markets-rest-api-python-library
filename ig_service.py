import requests
import json

# IG Markets REST API Library for Python
# http://labs.ig.com/rest-trading-api-reference
# By Lewis Barber - 2014 - http://uk.linkedin.com/in/lewisbarber/

class IGService:

	CLIENT_TOKEN = None
	SECURITY_TOKEN = None

	BASIC_HEADERS = None
	LOGGED_IN_HEADERS = None
	DELETE_HEADERS = None

	BASE_URL = 'https://api.ig.com/gateway/deal'
	BASE_URL_DEMO = 'https://demo-api.ig.com/gateway/deal'

	API_KEY = None
	IG_USERNAME = None
	IG_PASSWORD = None

	# Constructor, calls the method required to connect to the API (accepts acc_type = LIVE or DEMO)
	def __init__(self, username, password, api_key, acc_type="LIVE"):

		self.API_KEY = api_key
		self.IG_USERNAME = username
		self.IG_PASSWORD = password

		if acc_type != "DEMO" and acc_type != "LIVE":
			print "Error: Invalid account type specified, please provide LIVE or DEMO."
			return

		if acc_type == "DEMO":
			self.BASE_URL = self.BASE_URL_DEMO

		self.BASIC_HEADERS = { 
			'X-IG-API-KEY': self.API_KEY,
			'Content-Type': 'application/json', 
			'Accept': 'application/json; charset=UTF-8' 
		}

		self.create_session()

	########## ACCOUNT ##########

	# Returns a list of accounts belonging to the logged-in client
	def fetch_accounts(self):

		response = requests.get(self.BASE_URL + '/accounts', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns the account activity history for the last specified period
	def fetch_account_activity_by_period(self, milliseconds):

		response = requests.get(self.BASE_URL + '/history/activity/' + milliseconds, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns the transaction history for the specified transaction type and period
	def fetch_transaction_history_by_type_and_period(self, milliseconds, trans_type):

		response = requests.get(self.BASE_URL + '/history/transactions/' + trans_type + '/' + milliseconds, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	############ END ############



	########## DEALING ##########

	# Returns a deal confirmation for the given deal reference
	def fetch_deal_by_deal_reference(self, deal_reference):

		response = requests.get(self.BASE_URL + '/confirms/' + deal_reference, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns all open positions for the active account
	def fetch_open_positions(self):

		response = requests.get(self.BASE_URL  + '/positions', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Closes one or more OTC positions
	def close_open_position(self, deal_id, direction, epic, expiry, level, order_type, quote_id, size):

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
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	# Creates an OTC position
	def create_open_position(self, currency_code, direction, epic, expiry, force_open, 
		guaranteed_stop, level, limit_distance, limit_level, order_type, quote_id, size, 
		stop_distance, stop_level):

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
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	# Updates an OTC position
	def update_open_position(self, limit_level, stop_level, deal_id):

		params = {
			'limitLevel': limit_level,
			'stopLevel': stop_level
		}

		response = requests.put(self.BASE_URL + '/positions/otc/' + deal_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		if response.status_code == 200:
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	# Returns all open working orders for the active account
	def fetch_working_orders(self):

		response = requests.get(self.BASE_URL  + '/workingorders', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Creates an OTC working order
	def create_working_order(self, currency_code, direction, epic, expiry, good_till_date, 
		guaranteed_stop, level, limit_distance, limit_level, size, stop_distance, stop_level,
		time_in_force, order_type):

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
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	# Deletes an OTC working order
	def delete_working_order(self, deal_id):

		response = requests.post(self.BASE_URL + '/workingorders/otc/' + deal_id, data=json.dumps({}), headers=self.DELETE_HEADERS)

		if response.status_code == 200:
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	# Updates an OTC working order
	def update_working_order(self, good_till_date, level, limit_distance, limit_level, 
		stop_distance, stop_level, time_in_force, order_type, deal_id):

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

		response = requests.put(self.BASE_URL + '/workingorders/otc/' + deal_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		if response.status_code == 200:
			return self.fetch_deal_by_deal_reference(json.loads(response.text)['dealReference'])
		else:
			return response.text

	############ END ############



	########## MARKETS ##########

	# Returns the client sentiment for the given instrument's market
	def fetch_client_sentiment_by_instrument(self, market_id):

		response = requests.get(self.BASE_URL + '/clientsentiment/' + market_id, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns a list of related (also traded) client sentiment for the given instrument's market
	def fetch_related_client_sentiment_by_instrument(self, market_id):

		response = requests.get(self.BASE_URL + '/clientsentiment/related/' + market_id, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns all top-level nodes (market categories) in the market navigation hierarchy.
	def fetch_top_level_navigation_nodes(self):

		response = requests.get(self.BASE_URL + '/marketnavigation', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns all sub-nodes of the given node in the market navigation hierarchy
	def fetch_sub_nodes_by_node(self, node):

		response = requests.get(self.BASE_URL + '/marketnavigation/' + node, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns the details of the given market
	def fetch_market_by_epic(self, epic):

		response = requests.get(self.BASE_URL + '/markets/' + epic, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns all markets matching the search term
	def search_markets(self, search_term):

		response = requests.get(self.BASE_URL + '/markets?searchTerm=' + search_term, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Returns a list of historical prices for the given epic, resolution, multiplier and date range
	def fetch_historical_prices_by_epic_and_date_range(self, epic, resolution, start_date, end_date):

		response = requests.get(self.BASE_URL + '/prices/' + epic + '/' + resolution + '?startdate=' + start_date + '&enddate=' + end_date, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	############ END ############



	######### WATCHLISTS ########

	# Returns all watchlists belonging to the active account
	def fetch_all_watchlists(self):

		response = requests.get(self.BASE_URL + '/watchlists', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Creates a watchlist
	def create_watchlist(self, name, epics):

		params = { 
			'name': name, 
			'epics': epics
		}

		response = requests.post(self.BASE_URL + '/watchlists', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Deletes a watchlist
	def delete_watchlist(self, watchlist_id):

		response = requests.post(self.BASE_URL + '/watchlists/' + watchlist_id, data=json.dumps({}), headers=self.DELETE_HEADERS)

		return response.text


	# Returns the given watchlist's markets
	def fetch_watchlist_markets(self, watchlist_id):

		response = requests.get(self.BASE_URL + '/watchlists/' + watchlist_id, headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)


	# Adds a market to a watchlist
	def add_market_to_watchlist(self, watchlist_id, epic):

		params = { 
			'epic': epic
		}

		response = requests.put(self.BASE_URL + '/watchlists/' + watchlist_id, data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Remove an market from a watchlist
	def remove_market_from_watchlist(self, watchlist_id, epic):

		response = requests.post(self.BASE_URL + '/watchlists/' + watchlist_id + '/' + epic, data=json.dumps({}), headers=self.DELETE_HEADERS)

		return response.text

	############ END ############



	########### LOGIN ###########

	# Log out of the current session
	def logout(self):
		
		requests.post(self.BASE_URL + '/session', data=json.dumps({}), headers=self.DELETE_HEADERS)

	# Creates a trading session, obtaining session tokens for subsequent API access
	def create_session(self):

		params = { 
			'identifier': self.IG_USERNAME, 
			'password': self.IG_PASSWORD 
		}

		response = requests.post(self.BASE_URL  + '/session', data=json.dumps(params), headers=self.BASIC_HEADERS)

		print response.text

		self.set_headers(response.headers, True)

	# Switches active accounts, optionally setting the default account
	def switch_account(self, account_id, default_account):

		params = { 
			'accountId': account_id, 
			'defaultAccount': default_account
		}

		response = requests.put(self.BASE_URL + '/session', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		self.set_headers(response.headers, False)

		return json.loads(response.text)

	############ END ############



	########## GENERAL ##########
	
	# Returns a list of client-owned applications
	def get_client_apps(self):

		response = requests.get(self.BASE_URL + '/operations/application', headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Updates an application
	def update_client_app(self, allowance_account_overall, allowance_account_trading, api_key, status):

		params = { 
			'allowanceAccountOverall': allowance_account_overall, 
			'allowanceAccountTrading': allowance_account_trading, 
			'apiKey': api_key, 
			'status': status
		}

		response = requests.put(self.BASE_URL + '/operations/application', data=json.dumps(params), headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	# Disables the current application key from processing further requests. 
	# Disabled keys may be reenabled via the My Account section on the IG Web Dealing Platform.
	def disable_client_app_key(self):

		response = requests.put(self.BASE_URL + '/operations/application/disable', data=json.dumps({}), headers=self.LOGGED_IN_HEADERS)

		return json.loads(response.text)

	############ END ############



	########## PRIVATE ##########

	def set_headers(self, response_headers, update_cst):

		if update_cst == True:
			self.CLIENT_TOKEN = response_headers['CST']

		self.SECURITY_TOKEN = response_headers['X-SECURITY-TOKEN']

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
