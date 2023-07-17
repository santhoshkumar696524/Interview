import pytest
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


if __name__ == "__main__":
    pytest.main()
