import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
from src import TradingOperations as TO
from src import AccountOperations as AO
load_dotenv()
username = os.getenv("NOBITEX_USERNAME")
password = os.getenv("NOBITEX_PASSWORD")
Trader = TO.TradingOperations(username=username,
                           password=password,
                           twoFactorAuthentication="617864",
                           remember="no")
print(Trader.authenticationToken)

id = Trader.placeLimitOrder("buy","usdt","rls",550000,100)
id = Trader.placeMarketExecutionOrder("buy","usdt","rls",10)
Trader.cancelOrder(id)
Trader.getOrderStatus(id)
btc_balance = Trader.getCurrencyBallance("btc")
print(btc_balance)
Trader.getOrdersList()
Trader.getActiveCurrencies()
Trader.getPercissions()
Trader.logout()
