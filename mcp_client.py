import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient

tavily_api_key = os.getenv("TAVILY_API_KEY")

client = MultiServerMCPClient(
    {
        "tavily":{
            "transport" : "streamable_http",
            "url" : f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}"
        }
    }

)

#this process is called tool discovery
# async def main():
#     tools = await client.get_tools()

#     for tool in tools:
        # print(tool)


# async def main():
#     tools = await client.get_tools()

#     search_tool = next(
#         tool
#         for tool in tools
#         if tool.name == "tavily_search"
#     )

#     result = await search_tool.ainvoke(
#         {
#             "query": "What is the capital of France?"
#         }
#     )

#     print(result)

search_tool = None

async def initialize_mcp():
    global search_tool
    if search_tool is not None:
        return
    
    tools = await client.get_tools()

    for tool in tools:
        if tool.name == "tavily_search":
            search_tool = tool
            break


async def tavily_mcp_search(query : str, days : int):
    await initialize_mcp()
    result = await search_tool.ainvoke(
        {
            "query": f"Get the itinerary for {query} for {days} days."
        }
    )
    return result

# if __name__ == "__main__":
#     asyncio.run(main())