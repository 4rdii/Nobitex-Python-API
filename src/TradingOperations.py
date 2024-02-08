import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from src import  AccountOperations, MarketData
import logging
logging.basicConfig(filename='trading_operations.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


"""
    @title Python functions for Nobitex.com APIs
    @author Ardeshir Gholami https://github.com/4rdii
    @notice Take care Using your account with real money this repo is Under development!!
"""

class TradingOperations():

    def __init__(self,username, password, twoFactorAuthentication,remember) -> None:
        self.username = username
        self.password = password
        self.twoFactorAuthentication = twoFactorAuthentication
        self.remember = "yes"
        self.authenticationToken = self.login()
    
    def login(self):
        """
        logins to nobitex account using AccountOperations module
        module will autorun when you build an object
        """
        Token = os.getenv("NOBITEX_TOKEN")
        if Token == '0':
            Token = AccountOperations.nobitexLogin(self.username,
                                                   self.password,
                                                   self.twoFactorAuthentication,
                                                   self.remember)
        #### @dev Add later: Automatically add token to .env ####
        return Token
    
    def logout(self):
        logoutStatus = AccountOperations.nobitexLogout(self.authenticationToken)
        if logoutStatus:
            print("Token was successfully burnt!")
        else:
            print("log out failed! check the token!")

    def getCurrentPrice(self, srcCurrency,dstCurrency):
        if dstCurrency.lower == "irt":
            dstCurrency = "rls"
            rialToTomanFactor = 0.1
        else:
            rialToTomanFactor = 1
        symbolStats = MarketData.nobitexPairStats()
        latestPrice = rialToTomanFactor*int(symbolStats[f"{srcCurrency.lower()}-{dstCurrency.lower()}.latest"].values)
        return latestPrice

    def placeLimitOrder(self,type,srcCurrency,dstCurrency,price,amount):
        """
        PLACE LIMIT ORDER FUNCTION
            using this function you can place a limit order with these input parameters:
            1- type: "buy" or "sell"
            2- srcCurruency: "btc"
            3- dstCurrency: "rls" 
            Note: CARE DO NOT USE "IRT" - at the moment api dose not support IRT and only works with rials
            4- price: 23899999880 (in rials)
            5- amount: 0.001
            Note: a. There is a maximum decimals for each pair plesae use this link: https://nobitex.ir/policies/markets/
                  b. Also there is minimum trading amount (500,000 IRT at the moment)  
            returns the Order ID,
            API json format: (for further developments)
                  {'status': 'ok',
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
                        'id': 1304571635,
                        'status': 'Active',
                        'partial': False,
                        'fee': 0,
                        'user': 'email@email.com',
                        'created_at': '2024-02-06T21:49:02',
                        'market': 'USDT-RLS',
                        'averagePrice': '0'
                        }}
        """
        # Validate input parameters
        if type not in ['buy', 'sell']:
            raise ValueError("Invalid order type. Must be 'buy' or 'sell'.")
        if not srcCurrency or not dstCurrency:
            raise ValueError("Source and destination currencies must be specified.")
        if (price) <=  0 or (amount) <=  0:
            raise ValueError("Price and amount must be greater than zero.")
        
        mode = "default"
        execution = "limit"
        addOrderURL = "https://api.nobitex.ir/market/orders/add"
       
        header = {"Authorization": f"Token {self.authenticationToken}"}
        payLoad = {"type":type,
                   "mode": mode,
                   "execution": execution,
                   "srcCurrency": srcCurrency.lower(),
                   "dstCurrency": dstCurrency.lower(),
                   "amount": f"{amount}",
                   "price": f"{price}"
        }
        try:
            response = requests.post(url=addOrderURL, data=payLoad,headers=header)
            response.raise_for_status()  # Raise an exception for HTTP errors

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as err:
            logging.error(f"Error occurred: {err}")
            raise
        # Parse the response
        try:
            response_data = response.json()
            if response_data['status'] != 'ok':
                raise ValueError(f"Order placement failed: {response_data['message']}")
        except KeyError:
            logging.error("Unexpected response format from the API.")
            raise

        logging.info(f"Limit {type} order placed successfully for {amount} {srcCurrency}-{dstCurrency} at Price: {price}. Order ID: {response_data['order']['id']}")

        print(f"""
              =======================================================================================
              ORDER SUCCESSFUL:\n
              Limit {type} order placed for {amount} {srcCurrency}-{dstCurrency} at Price: {price}\n
              order created at {response.json()["order"]["created_at"]}\n
              Order Id = {response.json()["order"]["id"]}
              =======================================================================================
              """)
        return response_data['order']['id']
    
    def placeMarketExecutionOrder(self,type,srcCurrency,dstCurrency,amount):
        """
        PLACE Market price ORDER FUNCTION
            using this function you can place a limit order with these input parameters:
            1- type: "buy" or "sell"
            2- srcCurruency: "btc"
            3- dstCurrency: "rls" 
            Note: CARE DO NOT USE "IRT" - at the moment api dose not support IRT and only works with rials
            4- price: 23899999880 (in rials)
            5- amount: 0.001
            Note: a. There is a maximum decimals for each pair plesae use this link: https://nobitex.ir/policies/markets/
                  b. Also there is minimum trading amount (500,000 IRT at the moment)  
            returns the Order ID,
        """
        # Validate input parameters
        if type not in ['buy', 'sell']:
            raise ValueError("Invalid order type. Must be 'buy' or 'sell'.")
        if not srcCurrency or not dstCurrency:
            raise ValueError("Source and destination currencies must be specified.")
        if (amount) <=  0:
            raise ValueError("amount must be greater than zero.")
        
        mode = "default"
        execution = "market"
        addOrderURL = "https://api.nobitex.ir/market/orders/add"
       
        header = {"Authorization": f"Token {self.authenticationToken}"}
        payLoad = {"type":type,
                   "mode": mode,
                   "execution": execution,
                   "srcCurrency": srcCurrency.lower(),
                   "dstCurrency": dstCurrency.lower(),
                   "amount": f"{amount}",
                   
        }
        try:
            response = requests.post(url=addOrderURL, data=payLoad,headers=header)
            print(response.json())
            response.raise_for_status()  # Raise an exception for HTTP errors


        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as err:
            logging.error(f"Error occurred: {err}")
            raise
        # Parse the response
        try:
            response_data = response.json()
            if response_data['status'] != 'ok':
                raise ValueError(f"Order placement failed: {response_data['message']}")
        except KeyError:
            logging.error("Unexpected response format from the API.")
            raise

        logging.info(f"Limit {type} order placed successfully for {amount} {srcCurrency}-{dstCurrency} at Market Price. Order ID: {response_data['order']['id']}")

        print(f"""
              =======================================================================================
              ORDER SUCCESSFUL:\n
              Market Price {type} order placed for {amount} {srcCurrency}-{dstCurrency} at MarketPrice\n
              order created at {response.json()["order"]["created_at"]}\n
              Order Id = {response.json()["order"]["id"]}
              =======================================================================================
              """)
        return response_data['order']['id']

    def placeStopMarketOrder(self):
        pass

    def placeStopLimitOrder(self):
        pass
    
    def placeOcoOrders(self):
        pass
    
    def cancelOrder(self,orderId):
        """
        CANCEL AN ORDER GIVEN ORDER ID
        """
        cancelOrderURL = "https://api.nobitex.ir/market/orders/update-status"
        header = {"Authorization": f"Token {self.authenticationToken}"}
        payLoad = {"order":orderId,
                   "status": "canceled",
        }
        try:
            response = requests.post(url=cancelOrderURL, data=payLoad,headers=header)
            try:
                status = response.json()["updatedStatus"]
                print(f"""
              =======================================================================================
                      ORDER CANCELD SUCCESSFULLY:\n
                      Order with Id: {orderId} was successfully Canceled.
                      current order status: {status}
              =======================================================================================
                    """)
            except:
                print(response.json())
        except Exception:
            traceback.print_exc()
    
    # def addOrder(self,type,mode,execution,srcCurrency,dstCurrency,amount,price,stopPrice,stopLimitPrice,):
    #     # remove later
    #     pass

    def getOrderStatus(self,orderId):
        """
        RETRUNS ORDER STATUS GIVEN THE ORDER ID
        """
        getOrderStatusURL = f'https://api.nobitex.ir/market/orders/status?id={orderId}'
       
        header = {"Authorization": f"Token {self.authenticationToken}"}
        try:
            response = requests.get(url=getOrderStatusURL,headers=header)
            status = response.json()["order"]["status"]
            print(f"Order with OrderId = {orderId} is {status}")
        except Exception:
            traceback.print_exc()
        return status

    def getOrdersList(self):
        """
        This function gives a list of all active orders
        """
        getOrdersList = "https://api.nobitex.ir/market/orders/list"
        header = {"Authorization": f"Token {self.authenticationToken}"}
        try:
            response = requests.post(url=getOrdersList, headers=header)
        except Exception:
            traceback.print_exc()
        df=pd.DataFrame(response.json()["orders"])
        print(df)
        pass

    def getServerTime(self):
        # Get server time
        # At the moment Nobitex API dosent have Server Tiem and Ping API endpoints
        pass

    def getCurrencyBallance(self,currency):
        """
        This function returns the balance of requested currency input e.g. BTC
        """
        df = AccountOperations.nobitexWalletLists(self.authenticationToken)
        balance = df.at[f'{currency.upper()}', 'balance']
        return balance

    def getActiveCurrencies(self):
        percissionsDf , activeCurrencies = MarketData.nobitexMarketOptions()
        return activeCurrencies

    def getPercissions(self):
        percissionsDf , activeCurrencies = MarketData.nobitexMarketOptions()
        return percissionsDf
