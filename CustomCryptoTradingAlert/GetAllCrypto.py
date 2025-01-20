
from binance.client import Client
# Step 1: Binance API Credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def get_usdm_symbols():
    exchange_info = client.futures_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols'] if s['quoteAsset'] == 'USDT']
    # print(symbols)
    return symbols

print(get_usdm_symbols())
