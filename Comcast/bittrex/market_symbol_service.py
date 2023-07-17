import requests
import auth_creds

class MarketSymbolService:
    """Class for retrieving symbol details from a market using the Bittrex API."""

    def __init__(self):
        self.api_key = auth_creds.get_auth_creds()["api_key"]
        self.api_secret = auth_creds.get_auth_creds()["api_secret"]

    def get_symbol_detail(self, symbol):
        """Retrieve symbol detail from the entire market using the Bittrex API."""

        url = f"https://api.bittrex.com/v3/markets/{symbol}/summary"
        headers = {"X-API-Key": self.api_key, "X-API-Secret": self.api_secret}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200: return response.json()
            raise ValueError(f"http invoking error: {response.status_code}")
        except requests.exceptions.RequestException as error:
            raise Exception(f"Error on getting symbol details: {str(error)}") from error
