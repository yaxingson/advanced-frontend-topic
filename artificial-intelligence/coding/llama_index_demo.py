import os
import chromadb
import requests
import asyncio
from pydantic import PrivateAttr, Field
from llama_index.core.base.embeddings.base import BaseEmbedding, Embedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.llms import LLM, CustomLLM, ChatMessage, LLMMetadata, ChatResponse
from llama_index.core.settings import Settings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_key = os.getenv('DASHSCOPE_API_KEY')

class QwenApiLLM(CustomLLM):
  api_key:str = Field(default=api_key)
  model:str = Field(default="qwen-plus")

  def chat(self, messages, **kwargs):
    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }
    payload = {
      "model": self.model,
      "input": {
          "messages": [{"role": m.role, "content": m.content} for m in messages]
      }
    }

    response = requests.post(
      "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
      headers=headers, 
      json=payload
    )

    if response.status_code != 200:
      raise Exception(f"Qwen LLM API error: {response.status_code}, {response.text}")

    text = response.json()["output"]["text"]
    return ChatResponse(message=ChatMessage(role="assistant", content=text))

  def complete(self, prompt: str, **kwargs) -> str:
    return self.chat([ChatMessage(role="user", content=prompt)], **kwargs)

  def stream_complete(self, prompt: str, **kwargs):
    yield self.complete(prompt, **kwargs)

  @property
  def metadata(self) -> LLMMetadata:
    return LLMMetadata(
      context_window=4096,
      num_output=512,
      is_chat_model=True,
      model_name=self.model,
    )

class QwenEmbedding(BaseEmbedding):
  _api_key:str = PrivateAttr()
  _model:str = PrivateAttr()
  _api_url:str = PrivateAttr()

  def __init__(self, model="text-embedding-v1"):
    super().__init__()
    self._api_key = api_key
    self._model = model
    self._api_url = (
      "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
    )

  def _get_query_embedding(self, query):
    return self._get_text_embedding(query)

  def _get_text_embedding(self, text):
    return self._get_text_embedding_batch([text])[0]

  def _get_text_embedding_batch(self, texts):
    headers = {
      "Authorization": f"Bearer {self._api_key}",
      "Content-Type": "application/json",
    }

    payload = {
      "model": self._model,
      "input": {
          'texts':texts
      },
    }

    response = requests.post(self._api_url, json=payload, headers=headers)

    if response.status_code != 200:
      raise Exception(f"Qwen embedding API error: {response.status_code}, {response.text}")

    data = response.json()
    return [item["embedding"] for item in data["output"]["embeddings"]]

  async def _aget_query_embedding(self, query):
    return await asyncio.to_thread(self._get_query_embedding, query)

Settings.chunk_size = 300
Settings.llm = QwenApiLLM()

documents = SimpleDirectoryReader(
  input_files=['./news.txt']
).load_data()

vector_store_index = VectorStoreIndex.from_documents(
  documents=documents,
  embed_model=QwenEmbedding()
)

query_engine = vector_store_index.as_query_engine(
  llm=QwenApiLLM(),
  top_k=3,
  response_mode='compact',
)

response = query_engine.query('巴基斯坦军方发言人是谁？')
print(response)
