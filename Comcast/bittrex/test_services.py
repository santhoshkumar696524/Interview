"""
Test module for testing market services.

This module contains test cases for the market services, including the `MarketDetailService`
and `MarketSymbolService` classes. Each test case validates the functionality of specific
methods in these services.

"""
import pytest
import time
from market_detail_service import MarketDetailService
from market_symbol_service import MarketSymbolService


def test_get_market_detail():
    """Test the get_market_detail method of MarketDetailService."""
    market_detail_service = MarketDetailService()
    market_detail = market_detail_service.get_market_detail()

    assert market_detail is not None
    assert len(market_detail) > 0


def test_get_symbol_detail():
    """Test the get_symbol_detail method of MarketSymbolService."""
    market_symbol_service = MarketSymbolService()
    symbol_detail = market_symbol_service.get_symbol_detail("BTC-USDT")

    assert symbol_detail is not None
    assert "symbol" in symbol_detail

def test_load_test():
    market_detail_service = MarketDetailService()
    total_response_time,num_requests=0,10

    for _ in range(num_requests):
        start_time = time.time()
        market_detail = market_detail_service.get_market_detail()
        end_time = time.time()

        response_time = end_time - start_time
        total_response_time += response_time

    average_response_time = total_response_time / num_requests
    print(f"Average Response Time: {average_response_time} seconds")

    assert average_response_time < 2.0

def test_check_each_value_present():
    """Test if each value in the market detail is present."""
    market_detail_service = MarketDetailService()
    market_detail = market_detail_service.get_market_detail()

    assert all(key in market_detail[0] for key in ["symbol", "high", "low", "volume"])

if __name__ == "__main__":
    pytest.main()
