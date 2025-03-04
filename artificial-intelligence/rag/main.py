import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

model_settings = {
  'qwen':{
    'base_url':'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'env_name':'DASHSCOPE_API_KEY',
    'model':'qwen-plus'
  },
  'kimi':{
    'base_url':'https://api.moonshot.cn/v1',
    'env_name':'MOONSHOT_API_KEY',
    'model':'moonshot-v1-8k'
  },
  'deepseek': {
    'base_url':'https://api.deepseek.com',
    'env_name':'DEEPSEEK_API_KEY',
    'model':'deepseek-chat'
  }
}


def main(model='qwen'):
  settings = model_settings[model]

  client = OpenAI()

  data = client.embeddings.create(
    input='hello,world', 
    model='text-embedding-ada-002',
    encoding_format='float'
  ).data

  print([item.embedding for item in data])


if __name__ == '__main__':
  # main('kimi')
  pass
