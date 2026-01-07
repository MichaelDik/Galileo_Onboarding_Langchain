"""Stock advice tool."""
from langchain_core.tools import tool


@tool
def get_stock_advice(symbol: str) -> dict:
    """Get stock investment advice for a given stock symbol.
    
    Args:
        symbol: The stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
    
    Returns:
        Investment recommendation with target price, confidence, and reasoning.
    """
    return {
        "symbol": symbol,
        "recommendation": "BUY",
        "target_price": 185.50,
        "current_price": 175.20,
        "confidence": "High",
        "reasoning": "Strong fundamentals, positive earnings growth, and favorable market conditions suggest upward momentum."
    }
