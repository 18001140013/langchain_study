import os

from dotenv import load_dotenv

# 从env中加载环境变量
load_dotenv(verbose=True)

# 定义全局的 密钥与Api Base
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
