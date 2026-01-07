#https://v2docs.galileo.ai/cookbooks/use-cases/agent-langchain | Following this video
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from galileo import galileo_context
from galileo.handlers.langchain import GalileoCallback
from galileo import GalileoLogger

from tools.stock_advice import stock_advice_tool


load_dotenv()

context = galileo_context.init(project="Financial Advisor Agent", log_stream="dev_main_ls")

logger= GalileoLogger()

agent = initialize_agent(
    tools=[stock_advice_tool],
    llm=ChatOpenAI(model="gpt-4", temperature=0.7, callbacks=[GalileoCallback(galileo_logger=logger)]),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

if __name__ == "__main__":
    result = agent.invoke({"input": "Get stock advice for AAPL and explain the recommendation."})
    print(f"\nAgent Response:\n{result['output']}")
