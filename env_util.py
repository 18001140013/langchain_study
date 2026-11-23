import os

from dotenv import load_dotenv

"""
从.env中读取模型的访问密钥、端点,
定义成全局环境变量
"""

# 从env中加载环境变量
load_dotenv(verbose=True)

# DeepSeek
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
