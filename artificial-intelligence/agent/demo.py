from langchain_openai import ChatOpenAI
from langchain.serpapi import SerpAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.agents.tools import tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
  model='',
  temperature=0.5,
  api_key=''
)

tools = load_tools([], llm=llm)

agent = initialize_agent(
  llm=llm,
  tools=tools,
  agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)

if __name__ == '__main__':
  agent.run('')
