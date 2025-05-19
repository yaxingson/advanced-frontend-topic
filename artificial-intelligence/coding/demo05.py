import os
import requests
import openai
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.schema import HumanMessage,AIMessage,SystemMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.prompts import (ChatPromptTemplate, PromptTemplate, FewShotPromptTemplate, 
  HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from langchain_core.language_models.llms import LLM
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_community.callbacks.manager import get_openai_callback
# from langchain.chains import ConversationChain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import OpenAI, ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')

class Deepseek(LLM):
  def _call(self, prompt, stop = None, run_manager = None, **kwargs):
    headers = {
      "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
      "Content-Type": "application/json"
    }
    
    data = {
      "model": 'deepseek-reasoner',
       "messages": [
          {"role":"user", "content": prompt}
        ],
      "stream": False
    }

    response = requests.post('https://api.deepseek.com/chat/completions', json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        raise Exception(f"API 请求失败: {response.status_code}, {response.text}")

  @property
  def _identifying_params(self):
    return {
      'model_name':'DeepseekModel'
    }

  @property
  def _llm_type(self):
     return 'deepseek'
  
  def invoke(self, prompt):
    return self._call(prompt)

llm = Tongyi(model='qwen-plus')
chat = ChatTongyi(model='qwen-plus')

prompt_template = ChatPromptTemplate.from_template('简短易懂地解释{thing}是什么')
prompt = prompt_template.format_messages(thing='LLM')

response = chat.invoke(prompt)

examples = [
  {
    'Q':'横眉冷对千夫指，俯首甘为孺子牛。',
    'A':'彼は何千人もの人々の批判に冷静に向き合い、子供たちの牛になることもいとわなかった。'
  },
  {
    'Q':'不在沉默中爆发，就在沉默中灭亡。',
    'A':'静かに爆発するか、静かに滅びるか。'
  },
  {
    'Q':'我自横刀向天笑，去留肝胆两昆仑。',
    'A':'私は剣を手に持ち、空に向かって笑います。私が留まるかどうかに関係なく、私の忠誠心と勇気は私とともに残ります。'
  },
  {
    'Q':'人类的悲欢并不相通，我只觉得他们吵闹。',
    'A':'私は人間と同じ喜びや悲しみを共有しません。ただうるさいだけだと思う​​。'
  },
  {
    'Q':'无穷的远方，无数的人们，都和我有关。',
    'A':'無限の距離、無数の人々、すべてが私と関係している。'
  },
]

example_prompt = PromptTemplate(
  input_variables=['Q', 'A'],
  template='[Question]\n{Q}\n[Answer]\n{A}'
)

example_selector = LengthBasedExampleSelector(
  examples=examples,
  example_prompt=example_prompt,
)

few_shot_prompt_template = FewShotPromptTemplate(
  example_selector=example_selector,
  example_prompt=example_prompt,
  prefix='请根据以下示例回答用户问题:\n\n===\n',
  suffix='===\n\n[Question]\n{question}\n[Answer]\n',
  input_variables=['question'],
  example_separator='\n\n'
)

prompt = few_shot_prompt_template.format(question='人类的苦难永远不会结束，但是可以做出选择。')

response_schemas = [
  ResponseSchema(name='people', type='list', description=''),
  ResponseSchema(name='location', type='list', description=''),
  ResponseSchema(name='date', type='list', description=''),
]

out_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = out_parser.get_format_instructions()

prompt_template = ChatPromptTemplate.from_template('''
请从以下文本中提取出出现的日期、地点和人物信息：

```{text}```                                                
                                                   
{format_instructions}                                                                                                                                              
                                                   
''')

messages = prompt_template.format_messages(
  text='2023年5月，李华在北京参加了一场关于人工智能的会议，会上他遇到了张伟。',
  format_instructions=format_instructions
)

response = chat.invoke(messages)
info = out_parser.parse(response.content)

prompt = ChatPromptTemplate.from_messages([
  ("system", "你是一个有帮助的 AI 助手。"),
  MessagesPlaceholder(variable_name="history"),
  ("human", "{input}")
])

chain = prompt | chat

history_store = {}

def get_session_history(session_id: str):
  if session_id not in history_store:
    history_store[session_id] = InMemoryChatMessageHistory()
  return history_store[session_id]

with_history = RunnableWithMessageHistory(
  chain,
  get_session_history=get_session_history,
  input_messages_key="input",                    
  history_messages_key="history"
)

session_id = '89757'

while True:
  human_msg = input('> ')
  if human_msg.lower() == 'q':
    break
  response = with_history.invoke(
    {"input": human_msg}, 
    config={"configurable": {"session_id":session_id}}
  )
  print(response.content)
  # print(with_history.get_session_history(session_id))
