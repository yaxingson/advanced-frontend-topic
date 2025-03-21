import os
from openai import OpenAI
from openai.types import ChatCompletionToolParam, FunctionParameters
from dotenv import load_dotenv
from collections import Iterable

load_dotenv()

model_settings = {
  'openai':{
    'model':'gpt-4o-mini',
    'env_name':'OPENAI_API_KEY'
  },
  'llama':{
    'base_url':'https://api.llama-api.com',
    'model':'llama3.1-70b',
    'env_name':'LLAMA_API_KEY'
  },
  'claude':{
    'base_url':'https://api.anthropic.com/v1',
    'model':'claude-3-7-sonnet-20250219',
    'env_name':''
  },
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
  'chatglm':{
    'base_url':'https://open.bigmodel.cn/api/paas/v4',
    'env_name':'ZHIPU_API_KEY',
    'model':'glm-4-plus'
  },
  'doubao':{
    'base_url':'https://ark.cn-beijing.volces.com/api/v3',
    'env_name':'ARK_API_KEY',
    'model':'doubao-1-5-pro-32k-250115'
  },
  'deepseek': {
    'base_url':'https://api.deepseek.com',
    'env_name':'DEEPSEEK_API_KEY',
    'model':'deepseek-reasoner'
  }
}

tools:Iterable[ChatCompletionToolParam] = [
  {
    "type":"function",
    "function":{
      "name":"get_weather",
      "description":"",
      "parameters":{
        "lat": {
          "type":"",
          "description":""
        },
        "lon":{

        }
      },
      "strict":{

      }
    }
  }
]

def question(prompt, model='qwen'):
  settings = model_settings[model]

  client = OpenAI(
    api_key=os.environ.get(settings['env_name']),
    base_url=settings.get('base_url', ''),
    default_headers={
      'appid':'app-EAzvJHg6'
    }
  )
  
  completion = client.chat.completions.create(
    model=settings['model'],
    messages=[
      {"role": "user", "content": prompt}
    ],
    temperature=0.5,
    top_p=0.5,
    stream=False,
    tools=tools,
  )

  result = completion.choices[0].message.content

  print(result)
