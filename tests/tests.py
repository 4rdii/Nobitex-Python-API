import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from src import AccountOperations as AO
###
key = os.getenv("NOBITEX_TOKEN")
# now = int(dt.now().timestamp())
# start = now - 60*60*10
# print(now,start)
AO.nobitexLogout(key)