import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os
from datetime import datetime as dt

"""
    @title Python functions for Nobitex.com APIs
    @author Ardeshir Gholami https://github.com/4rdii
    @notice Take care Using your account with real money this repo is Under development!!
"""

def nobitexPairStats(sourceCurrency="btc", destinationCurrency="rls"):
    """
    This function gives the Stats for a specifix token Pair in Dataframe with these headers:
        ['btc-rls.isClosed', 'btc-rls.bestSell', 'btc-rls.bestBuy',
       'btc-rls.volumeSrc', 'btc-rls.volumeDst', 'btc-rls.latest',
       'btc-rls.mark', 'btc-rls.dayLow', 'btc-rls.dayHigh', 'btc-rls.dayOpen',
       'btc-rls.dayClose', 'btc-rls.dayChange']
    Default inputs is btc/rls pair    
    """
    statsURL = "https://api.nobitex.ir/market/stats"
    payLoad = {"srcCurrency": sourceCurrency, "dstCurrency": destinationCurrency}

    try:
        response = requests.post(url=statsURL, data=payLoad)
    except Exception:
        traceback.print_exc()
    marketData = response.json()["stats"]
    df = pd.DataFrame.from_dict(
        pd.json_normalize(marketData),
        orient="columns",
    )
    return df

def nobitexOrderBook(symbol = "BTCIRT"):
    """
    This function gives last bid/ask for a specific crypto pair
    """
    orderBookURL = f"https://api.nobitex.ir/v2/orderbook/{symbol}"
    try:
        response =requests.get(url=orderBookURL)
        lastUpdatedTimeStamp = response.json()["lastUpdate"]/1000
        print("got the ask/bids at: ",dt.fromtimestamp(lastUpdatedTimeStamp))
    except Exception:
        traceback.print_exc()
    df = pd.DataFrame.from_dict(
    pd.json_normalize(response.json()),
    orient="columns",
    )
    return df

def nobitexTradesHistory(symbol = "BTCIRT"):
    """
    This function gives last Trades for a specific crypto pair
    """
    tradeHistoryURL = f"https://api.nobitex.ir/v2/trades/{symbol}"
    try:
        response =requests.get(url=tradeHistoryURL)
    except Exception:
        traceback.print_exc()
    df = pd.DataFrame.from_dict(
    pd.json_normalize(response.json()["trades"]),
    orient="columns",
    )
    print(df)
    return df

def nobitexCandleSticks(startTimeStamp,endTimeStamp,symbol = "BTCIRT",resolution ="60"):
    """
    This function gives OHLC for a specific crypto pair from a starting time to an ending time
    only has daily and 1h candles
    returns a pandas dataframe of ohlcv for candlesticks
    """
    OHLCURL = f'https://api.nobitex.ir/market/udf/history?symbol={symbol}&resolution={resolution}&from={startTimeStamp}&to={endTimeStamp}'
    
    try:
        response =requests.get(url=OHLCURL)
        json_obj = response.json()
    except Exception:
        traceback.print_exc()
    df = pd.DataFrame(json_obj)
    print(df)
    return df

def nobitexMarketOptions():
    """
    This function returns Market Options such as Amount Percisions and Price Percisions as a Dataframe and a list for active Currencies

    """
    activeCurrencies=[]
    amountPrecisions=[]
    pricePrecisions=[]
    marketOptionsURL = "https://api.nobitex.ir/v2/options"
    try:
        response = requests.get(url=marketOptionsURL)
    except Exception:
        traceback.print_exc()
        return 0
    data = response.json()["nobitex"]
    keys_to_keep = ["activeCurrencies","amountPrecisions","pricePrecisions"]
    keys_list = data.copy().keys()
    for key in keys_list:
        if key in keys_to_keep:
            continue
        else:
            del data[key]
    activeCurrencies = data["activeCurrencies"]
    del data["activeCurrencies"]
    percisionsDf = pd.DataFrame(data)

    return percisionsDf , activeCurrencies

