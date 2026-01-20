from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
from schemas import AgentResponse

load_dotenv()


# Custom search tool
# from tavily import TavilyClient
# tavily_client = TavilyClient()
# @tool
# def search(query: str) -> str:
#     """
#     Tool to search the web for the given query.
#     Args:
#         query (str): The query to search for.
#     Returns:
#         str: The search results.
#     """
#     print(f"Searching for: {query}")
#     return tavily_client.search(query=query)


def main():
    llm = ChatOpenAI()
    agent = create_agent(
        model=llm, 
        tools=[TavilySearch()],
        response_format=AgentResponse
    )
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="search for 3 job postings for an ai engineer in Argentina on linkedin and list their details"
                )
            ]
        }
    )
    # Access structured response from the agent
    structured = result.get("structured_response", None)
    print(structured if structured is not None else result)


if __name__ == "__main__":
    main()
