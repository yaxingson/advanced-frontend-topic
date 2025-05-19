import os
import requests
import sqlite3
from langchain_community.chat_models import ChatZhipuAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langgraph.prebuilt import create_react_agent
from langchain.chains import RetrievalQA
from langchain.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

class ZhipuAIEmbeddings(Embeddings):
  def __init__(self):
    self.api_key = os.getenv('ZHIPU_API_KEY')

  def embed_documents(self, texts):
    return [self.embed_query(text) for text in texts]

  def embed_query(self, text):
    url = "https://open.bigmodel.cn/api/paas/v4/embeddings"
    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type":"application/json"
    }
    data = {
      "model": "embedding-2",
      "input": text
    }
    resp = requests.post(url, headers=headers, json=data)    
    return resp.json()["data"][0]["embedding"]

chat = ChatZhipuAI(
  model='glm-4',
  api_key=os.getenv('ZHIPU_API_KEY'),
  temperature=0.3,
  max_tokens=30
)

examples = [
  {
    'input':'今天真是太棒了！',
    'output':'积极'
  },
  {
    'input':'2023年12月，马云在杭州参加了一个人工智能论坛，并发表了演讲。',
    'output':'<root><person>马云</person><address>杭州</address><date>2023/12</date></root>'
  },
  {
    'input':'我觉得这个产品很差。',
    'output':'消极'
  },
  {
    'input':'他去了公司。',
    'output':'中性'
  },
  {
    'input':'2024年5月8日，约翰在纽约市参加了一个重要的会议。',
    'output':'<root><person>约翰</person><address>纽约市</address><date>2024/05/08</date></root>'
  },
]

prompt_template = PromptTemplate.from_template('''
请将以下内容翻译成{language}，并尽可能保留原文的语气与风格：

{text}
                                            
''')

prompt = prompt_template.format(
  language='法语',
  text='人生苦短，我用Python。'
)

example_prompt = PromptTemplate(
  input_variables=['input', 'output'],
  template='Input: {input}\r\nOutput: {output}'
)

example_selector = SemanticSimilarityExampleSelector.from_examples(
  examples=examples,
  embeddings=ZhipuAIEmbeddings(),
  vectorstore_cls=FAISS,
  k=2
)

few_shot_prompt_template = FewShotPromptTemplate(
  example_selector=example_selector,
  example_prompt=example_prompt,
  prefix='请根据下段示例，回答用户问题：',
  suffix='Input: {user_input}\r\nOutput: ',
  input_variables=["user_input"],
  example_separator="\n---\n"
)

prompt = few_shot_prompt_template.format(
  user_input='2024年11月5日，习近平在北京人民大会堂会见了来自法国的总统马克龙'
)

response_schemas = [
  ResponseSchema(name='person', description=''),
  ResponseSchema(name='address', description=''),
  ResponseSchema(name='date', description='')
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt_template = PromptTemplate(
  template='''
  请从下面的文本中提取所有出现的“时间”、“人物”和“地点”:
  
  """
  {user_input}
  """

  {format_instructions}

  ''',
  input_variables=['user_input'],
  partial_variables={'format_instructions':format_instructions}
)

prompt = prompt_template.format(user_input='2023年10月1日，习近平在北京天安门广场出席了国庆阅兵仪式。')

# response = chat.invoke([HumanMessage(content=prompt)])
# print(response.content)

llm_chain = prompt_template | chat

# output = llm_chain.invoke({'user_input':'乔布斯于2011年10月5日在加州去世。'})
# print(output.content)

documents = TextLoader('./news.txt', encoding='utf-8').load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=500,
  chunk_overlap=50,
)

texts = text_splitter.split_documents(documents)

map_prompt = PromptTemplate.from_template(
  "请用中文总结以下段落的要点：\n\n{text}\n\n总结："
)

combine_prompt = PromptTemplate.from_template(
  "以下是几个段落的中文总结，请你合并成一个通顺完整的最终总结：\n\n{text}\n\n最终总结："
)

summarize_chain = load_summarize_chain(
  llm=chat,
  map_prompt=map_prompt,
  combine_prompt=combine_prompt,
  chain_type='map_reduce',
  verbose=False
)

# response = summarize_chain.invoke({'input_documents':texts})
# print(response['output_text'])

@tool(description='获取指定地点的当前天气状况')
def get_weather(location):
  api_key = os.getenv('WEATHER_API_KEY')
  url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&lang=zh"

  response = requests.get(url)
  data = response.json()

  return f"{location} 当前天气：{data['current']['condition']['text']}，温度：{data['current']['temp_c']}°C"

agent = create_react_agent(
  model=chat,
  tools=[get_weather]
)

response = agent.invoke({
  "messages": [
    {"role": "user", "content": "今天天津市的天气怎么样？"}
  ]
})

db = SQLDatabase.from_uri('sqlite:///D:/llms.db')
db_chain = SQLDatabaseChain.from_llm(llm=chat, db=db, verbose=True)

# response = db_chain.invoke({"query": "Claude 3 Opus模型的提供商是谁？"})
# print(response)
