## IG Markets REST API - Python Library
--------------------------------------

A lightweight Python library that can be used to connect to the IG Markets REST API with a LIVE or DEMO account.

You can use the IG Markets HTTP / REST API to submit trade orders, open positions, close positions and view market sentiment. IG Markets provide Retail Spread Betting and CFD accounts for trading Equities, Forex, Commodities, Indices and much more.

Full details about the API along with information about how to open an account with IG can be found at the following link:

[http://labs.ig.com/](http://labs.ig.com/)

### How To Use The Library
--------------------------

Using this library to connect to the IG Markets API is extremely easy. All you need to do is import the IGService class, create an instance, and call the methods you wish to use. There is a method for each API endpoint exposed by their API. The code sample below shows you how to connect to the API, switch to a secondary account and retrieve all open positions for the active account.

**Note:** The secure session with IG is established when you create an instance of the class.

```python
from ig_service import IGService

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
api_key = "YOUR_API_KEY"
acc_type = "LIVE" # LIVE / DEMO

ig_service = IGService(username, password, api_key, acc_type)

account_info = ig_service.switch_account('ABC123', False)

print account_info

open_positions = ig_service.fetch_open_positions()

print open_positions
```
