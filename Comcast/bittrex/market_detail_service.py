import requests
import auth_creds

class MarketDetailService:
    """Class for retrieving whole market information using the Bittrex API."""

    def __init__(self):
        self.api_key = auth_creds.get_auth_creds()["api_key"]
        self.api_secret = auth_creds.get_auth_creds()["api_secret"]

    def get_market_detail(self):
        """Retrieve market detail for whole market using the Bittrex API."""

        url = "https://api.bittrex.com/v3/markets/summaries"
        response = requests.get(url, headers={"X-API-Key": self.api_key, "X-API-Secret": self.api_secret}, timeout=10)

        if response.status_code == 200:
            return response.json()

        raise ValueError(f"Error getting whole market detail: {response.status_code}")
