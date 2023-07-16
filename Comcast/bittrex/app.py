""" App module to demonstrate the usage of Bittrex Exchange Service. """

from market_detail_service import MarketDetailService
from market_symbol_service import MarketSymbolService


def main():
    """ Main function to demonstrate the usage of the market. """
    market_detail_service = MarketDetailService()
    market_symbol_service = MarketSymbolService()

    # Use the below services to perform actions
    market_detail = market_detail_service.get_market_detail()
    print("Market Details:", market_detail)

    symbol_detail = market_symbol_service.get_symbol_detail("BTC-USDT")
    print("Symbol Detail:", symbol_detail)


if __name__ == "__main__":
    main()
