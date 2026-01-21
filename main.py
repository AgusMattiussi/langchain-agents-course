from dotenv import load_dotenv
from langchain_classic.agents.format_scratchpad import format_log_to_str
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import tool, render_text_description, Tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import List, Union
from callbacks import AgentCallbackHandler

load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Return the length of the text by characters."""
    text = text.strip('\n').strip('"').strip("'")
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    """Find a tool by name in the list of tools."""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")

def main():
    tools = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """
    
    # ==================== PROMPT SETUP ====================
    # Create a PromptTemplate from the template string and pre-fill (partial) some variables:
    # - render_text_description(tools): Converts the list of tools into a human-readable text
    #   description that will be inserted into the {tools} placeholder in the template
    # - tool_names: Creates a comma-separated string of tool names (e.g., "get_text_length")
    #   for the {tool_names} placeholder, telling the LLM which actions it can take
    prompt = PromptTemplate.from_template(template).partial(
        tools=render_text_description(tools), 
        tool_names=", ".join([tool.name for tool in tools])
    )
    
    # ==================== LLM CONFIGURATION ====================
    # - stop: Defines stop sequences - the LLM will stop generating text when it encounters
    #   "\nObservation" or "Observation". This is crucial for ReAct agents because the LLM
    #   should stop after generating an Action and wait for the actual tool observation
    # - callbacks: List of callback handlers that get triggered during LLM execution
    #   (AgentCallbackHandler likely logs or tracks the agent's actions)
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0, 
        stop=["\nObservation", "Observation"],
        callbacks=[AgentCallbackHandler()]
    )
    
    # ==================== AGENT CHAIN DEFINITION ====================
    # intermediate_steps: A list that stores the history of (AgentAction, observation) tuples.
    # This serves as the agent's "memory" of what actions it has taken and what results it got,
    # allowing it to reason about previous steps when deciding the next action.
    intermediate_steps = []
    
    agent = (
        # Input Preprocessing Dictionary
        # This dictionary defines how to extract and transform input values before passing to the prompt.
        # Each key-value pair maps a prompt variable to a lambda function that extracts it from input:
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]), # This creates a readable log of previous Thought/Action/Observation sequences that gets inserted into the prompt, giving the LLM context of past reasoning
        }
        | prompt
        | llm
        # ReActSingleInputOutputParser parses the LLM's text output and extracts it into either:
        # - AgentAction: Contains the tool name and tool input the agent wants to use
        # - AgentFinish: Contains the final answer when the agent is done reasoning
        | ReActSingleInputOutputParser()
    )

    # ==================== AGENT EXECUTION LOOP ====================
    # agent_step: Holds the current result from the agent (either an action to take or final answer).
    agent_step = ""

    # Main agent loop: Keep running until the agent outputs an AgentFinish (final answer).
    # This implements the ReAct loop: Reason -> Act -> Observe -> Repeat
    while not isinstance(agent_step, AgentFinish):
        # Invoke the agent chain with the current input and scratchpad (history of steps).
        # The result is either:
        # - AgentAction: The agent wants to use a tool (contains tool name and input)
        # - AgentFinish: The agent has determined the final answer
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the word: DOG",
                # Pass the accumulated history of (action, observation) pairs
                "agent_scratchpad": intermediate_steps,
            }
        )
        print(agent_step)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            # Execute the tool by calling its underlying function (.func) with the input.
            # The result (observation) is what the tool returns (e.g., 3 for len("DOG"))
            observation = tool_to_use.func(str(tool_input))
            print(f"{observation=}")
            # Append this action-observation pair to the intermediate_steps history.
            # On the next loop iteration, this will be included in the agent_scratchpad,
            # allowing the agent to see and reason about what it learned from this tool call
            intermediate_steps.append((agent_step, str(observation)))

    # ==================== FINAL OUTPUT ====================
    if isinstance(agent_step, AgentFinish):
        print(agent_step.return_values)

    
if __name__ == "__main__":
    main()