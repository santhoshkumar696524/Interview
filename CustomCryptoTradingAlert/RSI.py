import os
import time
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import smtplib

# Step 1: Binance API Credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

# Step 2: Parameters for RSI Calculation
interval = "1h"  # Timeframe (e.g., 1m, 5m, 1h, 1d)
rsi_period = 14  # Default RSI period
lower_threshold = 20  # RSI threshold for oversold alert
higher_threshold = 80  # RSI threshold for overbought alert

# Step 3: Get All Symbols in USD-M Futures Market
def get_usdm_symbols():
    exchange_info = client.futures_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols'] if s['quoteAsset'] == 'USDT']
    return symbols


# Step 4: Function to Fetch Historical Data and Calculate RSI
def fetch_data_and_calculate_rsi(symbol):
    try:
        # Fetch historical candlestick data
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=100)  # Last 100 candles

        # Create a DataFrame for the price data
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])  # Ensure 'close' column is numeric

        # Calculate RSI using pandas-ta
        df["RSI"] = ta.rsi(df["close"], length=rsi_period)

        # Return the latest RSI value
        return df["RSI"].iloc[-1]  # Last RSI value
    except Exception as e:
        pass
        return None


# Step 5: Monitoring and Alert
def monitor_rsi_for_all_symbols():
    symbols = get_usdm_symbols()
    print(f"Monitoring RSI for {len(symbols)} symbols in the USD-M Futures market...")
    while True:
        for symbol in symbols:
            try:
                rsi_value = fetch_data_and_calculate_rsi(symbol)
                if rsi_value is None:
                    continue  # Skip if RSI calculation failed

                # Check if RSI is below or above the thresholds
                if rsi_value <= lower_threshold:
                    print(f"⚠️ ALERT: RSI is {rsi_value:.2f} (below {lower_threshold}) for {symbol}!")
                    # send_email_alert(symbol, rsi_value, "below")

                elif rsi_value >= higher_threshold:
                    print(f"⚠️ ALERT: RSI is {rsi_value:.2f} (above {higher_threshold}) for {symbol}!")
                    # send_email_alert(symbol, rsi_value, "above")

            except Exception as e:
                pass
        # Print a message to indicate the end of the current iteration
        print(f"Completed checking RSI for all symbols in this iteration at {time.strftime('%H:%M:%S')}.")

        # Wait before the next iteration
        time.sleep(120)  # Check every minute


# Step 6: Email Alert Function
def send_email_alert(symbol, rsi_value, condition):
    sender_email = os.environ.get("EMAIL1")
    password = os.environ.get("PASS1")  # Replace with your app password
    receiver_email1 = os.environ.get("EMAIL1")
    receiver_email2 = os.environ.get("EMAIL2")

    if condition == "below":
        subject = f"RSI Alert: Oversold for {symbol}"
        message = f"RSI for {symbol} has dropped below {lower_threshold}. Current RSI: {rsi_value:.2f}."
    elif condition == "above":
        subject = f"RSI Alert: Overbought for {symbol}"
        message = f"RSI for {symbol} has risen above {higher_threshold}. Current RSI: {rsi_value:.2f}."

    email_message = f"Subject: {subject}\n\n{message}"

    # Connect to SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email1, email_message)
        server.sendmail(sender_email, receiver_email2, email_message)


# Run the monitoring function
monitor_rsi_for_all_symbols()
