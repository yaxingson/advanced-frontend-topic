from ..message import SystemMessage, UserMessage, AssistantMessage

def template():
  prompt = '''
  {context}

  {instruction}

  """
  {input_data}
  """
  
  {examples}

  {output_indicator}
  '''

  return prompt.format(
    context='',
    instruction='',
    input_data='',
    output_indicator='',
    examples={

    }
  )

