#https://v2docs.galileo.ai/cookbooks/use-cases/agent-langchain | Following this video
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from galileo import galileo_context
from galileo.handlers.langchain import GalileoCallback
import os


load_dotenv()

#Define a Tool 
@tool
def greet(name: str) -> str: 
    """Say Hello to someone."""
    return f"Hello, {name}!"

with galileo_context(project="Financial Advisor Agent", log_stream="dev_main_ls"):
    agent = initialize_agent(
        tools=[greet],
        llm=ChatOpenAI(model="gpt-4", temperature=0.7, callbacks=[GalileoCallback()]),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

if __name__ == "__main__":
    result = agent.invoke({"input": "Say hello to Michael"})
    print(f"\nAgent Response:\n{result}")