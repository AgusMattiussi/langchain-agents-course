from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

load_dotenv()


def main():
    llm = ChatOpenAI()
    tools = [TavilySearch()]
    # prompt = hub.pull("hwchase17/react")

    # ==================== OUTPUT PARSER SETUP ====================
    # PydanticOutputParser: A LangChain utility that parses LLM text output into structured Pydantic models.
    # - pydantic_object: The Pydantic class (AgentResponse) that defines the expected output structure.
    # - This parser will validate and convert the agent's raw text response into an AgentResponse instance,
    #   ensuring type safety and structured data access.
    output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

    # ==================== PROMPT TEMPLATE SETUP ====================
    # PromptTemplate: A LangChain class that creates dynamic prompts with variable placeholders.
    # - template: The base prompt string containing the ReAct (Reasoning + Acting) logic pattern.
    #   ReAct is a paradigm where the agent reasons about what to do, takes an action (uses a tool),
    #   observes the result, and repeats until it can provide a final answer.
    # - input_variables: The list of variables that MUST be provided at runtime:
    #   * "input": The user's question or task
    #   * "agent_scratchpad": The running history of the agent's thoughts, actions, and observations
    #   * "tool_names": The names of available tools the agent can use
    # - .partial(): Pre-fills certain template variables with fixed values, here we inject:
    #   * "format_instructions": Auto-generated instructions from the output parser telling the LLM
    #     exactly how to format its response to match the AgentResponse Pydantic schema
    react_prompt_with_format_instructions = PromptTemplate(
        template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
        input_variables=["input", "agent_scratchpad", "tool_names"],
    ).partial(format_instructions=output_parser.get_format_instructions())

    # ==================== REACT AGENT CREATION ====================
    # create_react_agent: Factory function that creates a ReAct agent combining:
    # - llm: The language model (ChatOpenAI) that will do the reasoning and decision-making
    # - tools: List of tools the agent can invoke (here: TavilySearch for web searches)
    # - prompt: The prompt template that guides the agent's behavior and output format
    # Returns: A Runnable agent that follows the ReAct pattern (Thought -> Action -> Observation loop)
    agent = create_react_agent(llm, tools, prompt=react_prompt_with_format_instructions)

    # ==================== AGENT EXECUTOR SETUP ====================
    # AgentExecutor: A runtime wrapper that handles the execution loop of the agent.
    # - agent: The ReAct agent created above
    # - tools: The same tools list, needed to actually execute the actions the agent decides to take
    # - verbose=True: Enables detailed logging of each step (thoughts, actions, observations)
    #   This is useful for debugging and understanding how the agent reasons through a problem.
    # The executor manages: tool invocation, error handling, iteration limits, and output parsing.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # ==================== CHAIN DEFINITION ====================
    # RunnableLambda: A LangChain construct to wrap a Python function into a Runnable.
    # - extract_output: Extracts the 'output' key from the agent's result dictionary.
    # - parse_output: Parses the extracted output string into the Pydantic AgentResponse object using the output_parser.
    # The chain pipes the agent's execution through these post-processing steps.
    extract_output = RunnableLambda(lambda x: x["output"])
    parse_output = RunnableLambda(lambda x: output_parser.parse(x))
    chain = agent_executor | extract_output | parse_output

    # ==================== CHAIN INVOCATION ====================
    # .invoke(): Executes the chain synchronously with the provided input dictionary.
    # - "input": The user's question that the agent will try to answer
    # The agent will:
    # 1. Read the input and decide what action to take (e.g., search the web)
    # 2. Execute the action using the appropriate tool (TavilySearch)
    # 3. Observe the result and decide if it has enough info to answer
    # 4. Either repeat steps 1-3 or provide a final answer
    # Returns: A dictionary containing the agent's final response and intermediate steps
    result = chain.invoke({"input": "What is the weather like today in Mar del Plata?"})
    print(result)


if __name__ == "__main__":
    main()
