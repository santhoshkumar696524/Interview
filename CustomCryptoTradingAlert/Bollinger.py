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

# Step 2: Function to fetch USD-M Futures symbols
def get_usdm_symbols():
    exchange_info = client.futures_exchange_info()
    symbols = [s["symbol"] for s in exchange_info["symbols"] if s["quoteAsset"] == "USDT"]
    return symbols

# Step 3: Function to Fetch Historical Data and Calculate Bollinger Bands
def fetch_data_and_calculate_bb(symbol):
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

        # Calculate Bollinger Bands using pandas-ta
        bb = ta.bbands(df["close"], length=20, std=2)  # Bollinger Bands (20, 2)
        df["BB_Lower"] = bb["BBL_20_2.0"]  # Lower Band
        df["BB_Upper"] = bb["BBU_20_2.0"]  # Upper Band
        df["close"] = df["close"]

        # Return the latest close price and bands
        return df["close"].iloc[-1], df["BB_Lower"].iloc[-1], df["BB_Upper"].iloc[-1]
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None

# Step 4: Monitoring and Alert for Bollinger Bands
def monitor_bb_for_all_symbols():
    symbols = get_usdm_symbols()
    print(f"Monitoring Bollinger Bands for {len(symbols)} symbols in the USD-M Futures market...")
    while True:
        for symbol in symbols:
            try:
                close_price, lower_band, upper_band = fetch_data_and_calculate_bb(symbol)
                if close_price is None or lower_band is None or upper_band is None:
                    continue  # Skip if calculation failed

                print(f"Symbol: {symbol}, Close: {close_price:.2f}, Lower: {lower_band:.2f}, Upper: {upper_band:.2f}")

                # Check if price is below the lower band or above the upper band
                if close_price < lower_band:
                    print(f"⚠️ ALERT: {symbol} is below the lower Bollinger Band!")
                    # send_email_alert(symbol, close_price, "below", lower_band, upper_band)

                elif close_price > upper_band:
                    print(f"⚠️ ALERT: {symbol} is above the upper Bollinger Band!")
                    # send_email_alert(symbol, close_price, "above", lower_band, upper_band)

            except Exception as e:
                print(f"Error monitoring {symbol}: {e}")

        # Print a message to indicate the end of the current iteration
        print("Completed checking Bollinger Bands for all symbols in this iteration.")

        # Wait before the next iteration
        time.sleep(180)  # Check every minute

# Step 5: Send Email Alert
def send_email_alert(symbol, close_price, direction, lower_band, upper_band):
    sender_email = "your_email@gmail.com"
    receiver_email = "your_email@gmail.com"
    password = "your_email_password"  # Replace with your email's app password

    subject = f"Bollinger Bands Alert for {symbol}"
    if direction == "below":
        message = (f"The price of {symbol} is BELOW the lower Bollinger Band.\n\n"
                   f"Current Price: {close_price:.2f}\nLower Band: {lower_band:.2f}\nUpper Band: {upper_band:.2f}")
    elif direction == "above":
        message = (f"The price of {symbol} is ABOVE the upper Bollinger Band.\n\n"
                   f"Current Price: {close_price:.2f}\nLower Band: {lower_band:.2f}\nUpper Band: {upper_band:.2f}")

    email_message = f"Subject: {subject}\n\n{message}"

    try:
        # Connect to SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_message)
        print(f"Email alert sent for {symbol} ({direction}).")
    except Exception as e:
        print(f"Failed to send email for {symbol}: {e}")

# Run the monitoring function
monitor_bb_for_all_symbols()
