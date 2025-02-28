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

def question(prompt, model='qwen'):
  settings = model_settings[model]

  client = OpenAI(
    api_key=os.environ.get(settings['env_name']),
    base_url=settings['base_url']
  )
  
  completion = client.chat.completions.create(
    model=settings['model'],
    messages=[
      {"role": "user", "content": prompt}
    ],
    temperature=0.3
  )

  result = completion.choices[0].message.content

  print(result)
