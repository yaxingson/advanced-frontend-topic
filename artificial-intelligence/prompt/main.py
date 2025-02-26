import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

model_settings = {
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
  'deepseek': {
    'base_url':'https://api.deepseek.com',
    'env_name':'DEEPSEEK_API_KEY',
    'model':'deepseek-chat'
  }
}


def main(model='qwen'):
  settings = model_settings[model]

  client = OpenAI(
    api_key=os.environ.get(settings['env_name']),
    base_url=settings['base_url']
  )

  user_content = '''
  请识别下段内容中的姓名（username）、电话（phone）和地点（address）:
  
  """
  中国天津市河西区隆昌路17号院 联系人张伟 手机号18830484731
  """

  以JSON格式输出
  '''

  user_content = '''
  用HTML和CSS生成用户登录表单，要求如下:
  1. 含有用户名和密码框
  2. 输入框上下有8px的间隔
  3. 内容居中显示
  
  '''

  user_content = '''
  用杜甫的风格为下段描述生成一首诗:

  """
  沿着广袤而秀丽的草原奔驰，我看到碧蓝的天空令人心旷神怡，青草掀起的波浪，让人仿佛置身于一望无际的海洋中。
  """
  
  '''
  
  user_content = '''
  请给下段内容起5个标题:

  """
  乌克兰还拥有欧洲三分之一的锂矿，而锂是电动车电池的关键成分。乌克兰的钛产量占全球的 7%，
  钛是一种轻质金属，用于从飞机到发电站等各种建筑。不仅如此，乌克兰还拥有丰富的稀土金属矿藏。
  稀土金属由17种元素组成，可用于生产武器、风力涡轮机、电子产品和其他对现代国家经济发展至关
  重要的产品。BBC的分析指出，美国对控制稀土矿物生产的兴趣，主要源于与中国的竞争。 过去几十
  年来，中国已成为开采与加工稀土矿物的领导者，占全球稀土产量的60%至 70%，并掌握近90%的加工能力。
  """

  '''

  user_content = '''
  您是位经验丰富的小说家，请为我生成一本短篇小说的目录摘要，小说的主要人物和情节如下:

  主要人物: 阿星，性格内向，不合群而又不干平凡，有一颗渴望改变世界的心
  
  情节描述: 阿星从小生活在中国乡村，和大多数农村孩子一样，小时候成绩优秀，但不喜欢中国的应试教育，
  最后考入了一所普通的大学。毕业后，一开始阿星认为自己将来肯定会作出一番事业，但现实的残酷使他像
  大多数人一样忙忙碌碌地过完了一生。

  '''

  user_content = '''
  请为有一定开发经验的程序员生成web编程进阶的思维导图，要求以markdown的格式输出

  '''

  user_content = '''
  请参考以下格式整理文本，并输出:
  
  格式: 

  username --> 'Landon Cunningham'
  email --> 'obmuwco@ojpe.au'

  文本内容: 

  """
  {
    "username":"Derek Burgess",
    "email":"dibas@tafid.sn"
  }
  """
  
  '''



  completion = client.chat.completions.create(
    model=settings['model'],
    messages=[
      {"role": "user", "content": user_content}
    ],
    temperature=0.3
  )

  result = completion.choices[0].message.content

  print(result)


if __name__ == '__main__':
  main('kimi')
