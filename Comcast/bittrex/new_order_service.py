import requests
import auth_creds
import time
import hashlib
import hmac


class NewOrderService:
    """Service for placing a new order."""

    def __init__(self):
        """Initialize the NewOrderService."""
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

    def place_new_order(self, order_payload):
        """Place a new order with the provided payload."""
        timestamp = str(int(time.time() * 1000))
        uri = "https://api.bittrex.com/v3/orders"
        method = 'GET'
        content_hash = hashlib.sha512().hexdigest()
        pre_sign = f"{timestamp}{uri}{method}{content_hash}"
        signature = self.generate_signature(pre_sign)

        headers = {
            "X-API-Key": self.api_key,
            "X-API-Timestamp": timestamp,
            "X-API-Content-Hash": content_hash,
            "X-API-Signature": signature
        }

        response = requests.post(uri, headers=headers, json=order_payload, timeout=10)

        if response.status_code == 200:
            return response.json()

        raise ValueError(f"Error placing new order: {response.status_code}")
