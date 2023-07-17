""" App module to demonstrate the usage of Bittrex Exchange Service. """

from market_detail_service import MarketDetailService
from market_symbol_service import MarketSymbolService
from new_order_service import NewOrderService

def main():
    """ Main function to demonstrate the usage of the market. """
    market_detail_service = MarketDetailService()
    market_symbol_service = MarketSymbolService()

    # Use the below services to perform actions
    market_detail = market_detail_service.get_market_detail()
    print("Market Details:", market_detail)

    symbol_detail = market_symbol_service.get_symbol_detail("BTC-USDT")
    print("Symbol Detail:", symbol_detail)

    new_order_service = NewOrderService()

    order_payload = {
        "marketSymbol": "BTC-USDT",
        "direction": "BUY",
        "type": "LIMIT",
        "quantity": 0.5,
        "limit": 35000.0,
        "timeInForce": "GOOD_TIL_CANCELLED",
        "clientOrderId": "12345",
        "useAwards": False
    }

    response = new_order_service.place_new_order(order_payload)
    print("New Order Response:", response)

if __name__ == "__main__":
    main()
