
# Python Library For Using Nobitex Exchange APIs

## Description
NoBitex Trading python library is a powerful and flexible tool designed to automate cryptocurrency trading on the NoBitex exchange. This library can be used to design trading bots and softwares which work with Nobitex Rest API.

## Installation

Before you begin, ensure you meet the following requirements:

- You have installed the latest version of [Python](https://www.python.org/downloads/).
- You have a basic understanding of Python and its syntax.
- You have Pandas and Requests packages installed.

### Installing NoBitex API library

To install NoBitex API library, follow these steps:

1. Clone the repository:

```git clone https://github.com/4rdii/Nobitex-Python-API```

2. Change the directory to the project folder:

```cd Nobitex-Python-API```

3. Install the required packages:
```pip install -r requirements.txt```

   This will install the `requests` and `pandas` libraries, among others, as listed in the `requirements.txt` file.

### Setting Up API Credentials

To use the NoBitex python library, you will need valid API credentials for the NoBitex exchange. Set up the following environment variables with your credentials:
1. create .env file:
```touch .env```
2. in .env create envirtomental varibles such as:

NOBITEX_USERNAME="example@example.com"
NOBITEX_PASSWORD="pass"
NOBITEX_TOKEN="0"


3.set enviromental variables with command:
```source .env ```


## Prerequisites

- An active internet connection is required to communicate with the NoBitex API.
- Familiarity with Python programming is helpful for customizing and extending the library's functionalities.
- Access to a NoBitex account with the necessary permissions to execute trades.

### Development Tools

For development purposes, you may need the following tools:

- A code editor or Integrated Development Environment (IDE) like Visual Studio Code, PyCharm, or Atom.
- Version control software like Git for tracking changes and collaborating with others.

## Example File:
There is a File called Examples.py you can see how main clss is used, other functions in src folder are pretty easy to undrestand! please feel free to make an issue or a disscution if you have any problems!

## Contributing

Guidelines for contributing to your project.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Usefull Resources
1. Nobitex API docs [https://documenter.getpostman.com/view/5722122/Szmcayjw#c4f9d74b-02b8-427a-a675-14a1a5e5744b]
2. Nobitex API github [https://github.com/nobitex/docs-api]

## Contact
Ardeshir Gholami - agh1994@gmail.com

Project Link: [https://github.com/4rdii/Nobitex-Python-API]

## TO-DOS:
    1. finish unwritten functions/methods ✅ two functions remain
    2. write more tests
    3. Add more loggings

#### Tests to write:
    1. Unit tests:
        1. Authentication Tests:✅
            Test that your library correctly authenticates with the exchange's API using the provided API keys. ✅
            Verify that the library handles incorrect API keys or credentials gracefully.✅
        2. Response Parsing Tests:✅
            Test that your library can correctly parse API responses, including handling different data formats (JSON, XML) and extracting relevant information.✅
            Verify that the library can handle paginated responses and correctly process them.✅
        3. Utility Function Tests:( NO Util functions yet)
            If your library includes utility functions for tasks like calculating stop loss levels or determining market trends, write tests for these functions.
        4. Data Validation Tests:✅
            Test that your library validates input data before sending it to the API, ensuring that it meets the exchange's requirements.
        5. Environment Variable Tests:✅
            If your library uses environment variables for configuration, test that it falls back to default values or raises errors when required variables are missing.
    2. Intergration tests:
        1. Error Propagation Tests:
            Test how your library propagates errors received from the API to the calling code. This includes API errors, network errors, and timeouts.
            Test how your library handles API errors, such as rate limits, invalid parameters, or server downtime.
            Ensure that your library raises appropriate exceptions or returns meaningful error messages when an API call fails.
        2. Transaction Tests:✅
            Test that your library can execute transactions, such as buying and selling assets, and that the final state reflects the expected changes.
    3. Security tests:
        1. Authentication and Authorization Tests:
            Test that your library securely stores and transmits API keys and other sensitive credentials.
            Verify that the library checks for proper authorization before executing privileged operations.
        2. API Key Exposure Tests:✅
            Test that your library does not expose API keys in URLs, logs, or error messages.