import warnings
warnings.filterwarnings("ignore")
import urllib3

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from galileo import GalileoLogger
from galileo.handlers.langchain import GalileoCallback

from tools.stock_advice import get_stock_advice
from tools.customer_info import get_customer_info
from tools.bank_account import get_bank_balance

load_dotenv()

# Create logger with project and session name
logger = GalileoLogger(
    project="Financial Advisor Agent",
    log_stream="dev"
)
#Dynmaically Create Session Name
logger.start_session(name="3 Tools Calls")

# Create callback with the logger
callback = GalileoCallback(galileo_logger=logger)

#Instance of OpenaAIs gpt 3 via langhcain wrapper
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

SYSTEM_PROMPT = """You are a helpful financial advisor assistant. 
You provide stock investment advice, customer information, and bank account details.
Always explain your reasoning clearly and include relevant data when available.
Be concise but thorough in your responses."""

financial_advisor_agent = create_react_agent(
    model=llm,
    tools=[get_stock_advice, get_customer_info, get_bank_balance],
    prompt=SYSTEM_PROMPT,
)

if __name__ == "__main__":
    
    
    messages = []  # Conversation history for multi-turn
    # Add user message to history
    messages.append(("user", "Hello, please tell me my bank balance"))
    
    # Pass callback in config to capture full trace (LLM calls + tool calls)
    financial_advisor_agent.invoke(
        {"messages": messages},
        config={"callbacks": [callback]}
    )


    messages.append(("user", "I am Michael"))

    financial_advisor_agent.invoke(
        {"messages": messages},
        config={"callbacks": [callback]}
    )

    messages.append(("user", "What is my customer information?"))

    financial_advisor_agent.invoke(
        {"messages": messages},
        config={"callbacks": [callback]}
    )

    messages.append(("user", "Is google a good buy?"))
    
    result = financial_advisor_agent.invoke(
        {"messages": messages},
        config={"callbacks": [callback]}
    )

    
    # Get AI response and add to history
    final_message = result["messages"][-1]
    messages.append(("assistant", final_message.content))
    
    print(f"\nAgent: {final_message.content}\n")
    
