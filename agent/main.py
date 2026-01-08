import warnings
import urllib3
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)

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
    log_stream="multi-turn-session"
)
#Dynmaically Create Session Name
logger.start_session(name="Logger Session Tutorial")

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
    print("Hello, how can I help you today? (type 'quit' to exit)\n")
    
    messages = []  # Conversation history for multi-turn
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q", "thank you", "goodbye"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        messages.append(("user", user_input))
        
        # Pass callback in config to capture full trace (LLM calls + tool calls)
        result = financial_advisor_agent.invoke(
            {"messages": messages},
            config={"callbacks": [callback]}
        )
        
        # Get AI response and add to history
        final_message = result["messages"][-1]
        messages.append(("assistant", final_message.content))
        
        print(f"\nAgent: {final_message.content}\n")
