import warnings
warnings.filterwarnings("ignore", module="urllib3")
import urllib3
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from galileo import GalileoLogger
from galileo import galileo_context

from galileo.handlers.langchain import GalileoCallback
from langchain_core.tools import tool 


load_dotenv()
print("Running Agent ....")

@tool
def add(x: float,y: float) -> float: 
    """" adds two numbers x and y together """ 
    return x +y 
@tool 
def subtract(x: float, y:float)-> float:
    """ subtracts y from x """ 
    return x - y





SYSTEM_PROMPT = """You are a helpful math assistant.
You can add and subtract numbers. Use the available tools to perform calculations.
Always show your work and explain what operation you're performing."""
   
   
create_galileo_session()

logger = GalileoLogger(project="Financial Advisor Agent", log_stream="dev")
callback = GalileoCallback(galileo_logger=logger)

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

agent = create_react_agent(
    model=llm,
    tools=[add, subtract],
    prompt=SYSTEM_PROMPT, 
)

result = agent.invoke({"messages": [("user", "What is 15 plus 27 minus 10")]},
config={"callbacks": [callback]}

)
print(result["messages"][-1].content)