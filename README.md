## IG Markets REST API - Python Library
-------------------------------------

A lightweight Python library that can be used to connect to the IG Markets REST API with a LIVE or DEMO account.

You can use the IG Markets HTTP / REST API to submit trade orders, open positions, close positions and view market sentiment. IG Markets provide Retail Spread Betting and CFD accounts for trading Equities, Forex, Commodities, Indices and much more.

Full details about the API or for information about how to open a CFD / Spread Betting account with IG Markets can be found by following the link below:

[http://labs.ig.com/](http://labs.ig.com/)

### How To Use The Library
--------------------------

Using this library to connect to the IG Markets API is extremely easy. All you need to do is import the IGService class, create an instance, and call the methods you wish to use. There is a method for each API endpoint exposed by their API. The code sample below shows you how to connect to the API, switch to a secondary account and retrieve all open positions for the active account.

**Note:** The secure session with IG is established when you create an instance of the class. You will need to set your USERNAME, PASSWORD and API_KEY for IG at the top of the IGService class.

```python
from ig_service import IGService

ig_service = IGService()

account_info = ig_service.switch_account('ABC123', False)

print account_info

open_positions = ig_service.fetch_open_positions()

print open_positions
```
