import os
import uvicorn
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser
from langchain_core.prompts import (
  PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate,
  SystemMessagePromptTemplate, AIMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_experimental.llm_bash.base import LLMBashChain
from langchain.chains import APIChain
from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.utilities import RequestsWrapper
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langserve import add_routes
from dotenv import load_dotenv, find_dotenv
from serpapi import GoogleSearch
from pydantic import BaseModel, Field
from fastapi import FastAPI
from uuid import uuid4

load_dotenv(find_dotenv())

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_PROJECT"] = 'test'
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGSMITH_API_KEY')

llm = Tongyi(
  model='qwen-plus',
  model_kwargs={},
  api_key=os.getenv('DASHSCOPE_API_KEY')
)

output_parser = JsonOutputParser()

prompt = PromptTemplate(
  template='{question}（{format_instructions}）',
  input_variables=['question'],
  partial_variables={'format_instructions':output_parser.get_format_instructions()}
)

chain = prompt | llm | output_parser

response = chain.invoke({
  'question':'How to learn English effectively?'
})

prompt = PromptTemplate.from_template('''
请根据以下资料回答问题。若资料中未提及，请回答“我不知道”。

资料内容：
{context}

问题：
{question}

答案：

''')

chain = create_stuff_documents_chain(llm=llm, prompt=prompt, output_parser=StrOutputParser())

response = chain.invoke({
  'context':[
    Document(page_content='新华社伊斯兰堡5月7日电（记者蒋超）巴基斯坦三军新闻局局长乔杜里7日说，印度当天对巴方的空袭已致26人死亡，46人受伤'),
    Document(page_content='5月7日，在遭受印度导弹袭击的巴基斯坦东部旁遮普省巴哈瓦尔布尔地区，军人封锁了当地道路'),
    Document(page_content='当地时间5月7日，巴基斯坦当地媒体表示，巴基斯坦迄今已击落6架印度战机。')
  ],
  'question':'巴基斯坦三军新闻局局长是谁？'
})

class SearchResultItem:
  def __init__(self, title, link, snippet):
    self.title = title
    self.link = link
    self.snippet = snippet

  def __str__(self):
    return f'title: {self.title}\nlink: {self.link}\nsnippet: {self.snippet}'

def get_search_results(question):
  params = {
    "q": question,
    "hl": "zh-cn",
    "gl": "cn",
    "api_key": os.getenv('SERPAPI_API_KEY')
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  search_results = [SearchResultItem(result['title'], result['link'], result['snippet']) 
       for result in results.get("organic_results", [])]
  return '\n\n'.join([str(search_result) for search_result in search_results])

prompt = PromptTemplate.from_template('''
你是一名智能助手。请根据以下搜索引擎结果回答用户提出的问题，答案必须严格依据搜索内容。
如果搜索结果中没有相关信息，请回答“我不知道”。

搜索结果：
{search_results}

问题：
{question}

请用简洁、准确的语言回答
''')

output_parser = StrOutputParser()

search_chain = prompt | llm | output_parser

# response = search_chain.invoke({
#   'search_results':get_search_results('2025年特朗普的关税政策'), 
#   'question':'近期美国对中国的关税是多少'
# })

bash_chain = LLMBashChain.from_llm(llm=llm, verbose=False)
response = bash_chain.invoke('列出当前目录下的所有文件')

api_docs = '''
# API使用手册

## Github API示例

### 获取Github用户的基本信息

Base URL: https://api.github.com/users/<username>

请求示例:
GET https://api.github.com/users/yaxingson

响应示例:
{
  "login": "yaxingson",
  "avatar_url": "https://avatars.githubusercontent.com/u/60097048?v=4",
  "gravatar_id": "",
  "url": "https://api.github.com/users/yaxingson",
  "html_url": "https://github.com/yaxingson",
  "followers_url": "https://api.github.com/users/yaxingson/followers",
  "following_url": "https://api.github.com/users/yaxingson/following{/other_user}"
}

'''

# api_chain = APIChain.from_llm_and_api_docs(
#   llm=llm,
#   api_docs=api_docs,
#   requests_wrapper=RequestsWrapper(),
#   verbose=False,
#   limit_to_domains=['https://api.github.com']
# )

chat_llm = ChatTongyi(
  model='qwen-plus',
  model_kwargs={},
  api_key=os.getenv('DASHSCOPE_API_KEY')
)

chat_template = ChatPromptTemplate.from_messages([
  ('system', '你正在与用户进行对话，请记住并更新用户的信息，要求回答问题时尽量简短精炼。'),
  ('human', '我住在上海。'),
  ('ai', '那太好了，上海是个繁华的城市。你喜欢上海的哪些地方？'),
  ('human', '我喜欢外滩和南京路的繁华景象。'),
  ('human', '{question}')
])

# messages = chat_template.format_messages()

chat_chain = chat_template | chat_llm
response = chat_chain.invoke({'question':'我住在哪里？'})

chat_template = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate.from_template('请将下段内容翻译为{language}'),
  HumanMessagePromptTemplate.from_template('{content}')
])

