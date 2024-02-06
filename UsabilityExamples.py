import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
from src import TradingOperations as TO

load_dotenv()
username = os.getenv("NOBITEX_USERNAME")
password = os.getenv("NOBITEX_PASSWORD")

Trader = TO.TradingOperations(username=username,
                           password=password,
                           twoFactorAuthentication="",
                           remember="no")
#print(Trader.authenticationToken)

id = Trader.placeLimitOrder("buy","usdt","rls","550000","100")
Trader.cancelOrder(1304616040)
Trader.getOrderStatus(id)
Trader.logout()