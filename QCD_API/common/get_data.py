# _*_coding:utf-8_*_
# @Time     :2019/4/10 13:53
# @Author   :Tanxi
# @Email    :1410510771@qq.com
# @File     :get_data.py
# @Software :PyCharm Community Edition

import re
from Combat_API.common import project_path
from Combat_API.common.read_config import ReadConfig

config = ReadConfig(project_path.conf_path)


class GetData:
    '''可以用来动态的更改 删除 获取数据'''
    COOKIE = None  # 请求时cookie初始值
    LOAN_ID = None  # 新添加项目时，标id的初始值
    user_phone = config.read_str('data', 'user_phone')
    user_pwd = config.read_str('data', 'user_pwd')
    user_member_id = config.read_str('data', 'user_member_id')


def replace(target):
    p = '#(.*?)#'
    while re.search(p, target):
        pre_value = re.search(p, target).group(1)
        value = getattr(GetData, pre_value)
        target = re.sub(p, value, target, count=1)
    return target
