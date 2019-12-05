import os

# 项目根目录下local文件夹，存放本地json数据文件，作为测试用例。
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + '/local/'

# 数据库配置
DATABASE = {
    'USER': 'root',
    'PASSWORD': 'since1967',
    'NAME': 'odds',
    'HOST': 'localhost',
    'PORT': 3306,
}
# 自定义的event和event_id匹配
EVENT_ID = 1
EVENT_ID_DICT = dict()
