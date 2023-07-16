import pytest
from market_detail_service import MarketDetailService
from market_symbol_service import MarketSymbolService


def test_get_market_detail(market_detail_service):
    """Test the get_market_detail method of MarketDetailService."""
    market_detail = market_detail_service.get_market_detail()

    assert market_detail is not None
    assert len(market_detail) > 0


def test_get_symbol_detail(symbol_detail_service):
    """Test the get_symbol_detail method of MarketSymbolService."""
    symbol_detail = symbol_detail_service.get_symbol_detail("BTC-USDT")

    assert symbol_detail is not None
    assert "symbol" in symbol_detail


if __name__ == "__main__":
    import subprocess

    subprocess.run(["pylint", "auth_creds.py", "market_symbol_service.py", "market_detail_service.py", "test_services.py"], check=True)
    subprocess.run(["flake8", "auth_creds.py", "market_symbol_service.py", "market_detail_service.py", "test_services.py"], check=True)
    pytest.main()
