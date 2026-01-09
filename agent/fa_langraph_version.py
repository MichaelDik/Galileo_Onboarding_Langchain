from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

load_dotenv()


# Simple tool
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny and 72°F"


tools = [get_weather]
tool_map = {t.name: t for t in tools}


# State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# LLM with tool
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)


# Agent node
def agent(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Tool node - execute tool calls
def tool_node(state: State):
    results = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tool_map[tool_call["name"]].invoke(tool_call["args"])
        results.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
    return {"messages": results}


# Router
def should_continue(state: State):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


# Build graph
graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile()


if __name__ == "__main__":
    # Save graph visualization as PNG
    png_data = app.get_graph().draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(png_data)
    print("Graph saved to agent_graph.png")
    
    # Run the agent
    result = app.invoke({"messages": [HumanMessage(content="What's the weather in Paris?")]})
    print(result["messages"][-1].content)
