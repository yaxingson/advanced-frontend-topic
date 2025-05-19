import os
import openai
import chromadb
import tiktoken
import numpy as np
import gradio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core.settings import Settings
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.file import PDFReader, MarkdownReader
from llama_index.core import Document
from llama_index.core.llama_pack import download_llama_pack
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.base_url = os.environ["OPENAI_BASE_URL"]

llm = OpenAI(model="gpt-4o-mini")

Settings.chunk_size = 300
Settings.llm = llm

chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.get_or_create_collection('test')
chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=chroma_vector_store)

documents = SimpleDirectoryReader(input_files=['./news.txt']).load_data()

documents = [
  Document(text='''
  英国前贸易官员艾丽·雷尼森提到，前任美国总统拜登在取消对英国的钢铁关税时，也曾要求查看英国对一家中资钢铁公司
  的审计报告。她认为，特朗普政府的这一举措，本质上是美国政府对长期限制中国参与全球战略性商品供应政策的进一步升级。
  '''),
  Document(text='''
  所谓“232调查”，是指美国商务部根据1962年《贸易扩展法》第232条款规定的授权，对特定产品进口是否对美国国家安全
  造成威胁进行立案调查。这项调查允许美国总统限制被认为对国家安全构成威胁的产品进口。
  '''),
  Document(text='''
  5月7日，中国外交部宣布，5月9日至12日访问瑞士期间，中共中央政治局委员、国务院副总理何立峰作为中美经贸中方牵头人，
  将与美方牵头人美国财政部长贝森特举行会谈。
  '''),
]

documents = PDFReader().load_data('./resume.pdf')

vector_store_index = VectorStoreIndex.from_documents(
  documents=documents,
  storage_context=storage_context
)

query_engine = vector_store_index.as_query_engine(
  response_mode=ResponseMode.TREE_SUMMARIZE,
  streaming=False,
)

query = 'Anthony Fu在哪所院校毕业的？（用中文回答）'

# response = query_engine.query()

# AutoMergingRetrieverPack = download_llama_pack(
#   "AutoMergingRetrieverPack", "./auto_merging_retriever_pack"
# )

# auto_merging_retriever_pack = AutoMergingRetrieverPack(documents)
# response = auto_merging_retriever_pack.run(query)

# print(response)

model = openai.OpenAI()

messages=[
  {'role':'user', 'content':'政治自由对于一个国家意味着什么？'}
]

completion = model.chat.completions.create(
  model='gpt-3.5-turbo',
  messages=messages,
  max_tokens=1000,
  temperature=0.5,
  n=1,
  stream=False,
)

response = completion.choices[0].message.content

# print(completion.usage)

encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
tokens = encoding.encode(str(messages))

# print(len(tokens))

embeddings = model.embeddings.create(
  model='text-embedding-ada-002',
  input='天空为什么是蓝色的？',
)

vector_data = embeddings.data[0].embedding

# print(len(vector_data))

chat = ChatOpenAI()
# response = chat.invoke('孙中山和鲁迅的共同点？')
# print(response)

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=50,
  chunk_overlap=10
)

documents = PyPDFLoader('resume.pdf').load_and_split(text_splitter)

embedding = OpenAIEmbeddings()
db = FAISS.from_documents(documents=documents, embedding=embedding)

response_schemas = [
  ResponseSchema(name='question', type='string', description=''),
  ResponseSchema(name='answer', type='string', description='')
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

question = f'Anthony Fu的毕业院校？（{format_instructions}）'

# retrieval_documents = db.similarity_search(question, k=3)

qa_chain = RetrievalQA.from_chain_type(
  llm=chat,
  chain_type="stuff",
  retriever=db.as_retriever(search_kwargs={'k': 3}),
  return_source_documents=True
)

response = qa_chain.invoke(question)

# print(response['result'])
