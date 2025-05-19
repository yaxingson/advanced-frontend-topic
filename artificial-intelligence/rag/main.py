import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import TextLoader, \
  CSVLoader, DirectoryLoader, UnstructuredHTMLLoader, JSONLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, \
  CharacterTextSplitter, Language
from doctran import Doctran

load_dotenv(find_dotenv())

prompt_template = '''
你是一个专业的中文助手。
请根据提供的资料简明扼要地用中文回答问题，回答长度不超过100字。
如果找不到答案，请回复 "无法从资料中确定答案"。

[资料]
{retrieved_context}

[问题]
{user_question}

[回答（JSON格式）]：
{
  "answer": "..."
}

'''

def main():
  client = OpenAI()

  response = client.embeddings.create(
    input="This is a sample sentence.",
    model="text-embedding-3-small" 
  )

  embedding = response.data[0].embedding
  print(embedding)  

def loader_demo():
  md_loader = TextLoader('./source/readme.md')
  csv_loader = CSVLoader('./source/users.csv', source_column='username')
  html_loader = UnstructuredHTMLLoader('./source/about.html')
  json_loader = JSONLoader('./source/config.json', jq_schema='.author')
  pdf_loader = PyPDFLoader('./source/resume.pdf')
  loader = DirectoryLoader(path='./source', glob='*')

def text_split_demo():
  text_splitter = RecursiveCharacterTextSplitter(
    separators=['\r\n'],
    is_separator_regex=False,
    chunk_size=50,
    chunk_overlap=20,
    length_function=len,
    add_start_index=True,
  )

  with open('./source/about.html') as f:
    text = f.read()
    doc = text_splitter.create_documents([text])
    print(doc)

def code_split_demo():
  py_code_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=10
  )

  with open('./source/utils.py') as f:
    doc = py_code_splitter.create_documents([f.read()])
    print(doc)


if __name__ == '__main__':
  code_split_demo()
