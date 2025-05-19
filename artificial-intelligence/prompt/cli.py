import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI(
  base_url='https://api.deepseek.com',
  api_key=os.environ.get('DEEPSEEK_API_KEY')
)

def generate_prompt():
  prompt_template = '''  
  # 上下文背景信息
  {context}

  # 指示
  {instruction}

  # 输入信息
  {input_msg}

  # 输出信息
  {output_msg}
  
  # 示例
  {examples}

  '''

  instruction = input('指示: ')
  context = input('上下文背景信息: ')
  examples = input('示例: ')
  input_msg = input('输入信息: ')
  output_msg = input('输出信息: ')

  return prompt_template.format(instruction=instruction, 
    context=context, examples=examples, input_msg=input_msg, output_msg=output_msg)

def query(content, role='个人助手', prev_response=None):
  messages = [
    {'role':'system', 'content':f'你是位{role}'},
    {'role':'user', 'content':prompt},
    {'role':'assistant', 'content':''}
  ]

  # client.moderations.create({})

  completion = client.chat.completions.create(
    model='deepseek-reasoner',
    messages=messages,
    temperature=0.3,
    seed=None,
    stream=False,
    top_p=1,
    
  )

  return completion.choices[0].message.content


if __name__ == '__main__':
  while True:
    prompt = generate_prompt()
    
    response = query(prompt, input('设定角色: '))

    print(response)

    proceed = input('继续(y|n)? ')

    if(proceed.lower() == 'n'):
      break




