import os
import openai
import bs4
from langchain_core.documents.base import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')

os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' 

llm = ChatOpenAI(
  model='gpt-3.5-turbo',
  temperature=0.01
)

documents = [
  Document(page_content='''
  华盛顿/多伦多 — 加拿大自由党的领袖、前加拿大央行行长马克·卡尼(Mark Carney)星期五(3月14日)宣誓就任加拿大总理。
  他立即表示，他可以与美国总统唐纳德·特朗普(Donald Trump)合作。他上任后面临的最为严峻的挑战就是如何处理与美国的
  关税战。在对华关系上，有专家预期这位新总理做出新的努力来改善与中国的关系。
  '''),
  Document(page_content='''
  卡尼在上周的自由党领袖竞选中取得压倒性胜利，接替了在任九年的卸任总理贾斯汀·特鲁多，担任加拿大的第24任总理。在他
  就任之际，美国与加拿大的贸易战正在持续发酵。
  '''),
  Document(page_content='''
  加拿大全球事务研究所(Canadian Global Affairs Institute)副所长兼加拿大-美国关系专家组成员科林·罗伯逊
  (Colin Robertson)在接受美国之音采访时说，基于卡尼在竞选期间发表的言论来看，他会把重点放在外交以及与特朗普政府、
  国会和州政府的接触上。他还提到，卡尼曾表示会对美国政府的关税行动采取反关税措施。
  ''')
]

embedding = OpenAIEmbeddings(model='text-embedding-ada-002')

vector_store = Chroma.from_documents(documents=documents, embedding=embedding)

query = '加拿大的第23任总理是谁？'

# results = vector_store.similarity_search_with_score(query)
retriever = RunnableLambda(vector_store.similarity_search).bind(k=1)

message = '''
根据以下提供的参考资料，回答用户的问题。

资料：
{context}

问题：
{question}

请基于资料作答，如果资料中没有明确答案，请说明无法确定。
'''

prompt_template = ChatPromptTemplate.from_messages([('human', message)])

chain = {'context':retriever,'question':RunnablePassthrough()} | prompt_template | llm

# response = chain.invoke(query)
# print(response.content)

tavily_search = TavilySearchResults(max_results=3)

# response = llm.invoke('请列出当前目录下的所有文件')
# print(response.content)

loader = WebBaseLoader(
  web_path='https://www.anthropic.com/news/model-context-protocol',
  bs_kwargs={
    'parse_only':bs4.SoupStrainer(class_=('Body_body__XEXq7'))
  }
)

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=300,
  chunk_overlap=50
)

documents = loader.load_and_split(text_splitter)
vector_store = Chroma.from_documents(documents=documents, embedding=embedding)
retriever = vector_store.as_retriever()

prompt = ChatPromptTemplate.from_messages([
  ('system', '根据以下提供的参考资料，用中文回答用户的问题。\n\n[资料]\n{context}'),
  ('human', '[问题]\n{input}')
])

chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

# response = chain.invoke({'input':'MCP的三个主要组件是什么？'})
# print(response['answer'])



