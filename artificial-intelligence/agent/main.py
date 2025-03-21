import pytest
from time import time
from prompt import prompt_template_from
from fastapi import FastAPI

MAX_REQUEST_TIMES = 8

tools = {

  
}

def call_llm_api():
  """
  
  
  """
  return {
    'action':{
      'name':'',
      'args':{}
    },
    'plan':{
      'response':''
    }
  }


def exec_task(task_description):
  """
  

  """
  count = 0
  chat_history = []

  while count <= MAX_REQUEST_TIMES:
    count += 1

    prompt = prompt_template_from(task_description)

    start = time()

    response = call_llm_api()

    action = response.get('action')
    action_name, action_args = action['name'], action['args']

    if action_name == 'finish':
      break
    
    tool = tools[action_name]



    end = time()

    if not (response and isinstance(response, dict)):
      continue


def main():
  greet = 'AI Agent 0.0.1\r\nType "help" or "/?" for more information'

  print(greet)

  help_message = '''


  '''

  while True:
    user_input = input('>>> ')

    if user_input == 'q':
      break
    elif user_input == 'help' or user_input == '/?':
      print(help_message)
    else:
      exec_task(user_input)


if __name__ == '__main__':
  main()
