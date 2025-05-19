import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI(
  base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
  api_key=os.getenv('DASHSCOPE_API_KEY')
)

def test():
  completion = client.chat.completions.create(
    model='qwen-plus',
    messages=[
      {'role':'system', 'content':'您是一位经验丰富的健身教练，请根据以往经验回答下列用户问题'},
      {'role':'user', 'content':'为新手制定一份一周内的健身方案'}
    ],
    temperature=0.3,
    stream=True
  )

  # for chunk in completion:
  #   if hasattr(chunk, 'choices') and chunk.choices:
  #     choice = chunk.choices[0]
  #     if hasattr(choice, 'text'):
  #       print(choice.text, end='', flush=True)

  for chunk in completion:
    if 'choices' in chunk:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            print(delta['content'], end='', flush=True)

def bootstrap():
  st.set_page_config(
    page_title='Streamlit Demos'
  )
  
  st.write('Streamlit')
  "A faster way to build and share data apps."

  username = st.text_input('Username')
  
  if username:
     st.session_state['username'] = username
  
  st.number_input('Count', max_value=10, min_value=0, value=3)
  st.text_area('Resume')
  st.time_input('Current Time')
  st.file_uploader('Data Source', type=['csv', 'json', 'md'])

  if st.sidebar.button('Rerun'):
     st.rerun()

  if st.sidebar.button('User'):
     st.switch_page('./user.py')

  tab1 , tab2 = st.tabs(['tab1', 'tab2'])
  tab1.write('this is tab1')
  tab2.write('this is tab2')

  with st.expander('Python'):
     st.write('Python is a programming language that lets you work more quickly and \
              integrate your systems more effectively.')

  st.chat_input('你好，有什么可以帮助您的吗')


if __name__ == '__main__':
  bootstrap()
