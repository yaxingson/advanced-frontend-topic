import os
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_community.llms.tongyi import Tongyi
from langchain_community.llms.fake import FakeListLLM
from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs.generation import Generation
from langchain_core.outputs.llm_result import LLMResult
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

examples = [
  {
    'question':'我吃苹果',
    'answer':'<root><subject>我</subject><predicate>吃</predicate><object>苹果</object></root>'
  },
  {
    'question':'他写信',
    'answer':'<root><subject>他</subject><predicate>写</predicate><object>信</object></root>'
  },
  {
    'question':'我们看电影',
    'answer':'<root><subject>我们</subject><predicate>看</predicate><object>电影</object></root>'
  }
]

class Employee(BaseModel):
  name:str = Field(description='')
  email:str = Field(description='')
  phone_number:str = Field(description='')


class Translator(BaseLLM):
  def _generate(self, prompts, stop=None, run_manager=None, **kwargs):
    results = []
    for prompt in prompts:
      result = Generation(text=f'[{datetime.now()}] {prompt}')
      results.append(result)
    return LLMResult(generations=[results])

  @property
  def _llm_type(self):
    return type(self).__name__.lower()


def main():
  model = Tongyi(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    model='qwen-max', 
    model_kwargs={},
    streaming=False
  )
  
  # prompt_tpl = PromptTemplate.from_template('请将下段句子翻译为日语（仅输出翻译内容）：\n\n{user_input}')
  # user_input = input('> ')
  # prompt = prompt_tpl.format(user_input=user_input)

  parser = JsonOutputParser()
  parser = PydanticOutputParser(pydantic_object=Employee)

  example_prompt = PromptTemplate(
    input_variables=['question', 'answer'],
    template='Question: {question}\nAnswer: {answer}',
  )

  prompt_tpl = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix='请参考下面的示例，回答问题: \n<example>',
    suffix='</example>\n\nQuestion: 她在听音乐\nAnswer: ',
    input_variables=[]
  )
  
  prompt = prompt_tpl.format()

  prompt = PromptTemplate(
    template="Randomly generate an employee's information, including name, email, and phone number.({format_instructions})",
    partial_variables={'format_instructions':parser.get_format_instructions()}
  )

  chain = prompt | model | parser

  # for s in chain.stream({}):
  #   print(s)

  result = model.invoke(prompt.format())
  employee = parser.parse(result)

  print(isinstance(employee, Employee))

  print(model.invoke('who are you ?'))


if __name__ == '__main__':
  responses = [
    '你好！有什么我可以帮你的吗？',
    '早上好，很高兴遇见你。',
    '我是一位乐于助人的智能助手，提供简洁且信息丰富的回复。'
  ]

  fake_list_llm = FakeListLLM(responses=responses)

  print(fake_list_llm.invoke('你好呀'))
  print(fake_list_llm.invoke('你好呀'))
  print(fake_list_llm.invoke('你好呀'))
  print(fake_list_llm.invoke('你好呀'))
  print(fake_list_llm.invoke('你好呀'))
