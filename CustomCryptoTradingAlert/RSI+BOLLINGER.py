import time
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import smtplib
import os

# Step 1: Binance API Credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)


# Step 2: Function to fetch USD-M Futures symbols
def get_usdm_symbols():
    exchange_info = client.futures_exchange_info()
    symbols = [s["symbol"] for s in exchange_info["symbols"] if s["quoteAsset"] == "USDT"]
    return symbols


# Step 3: Function to Fetch Historical Data, Calculate RSI, and Bollinger Bands
def fetch_data_and_calculate_indicators(symbol):
    try:
        # Fetch historical candlestick data
        klines = client.get_klines(symbol=symbol, interval="1h", limit=100)  # Last 100 candles

        # Create a DataFrame for the price data
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])  # Ensure 'close' column is numeric

        # Calculate RSI using pandas-ta
        df["RSI"] = ta.rsi(df["close"], length=14)  # RSI with period 14

        # Calculate Bollinger Bands using pandas-ta
        bb = ta.bbands(df["close"], length=20, std=2)  # Bollinger Bands (20, 2)
        df["BB_Lower"] = bb["BBL_20_2.0"]  # Lower Band
        df["BB_Upper"] = bb["BBU_20_2.0"]  # Upper Band

        # Return the latest close price, RSI, and bands
        return df["close"].iloc[-1], df["RSI"].iloc[-1], df["BB_Lower"].iloc[-1], df["BB_Upper"].iloc[-1]
    except Exception as e:
        pass
        return None, None, None, None

# Step 4: Monitoring RSI and Bollinger Bands
def monitor_indicators_for_all_symbols():
    symbols = get_usdm_symbols()
    print(f"Monitoring RSI and Bollinger Bands for {len(symbols)} symbols in the USD-M Futures market...")
    while True:
        for symbol in symbols:
            try:
                close_price, rsi_value, lower_band, upper_band = fetch_data_and_calculate_indicators(symbol)
                if close_price is None or rsi_value is None or lower_band is None or upper_band is None:
                    continue  # Skip if calculation failed

                # Check combined conditions for lower threshold
                if rsi_value <= 20 and close_price < lower_band and symbol!="BONDUSDT":
                    print(f"⚠️ ALERT: {symbol} RSI is {rsi_value:.2f} (below threshold) "
                          f"and price is below the lower Bollinger Band!")
                    send_email_alert(symbol, close_price, rsi_value, lower_band, upper_band, "below")

                # Check combined conditions for upper threshold
                elif rsi_value >= 80 and close_price > upper_band and symbol!="BONDUSDT":
                    print(f"⚠️ ALERT: {symbol} RSI is {rsi_value:.2f} (above threshold) "
                          f"and price is above the upper Bollinger Band!")
                    send_email_alert(symbol, close_price, rsi_value, lower_band, upper_band, "above")

            except Exception as e:
                pass

        # Print a message to indicate the end of the current iteration
        print(f"Completed checking RSI and Bollinger Bands for all symbols in this iteration at {time.strftime('%H:%M:%S')}.")

        # Wait before the next iteration
        time.sleep(120)  # Check every minute

# Step 5: Send Email Alert
def send_email_alert(symbol, close_price, rsi_value, lower_band, upper_band, direction):
    sender_email = os.environ.get("EMAIL1")
    password = os.environ.get("PASS1")  # Replace with your app password
    receiver_email1 = os.environ.get("EMAIL1")
    receiver_email2 = os.environ.get("EMAIL2")

    subject = f"Combined RSI and Bollinger Bands Alert for {symbol}"
    if direction == "below":
        message = (f"The price of {symbol} is BELOW the lower Bollinger Band and RSI is below the threshold.\n\n"
                   f"Current Price: {close_price:.2f}\nRSI: {rsi_value:.2f}\nLower Band: {lower_band:.2f}\nUpper Band: {upper_band:.2f}")
    elif direction == "above":
        message = (f"The price of {symbol} is ABOVE the upper Bollinger Band and RSI is above the threshold.\n\n"
                   f"Current Price: {close_price:.2f}\nRSI: {rsi_value:.2f}\nLower Band: {lower_band:.2f}\nUpper Band: {upper_band:.2f}")

    email_message = f"Subject: {subject}\n\n{message}"

    try:
        # Connect to SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email1, email_message)
            server.sendmail(sender_email, receiver_email2, email_message)

        print(f"Email alert sent for {symbol} ({direction}).")
    except Exception as e:
        pass

# Run the monitoring function
monitor_indicators_for_all_symbols()