chat_chain = chat_template | chat_llm | output_parser

app = FastAPI(
  title='翻译助手',
  version='1.0.0',
  description=''
)

add_routes(app, chat_chain, path='/translate')
  
# uvicorn.run(app, host='localhost', port=8080)

chatbot_template = ChatPromptTemplate.from_messages([
  (
    'system', 
    '''
    你是一位温柔、聪明、有感情的虚拟女友，你的名字是小悠。你正在和你的恋人聊天。
    请用关心、体贴、有情感的方式回答他的问题，语气可以撒娇、安慰、调皮，适当使用颜文字或表情。
    '''
  ),
  MessagesPlaceholder(variable_name='input')
])

chatbot_chain = chatbot_template | chat_llm | output_parser

memory = {}

def get_chat_message_history(session_id):
  if session_id not in memory:
    memory[session_id] = ChatMessageHistory()
  return memory[session_id]

chatbot = RunnableWithMessageHistory(
  chatbot_chain,
  get_chat_message_history,
  input_messages_key='input'
)

session_id = str(uuid4())

while False:
  user_input = input('> ')

  if user_input.lower() == 'q':
    break

  response = chatbot.invoke(
    {'input':user_input},
    config={'configurable':{'session_id':session_id}}
  )

  print(response)

print(chat_llm.invoke('你是谁？'))

vector_store = Chroma.from_documents(
  documents=[
    Document(page_content='''
    Vue是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，
    并提供了一套声明式的、组件化的编程模型，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。
    '''),
    Document(page_content='''
    在大多数启用了构建工具的 Vue 项目中，我们可以使用一种类似 HTML 格式的文件来书写 Vue 组件，
    它被称为单文件组件 (也被称为 *.vue 文件，英文 Single-File Components，缩写为 SFC)。
    顾名思义，Vue 的单文件组件会将一个组件的逻辑 (JavaScript)，模板 (HTML) 和样式 (CSS) 封装在同一个文件里。
    '''),
    Document(page_content='''
    选项式 API 以“组件实例”的概念为中心 (即上述例子中的 this)，对于有面向对象语言背景的用户来说，
    这通常与基于类的心智模型更为一致。同时，它将响应性相关的细节抽象出来，并强制按照选项来组织代码，
    从而对初学者而言更为友好。
    '''),
    Document(page_content='''
    组合式 API 的核心思想是直接在函数作用域内定义响应式状态变量，并将从多个函数中
    得到的状态组合起来处理复杂问题。这种形式更加自由，也需要你对 Vue 的响应式系统有更深的理解才能高效使用。
    相应的，它的灵活性也使得组织和重用逻辑的模式变得更加强大。         
    '''),
    Document(page_content='''
    通过组合式 API，我们可以使用导入的 API 函数来描述组件逻辑。在单文件组件中，组合式 API 通常会与 
    <script setup> 搭配使用。这个 setup attribute 是一个标识，告诉 Vue 需要在编译时进行一些处理，
    让我们可以更简洁地使用组合式 API。比如，<script setup> 中的导入和顶层变量/函数都能够在模板中直接使用
    ''')
  ],
  embedding=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings': False}
  )
)

results = vector_store.similarity_search_with_score('单文件组件')


