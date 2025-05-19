import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from mcp import ClientSession

load_dotenv(find_dotenv())

class MCPClient:
  def __init__(self):
    self.client = OpenAI(
      api_key=os.environ.get('DEEPSEEK_API_KEY'),
      base_url='https://api.deepseek.com'
    )
    self.session = None

  async def connect(self, script_path):
    is_js = script_path.endswith('.js')
    is_python = script_path.endswith('.py')
    command = 'node' if is_js else 'python'

