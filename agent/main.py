from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from galileo.handlers.langchain import GalileoCallback

load_dotenv()

# Create callback - it will capture everything including tool calls
callback = GalileoCallback()


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


llm = ChatOpenAI(model="gpt-4", temperature=0.7)

SYSTEM_PROMPT = """You are a helpful financial advisor assistant. 
You provide stock investment advice and market analysis.
Always explain your reasoning clearly and include relevant data when available.
Be concise but thorough in your responses."""

agent = create_react_agent(
    model=llm,
    tools=[get_stock_advice],
    prompt=SYSTEM_PROMPT,
)

if __name__ == "__main__":
    # Pass callback in config to capture full trace (LLM calls + tool calls)
    result = agent.invoke(
        {"messages": [("user", "Should I buy AAPL?")]},
        config={"callbacks": [callback]}
    )
    final_message = result["messages"][-1]
    print(f"\nAgent Response:\n{final_message.content}")
