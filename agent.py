from langchain import OpenAI
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.tools.human.tool import HumanInputRun
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI


from memory import get_memory


tools = [
    Tool(
        name = "OhMyZsh Official Wiki",
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

memory = ConversationSummaryBufferMemory(memory_key="chat_history",
                                         return_messages=True,
                                         max_token_limit=400,
                                         llm=ChatOpenAI(temperature=0))
def conversational_agent():
    llm=ChatOpenAI(temperature=0)
    agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent

if __name__ == "__main__":
    while True:
        agent = conversational_agent()
        query = input("Ask me something: ")
        answer = agent.run(query)
        print(answer)
        # print memory
        print(f'\nMemory: {memory.load_memory_variables({})}')