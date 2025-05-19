import os
from openai import OpenAI
from doctran import Doctran, DoctranConfig
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS, Chroma, Milvus
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatOpenAI(
  base_url=os.getenv('OPENAI_BASE_URL'),
  api_key=os.getenv('OPENAI_API_KEY'),
  model="gpt-4o-mini",
  temperature=0.1,
)

embedding = OpenAIEmbeddings(
  base_url=os.getenv('OPENAI_BASE_URL'),
  api_key=os.getenv('OPENAI_API_KEY')
)

docx_loader = Docx2txtLoader('./test.docx')
docx_docs = docx_loader.load()

pdf_loader = PyPDFLoader('./test.pdf')
pdf_docs = pdf_loader.load()

xls_loader = UnstructuredExcelLoader('./test.xls')
xls_docs = xls_loader.load()

text_splitter = CharacterTextSplitter(
  chunk_size=100,
  chunk_overlap=30
)

split_docs = text_splitter.split_documents(pdf_docs)

chroma_db = Chroma.from_documents(split_docs, embedding=embedding)

retriever_from_llm = MultiQueryRetriever.from_llm(
  retriever=chroma_db.as_retriever(),
  llm=llm
)

query = '在线文档预览兼容的主流浏览器有哪些？'
relevant_docs = retriever_from_llm.invoke(query)

context = ''

for relevant_doc in relevant_docs:
  context += relevant_doc.page_content

prompt_template = ChatPromptTemplate.from_messages([
  ('system', '请仅根据以下资料内容回答问题，不要凭空编造答案。如果无法从资料中找到答案，请回复“根据提供的信息无法确定”。\n\n[资料]\n{context}'),
  ('human', '[问题]\n{query}')
])

messages = prompt_template.format_messages(context=context, query=query)

response = llm.invoke(messages)

print(response.content)


