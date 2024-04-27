# Pycrypto

## Description

This is a simple python GUI application that helps you keeping track of a crypto currency portfolio. It uses the CoinMarketCap API to get the latest prices of the coins and calculates the total value of your portfolio.

## Installation

To install the application, you need to have python3 installed on your machine. You can download it from the official website: https://www.python.org/downloads/

After you have installed python3, you can install the required packages by running the following command in the terminal:


```bash 
pip install -r requirements.txt
```

## Usage

To run the application, you need to run the following command in the terminal:

```bash
python main.py
```

After you run the command, the application will open and you can start adding your coins to the portfolio. Please do not forget to place the API key in the .env file as described in the .env.example file.

You can get the API key from the following website: https://coinmarketcap.com/api/. You need to create an account and then you can get the API key from the dashboard. 

You can make an executable file by using pyinstaller. You can install pyinstaller by running the following command in the terminal:

```bash
pip install pyinstaller
```

After you have installed pyinstaller, you can create an executable file by running the following command in the terminal:

```bash
pyinstaller --onefile main.py
```

After you run the command, you will find the executable file in the dist folder. You can run the executable file by double clicking on it. Make sure to place the .env file and the btc.png file in the same folder as the executable file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
