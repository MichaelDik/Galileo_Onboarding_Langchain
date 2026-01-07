from galileo.handlers.langchain import GalileoCallback
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from galileo import GalileoLogger


#create a custom logger 
logger = GalileoLogger(project="my-project", log_stream="my-log-stream")

# Create a callback handler
callback = GalileoCallback(galileo_logger=logger)

# Initialize the LLM with the callback
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, callbacks=[callback])

# Create a message with the user's query
messages = [
    HumanMessage(content="What is 2+2?")
]

# Make the API call
response = llm.invoke(messages)

print(response.content)