from galileo.handlers.langchain import GalileoCallback
from galileo import GalileoLogger

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

SYSTEM_PROMPT = "You are a financcial advisor assistant. Answer clearly and concisely."

logger = GalileoLogger(project="my-project", log_stream="my-log-stream")

callback = GalileoCallback(galileo_logger=logger)

llm = ChatOpenAI(model="gpt-4o", temperature=0.7, callbacks=[callback])

messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content="Is Apple a good investment?")
]

response = llm.invoke(messages)

print(response.content)


