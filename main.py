from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()


def main():
    llm = ChatOpenAI()
    tools = [TavilySearch()]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    chain = agent_executor
    result = chain.invoke({"input": "What is the weather like today in Mar del Plata?"})
    print(result)


if __name__ == "__main__":
    main()
