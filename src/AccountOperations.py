import warnings
warnings.filterwarnings("ignore")
import requests
import traceback
import pandas as pd
import os


"""
    @title Python functions for Nobitex.com APIs
    @author Ardeshir Gholami https://github.com/4rdii
    @notice Take care Using your account with real money this repo is Under development!!
"""
class CustomError(Exception):
    """A custom exception for handling specific error conditions."""
    pass

def nobitexLogin(username, password, twoFactorAuthentication="0",remember="yes"):
    """
    Logins to Nobitex Account then returns the authentication token
        1.if you have 2nd Authentication On use authToken as a string
        2.You can change remember to "no" if you want a 4h token
    """
    loginURL = "https://api.nobitex.ir/auth/login/"
    if twoFactorAuthentication!="0":
        header = {"X-TOTP": twoFactorAuthentication}
    else:
        header = {}
    payLoad = {
        "username": f"{username}",
        "password": f"{password}",
        "captcha": "api",
        "remember": remember
    }
    try:
        response = requests.post(url=loginURL, data=payLoad, headers=header)
        response_json = response.json()
        if 'key' not in response_json:
            if "error" in response_json or "non_field_errors" in response_json:
                error = response_json
            raise KeyError(f"Login Failed! {error} ")
        return response_json["key"]

    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the KeyError specifically if needed
        if isinstance(e, KeyError):
            # Handle the KeyError, possibly by raising a custom exception
            raise CustomError(f"Login Failed! {error} ")
        # Re-raise the exception to be caught by the caller
        raise

    # try:
    #     response = requests.post(url=loginURL, data=payLoad, headers=header)
    #     print(response.json())
    #     return response.json()["key"]

    # except Exception:
    #     traceback.print_exc()
    #     return response.json()

def nobitexLogout(key):
    """ This function burns the existing Authentication token"""
    logoutURL = "https://api.nobitex.ir/auth/logout/"
    header = {"Authorization": f"Token {key}"}
    try:
        response = requests.post(url=logoutURL, headers=header)
        try:
            print(response.json()["message"])
        except KeyError:
            print(response.json()["detail"])
        return True
    except Exception:
        traceback.print_exc()
        return False

def nobitexGetProfileData(key):
    """ Getting and Printing Profile Data"""
    getProfileDataURL = "https://api.nobitex.ir/users/profile"
    header = {"Authorization": f"Token {key}"}
    try:
        response = requests.post(url=getProfileDataURL, headers=header)
        print(response.json())
        ### @dev Note: Add logging  
    except Exception:
        traceback.print_exc()

def nobitexGetProfileLimitations(key):
    """ Getting and Printing Profile Limitations
    'limitations': {'userLevel': 'level2', 'features': {'crypto_trade': False, 'rial_trade': False, 'coin_deposit': False, 'rial_deposit': False, 'coin_withdrawal': False, 'rial_withdrawal': False}, 'limits': {'withdrawRialDaily': {'used': '0', 'limit': '3000000000'}, 'withdrawCoinDaily': {'used': '0', 'limit': '2000000000'}, 'withdrawTotalDaily': {'used': '0', 'limit': '5000000000'}, 'withdrawTotalMonthly': {'used': '0', 'limit': '150000000000'}}, 'depositLimits': {'depositRialDaily': {'used': 250000000, 'limit': '250000000'}}}

    """
    getProfileLimitationsURL = "https://api.nobitex.ir/users/limitations"
    header = {"Authorization": f"Token {key}"}
    try:
        response = requests.post(url=getProfileLimitationsURL, headers=header)
        print(response.json()["limitations"])
        ### @dev Note: Add limitation custom errors  
    except Exception:
        traceback.print_exc()
        return(Exception)
    
def nobitexAddBankAccountWithCardNumebr(key,cardNumber,bankName):
    """ Adding Bank Card to Account using SHOMARE KART
        @dev: this function is Not tested use at your own discretion
    """
    
    addBankCardURL = "https://api.nobitex.ir/users/cards-add"
    header = {"Authorization": f"Token {key}"}
    payLoad = {
        "number": f"{cardNumber}",
        "bank": f"{bankName}",
    }
    try:
        response = requests.post(url=addBankCardURL, headers=header,data=payLoad)
        if(response.json()["status"]== "ok"):
            print(f"Your Card with Number:{cardNumber} in {bankName} Bank was added to your Nobitex Account")
    except Exception:
        traceback.print_exc()

def nobitexAddBankAccountWithAccountNumber(key,shabaNumber,accountNumber):
    """ Adding Bank Card to Account using SAEBA and SHOMARE HESAB
        @dev: this function is Not tested use at your own discretion
    """
    
    addBankCardURL = "https://api.nobitex.ir/users/accounts-add"
    header = {"Authorization": f"Token {key}"}
    payLoad = {
        "shaba": f"{shabaNumber}",
        "number": f"{accountNumber}",
    }
    try:
        response = requests.post(url=addBankCardURL, headers=header,data=payLoad)
        if(response.json()["status"]== "ok"):
            print(f"Your Card with SHABA:{shabaNumber} and Account Number {accountNumber}  was added to your Nobitex Account")
    except Exception:
        traceback.print_exc()

def nobitexWalletLists(key,):
    """ gets and returns a df of active wallets of the user"""
    walletListURL = "https://api.nobitex.ir/v2/wallets?currencies"
    header = {"Authorization": f"Token {key}"}
    try:
        response = requests.post(url=walletListURL, headers=header)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise CustomError("Failed to retrieve wallet lists")

    data = response.json()
    if 'wallets' not in data:
        raise CustomError("Expected 'wallets' key in the response JSON")

    wallets = data['wallets']   
    df = pd.DataFrame(wallets)
    df = df.transpose()
    return df
