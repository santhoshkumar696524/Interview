import hashlib
import hmac
import time
import requests
import auth_creds


class MarketDetailService:
    """Class for retrieving whole market information using the Bittrex API."""
    def __init__(self):
        self.api_key = auth_creds.get_auth_creds()["api_key"]
        self.api_secret = auth_creds.get_auth_creds()["api_secret"]

    def generate_signature(self, pre_sign):
        """Generates the API signature."""
        signature = hmac.new(
            bytes(self.api_secret, 'utf-8'),
            bytes(pre_sign, 'utf-8'),
            hashlib.sha512
        ).hexdigest()
        return signature

    def get_market_detail(self):
        """Gets the market detail for the entire market."""
        timestamp = str(int(time.time() * 1000))
        uri = "https://api.bittrex.com/v3/markets/summaries"
        method='GET'
        content_hash = hashlib.sha512().hexdigest()
        pre_sign = f"{timestamp}{uri}{method}{content_hash}"
        signature = self.generate_signature(pre_sign)

        headers = {
            "X-API-Key": self.api_key,
            "X-API-Timestamp": timestamp,
            "X-API-Content-Hash": content_hash,
            "X-API-Signature": signature
        }

        response = requests.get(uri, headers=headers,timeout=10)

        if response.status_code == 200:
            return response.json()

        raise ValueError(f"Error getting market detail: {response.status_code}")
