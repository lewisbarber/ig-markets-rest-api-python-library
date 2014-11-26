#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

from ig_service import IGService
from ig_service_config import * # defines username, password, api_key, acc_type, acc_number
import pandas as pd

def test_ig_service():
    ig_service = IGService(username, password, api_key, acc_type)
    ig_service.create_session()

    response = ig_service.fetch_accounts()
    print(response)
    assert(response['balance'][0]['available']>0)

    response = ig_service.fetch_account_activity_by_period(10000)
    print(response)
    assert(isinstance(response, pd.DataFrame))

    response = ig_service.fetch_account_activity_by_period(10000)
    print(response)
    assert(isinstance(response, pd.DataFrame))

    response = ig_service.fetch_transaction_history_by_type_and_period(10000, "ALL")
    print(response)
    assert(isinstance(response, pd.DataFrame))

    response = ig_service.fetch_open_positions()
    print(response)
    assert(isinstance(response, pd.DataFrame))

    response = ig_service.fetch_working_orders()
    print(response)
    assert(isinstance(response, pd.DataFrame))

    response = ig_service.fetch_top_level_navigation_nodes()
    print(response)
    assert(isinstance(response, pd.DataFrame))
    market_id = response['id'].iloc[0]

    response = ig_service.fetch_client_sentiment_by_instrument(market_id)
    print(response)
    assert(isinstance(response, dict))

    response = ig_service.fetch_related_client_sentiment_by_instrument(market_id)
    print(response)
    assert(isinstance(response, pd.DataFrame))
