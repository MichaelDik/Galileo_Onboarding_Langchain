"""Stock advice tool."""
import json
from langchain.agents import Tool
from galileo import log

STOCK_ADVICE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_stock_advice",
        "description": "Get stock investment advice for a given stock symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol (e.g., AAPL, GOOGL, MSFT)"
                }
            }
        }
    }
}

#@log(span_type="tool", name="get_stock_advice")
@log
def get_stock_advice(symbol: str = None) -> dict:
    """Get stock advice for a given stock symbol."""
    symbol = symbol or "AAPL"
    return {
        "symbol": symbol,
        "recommendation": "BUY",
        "target_price": 185.50,
        "current_price": 175.20,
        "confidence": "High",
        "reasoning": "Strong fundamentals, positive earnings growth, and favorable market conditions suggest upward momentum."
    }


# LangChain Tool wrapper for agent use

stock_advice_tool = Tool(
    name="get_stock_advice",
    func=lambda symbol: json.dumps(get_stock_advice(symbol)),
    description="Get stock investment advice for a given stock symbol (e.g., AAPL, GOOGL, MSFT). Returns recommendation, target price, confidence level, and reasoning."
)