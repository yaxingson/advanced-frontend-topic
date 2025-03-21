from typing import List

class ToolParam:
  def __init__(self, name, type, required):
    self.name = name
    self.type = type
    self.required = required

class Tool:
  def __init__(self, name, description, params:List[ToolParam], return_value):
    self.name = name
    self.description = description
    self.params = params
    self.return_value = return_value

class File:
  @staticmethod
  def read(path:str, encoding='utf-8'):
    """ Read the entire contents of a file """
    pass


  @staticmethod
  def write():
    pass

class Db:
  pass
