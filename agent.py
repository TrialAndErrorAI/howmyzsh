from langchain import OpenAI
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.tools.human.tool import HumanInputRun

from memory import get_memory

tools = [
    Tool(
        name = "OhMyZsh QA System",
        func=get_memory().agent_tool(),
        description="This is your primary tool. You always start here. This is the Oh My Zsh (ohmyzsh) wiki. It may not have all the info."
        
    ),
    Tool(
        name = "Google Search",
        func=GoogleSearchAPIWrapper(k=1).run,
        description="This is google search across the internet. Useful when searching OhMyZsh QA System does not give the answer. Use for OhMyZsh or shell realted queries only"
    ),
    # Tool(
    #     description="You can ask a human for guidance when you think you got stuck or you are not sure what to do next. The input should be a question for the human.",
    #     func = HumanInputRun().run,
    #    name="Human" 
    #     ),
]

agent = initialize_agent(
    llm=OpenAI(),
    tools=tools,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    while True:
        query = input("Ask me something: ")
        answer = agent.run(query)
        print(answer)