import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import requests
import json

load_dotenv(find_dotenv())

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
    'env_name':'CLAUDE_API_KEY'
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

def add(first_value, second_value):
  return first_value + second_value

def get_weather(city):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key=5eff4dfe86f411a8dce2c4bb4b3710d5"
    response = requests.get(url).json()
    if response["status"] == "1":
        weather = response["lives"][0]
        return f"{weather['city']} 天气: {weather['weather']}, 温度: {weather['temperature']}℃"
    else:
        return "查询失败"

tools = [
  {
    "type":"function",
    "function":{
      "name":"add",
      "description":"Calculate the sum of the two numbers.",
      "parameters":{
        "type":"object",
        "properties":{
          "first_value": {
            "type":"number",
            "description":"first value"
          },
          "second_value":{
            "type":"number",
            "description":"second value"
          }
        },
        "required": ["first_value", "second_value"]
      }
    }
  },
  {
    "type":"function",
    "function":{
      "name":"get_weather",
      "description":"Obtain the weather conditions of the designated city on that day.",
      "parameters":{
        "type":"object",
        "properties":{
          "city":{
            "type":"string",
            "description":"city"
          }
        },
        "required": ["city"]
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
    stream=False
  )

  result = completion.choices[0].message.content

  print(result)

def generate(desc):
  response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
      "authorization": f"Bearer sk-1WiDvaSzfm0GjOKN8o5ZKiOxaLbHcuDH9qH2YtB5rnHA4JZr",
      "accept": "image/*",
      "Content-Type": "application/json"
    },
    files={"none": ''},
    data={
      "prompt": desc,
      "output_format": "jpeg",
      "width":800,
      "height":1294,
      "samples":1
    }
  )

  if response.status_code == 200:
    print(response.json())
  else:
    raise Exception(str(response.json()))

def call(prompt, messages=None):
  print('xx')

    
  settings = model_settings['chatglm']

  if messages is None:
    messages = [
      {"role": "user", "content": prompt}
    ]

  client = OpenAI(
    api_key=os.environ.get(settings['env_name']),
    base_url=settings.get('base_url', ''),
    default_headers={
      'appid':'app-EAzvJHg6'
    }
  )

  completion = client.chat.completions.create(
    model=settings['model'],
    messages=messages,
    temperature=0.5,
    top_p=0.5,
    stream=False,
    tools=tools
  )

  print(completion.choices[0].message.content)

  tool_calls = completion.choices[0].message.tool_calls

  if tool_calls is not None:
    for tool_call in tool_calls:
      tool_call_id = tool_call.id
      func = tool_call.function
      func_name = func.name
      args = json.loads(func.arguments)
      match func_name:
        case 'add':    
          result = add(args['first_value'], args['second_value'])
          messages.append({
            'tool_call_id':tool_call_id,
            'role':'tool',
            'name':func_name,
            'content':str(result)
          })
        case 'get_weather':
          result = get_weather(args['city'])
          messages.append({
            'tool_call_id': tool_call_id,
            'role':'tool',
            'name':func_name,
            'content':result
          })
          
