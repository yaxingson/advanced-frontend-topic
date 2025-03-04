from tools import generate_tools_description

template = '''
尽可能地回答以下问题，你可以使用如下的工具:

{tool_name_description}

请使用以下格式回答:

"""
Thought {n}: {}
Action {n} : {}
Observe {n}: {}

"""

'''


prompt_template = '''
你是位问答专家，应该始终独立做出决策，无需寻求用户的提示和帮助, 追求极简的策略，避免涉及法律问题。

目标:
{task}

限制条件说明:
{constraints}

资源说明:
{resources}

使用如下的JSON格式作出响应:
{output_format}
确保响应结果可以由Python中的json模块解析

'''

output_format = '''
{
  "action": {
    "name": "",
    "args": {
    
    }
  
  }

}
'''


def prompt_template_from(task_description):
  """
  
  """
  prompt = prompt_template.format(
    task=task_description,
    output_format=output_format,

  )

  return prompt
