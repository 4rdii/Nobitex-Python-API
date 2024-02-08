import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from src import AccountOperations, TradingOperations,MarketData
from src.AccountOperations import CustomError  
import unittest
from unittest.mock import patch, MagicMock
import requests
from src import AccountOperations   
from src.AccountOperations import nobitexWalletLists  
from src.TradingOperations import  TradingOperations

import pytest
load_dotenv()
username = os.getenv("NOBITEX_USERNAME")
password = os.getenv("NOBITEX_PASSWORD")

class TestNobitexLogin(unittest.TestCase):

    @patch('requests.post')
    def test_successful_login(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'valid_token'}
        mock_post.return_value = mock_response

        # Call the function with valid credentials
        token = AccountOperations.nobitexLogin('valid_username', 'valid_password')

        # Assert the function returns the expected token
        self.assertEqual(token, 'valid_token')

    @patch('requests.post')
    def test_failed_login(self, mock_post):
        # Mock failed response
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': 'invalid_credentials'}
        mock_post.return_value = mock_response

        # Call the function with invalid credentials
        with self.assertRaises(CustomError):  # Expect the CustomError to be raised
            AccountOperations.nobitexLogin('invalid_username', 'invalid_password')


    @patch('requests.post')
    def test_two_factor_authentication(self, mock_post):
        # Mock successful response with two-factor authentication
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'valid_token'}
        mock_post.return_value = mock_response

        # Call the function with two-factor authentication enabled
        token = AccountOperations.nobitexLogin('valid_username', 'valid_password', twoFactorAuthentication='123456')

        # Assert the function returns the expected token
        self.assertEqual(token, 'valid_token')

    @patch('requests.post')
    def test_remember_me_option(self, mock_post):
        # Mock successful response with remember me option set to "no"
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'short_lived_token'}
        mock_post.return_value = mock_response

        # Call the function with remember me option set to "no"
        token = AccountOperations.nobitexLogin('valid_username', 'valid_password', remember='no')

        # Assert the function returns the expected token
        self.assertEqual(token, 'short_lived_token')

class TestNobitexWalletLists(unittest.TestCase):

    @patch('requests.post')
    def test_wallet_list_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "wallets": {
                "DOGE": {
                    "id":  2758933,
                    "balance": "80.8225",
                    "blocked": "0"
                },
                "RLS": {
                    "id":  2758920,
                    "balance": "12018829.48289",
                    "blocked": "0"
                },
                "USDT": {
                    "id":  2758924,
                    "balance": "6.4515",
                    "blocked": "0"
                },
                "BTC": {
                    "id":  2758921,
                    "balance": "0",
                    "blocked": "0"
                }
            }
        }
        mock_post.return_value = mock_response

        # Call the function with a valid key
        df = nobitexWalletLists('valid_key')

        # Assert the function returns a DataFrame with the expected shape
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df),   4)  # Four currencies in the mock response
        self.assertEqual(df.columns.tolist(), ['id', 'balance', 'blocked'])  # Check column names


    @patch('requests.post')
    def test_wallet_list_failure(self, mock_post):
        # Mock failed response
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': 'invalid_key'}
        mock_post.return_value = mock_response

        # Call the function with an invalid key
        with self.assertRaises(CustomError):  # Expect the CustomError to be raised
            nobitexWalletLists('invalid_key')

class TestPlaceLimitOrder(unittest.TestCase):

    @patch('requests.post')
    def test_place_limit_order_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'order': {
                        'type': 'buy',
                        'execution': 'Limit',
                        'tradeType': 'Spot',
                        'srcCurrency': 'Tether',
                        'dstCurrency': '﷼',
                        'price': '550000',
                        'amount': '100',
                        'totalPrice': '0',
                        'totalOrderPrice': '55000000',
                        'matchedAmount': 0,
                        'unmatchedAmount': '100',
                        'clientOrderId': None,
                        'isMyOrder': False,
                        'id': 12345,
                        'status': 'Active',
                        'partial': False,
                        'fee': 0,
                        'user': 'email@email.com',
                        'created_at': '2024-02-06T21:49:02',
                        'market': 'USDT-RLS',
                        'averagePrice': '0'}
        }
        mock_post.return_value = mock_response

        # Create an instance of TradingOperations with a fake authentication token
        trader = TradingOperations('test_user', 'test_pass', twoFactorAuthentication=None, remember=True)
        trader.authentication_token = 'fake_auth_token'

        # Call the placeLimitOrder method with valid parameters
        order_id = trader.placeLimitOrder('buy', 'btc', 'rls',  23899999880,  0.001)

        # Assert the function returns the correct order ID
        self.assertEqual(order_id,  12345)

    @patch('requests.post')
    def test_place_limit_order_failure(self, mock_post):
        # Mock failed response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Invalid parameters'
        }
        mock_post.return_value = mock_response

        # Create an instance of TradingOperations with a fake authentication token
        trader = TradingOperations('test_user', 'test_pass', twoFactorAuthentication=None, remember=True)
        trader.authentication_token = 'fake_auth_token'

        # Call the placeLimitOrder method with invalid parameters
        with self.assertRaises(ValueError):  # Expect a ValueError to be raised
            trader.placeLimitOrder('invalid_type', 'btc', 'rls',  23899999880,  0.001)

    # Add more tests for edge cases, validation checks, etc.

class TestTransactionFlow(unittest.TestCase):

    def setUp(self):
        # Set up test environment
        self.trader = TradingOperations(os.environ['NOBITEX_USERNAME'], os.environ['NOBITEX_PASSWORD'])

    def test_transaction_flow(self):
        # Place a limit order
        self.order_id = self.trader.placeLimitOrder('buy', 'btc', 'usdt',  23899999880,  0.001)
        self.assertIsNotNone(self.order_id, "Order placement failed")

        # Retrieve the order status
        order_status = self.trader.getOrderStatus(self.order_id)
        self.assertEqual(order_status, 'open', "Order status should be 'open'")

    def tearDown(self):
        # Cancel the order if it's still open
        if self.order_id:
            self.trader.cancelOrder(self.order_id)


if __name__ == '__main__':
    unittest.main()
