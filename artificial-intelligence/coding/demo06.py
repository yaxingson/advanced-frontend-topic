from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import (ChatPromptTemplate, MessagesPlaceholder, 
    HumanMessagePromptTemplate)
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from dotenv import load_dotenv, find_dotenv
from langchain_deepseek import Deepseek, ChatDeepseek

load_dotenv(find_dotenv())

llm = ChatTongyi()

prompt = ChatPromptTemplate.from_messages([
  SystemMessage(content='你是一个聪明、友善且乐于助人的AI助手。'),
  MessagesPlaceholder(variable_name='chat_history'),
  HumanMessagePromptTemplate.from_template('{question}')
])

messages = prompt.format_messages(
  chat_history=[
    HumanMessage(content='你好，我叫sonera, 很高兴见到你！'),
    AIMessage(content='你好，Sonera！我也很高兴见到你 😊')
  ],
  question='还记得我叫什么名字吗？'
)

response = llm.invoke(messages)

print(response.content)
