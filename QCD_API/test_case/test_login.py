# _*_coding:utf-8_*_
# @Time     :2019/3/27 16:57
# @Author   :Tanxi
# @Email    :1410510771@qq.com
# @File     :test_login.py
# @Software :PyCharm Community Edition

import json
import unittest

from ddt import ddt, data, unpack

from Combat_API.common import project_path
from Combat_API.common.doExcell import PyExcel
from Combat_API.common.httpRequest import HttpRequest
from Combat_API.common.python_logging import MyLogger
from Combat_API.common.read_config import ReadConfig
from Combat_API.common import get_data

log = MyLogger()

'''测试登录'''


@ddt
class TestCases(unittest.TestCase):
    # 读取测试用例
    a = ReadConfig(project_path.conf_path)
    sheetname = 'login'
    pre_url = a.read_str('reqUrl', 'pre_url')
    t = PyExcel(project_path.case_path, sheetname)
    test_data = t.read_data('loginCase')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 写用例
    @data(*test_data)
    # @unpack
    def test_cases(self, case):
        log.info('{}用例开始执行：'.format(self.sheetname + '_' + str(case[0])))
        method = case[2]

        # 获取已参数化的登录手机号及密码
        case[4] = get_data.replace(case[4])

        req = HttpRequest(self.pre_url, method)
        actual_result = req.http_request(case[1], case[2], json.loads(case[4]))
        log.info('实际结果是：{}'.format(actual_result.json()))
        self.t.write_data(case[0] + 1, 8, json.dumps(actual_result.json(), ensure_ascii=False))
        excepted_result = json.loads(case[5])
        log.info('期望结果是：{}'.format(excepted_result))
        try:
            self.assertDictEqual(excepted_result, actual_result.json())
            # self.assertEqual(excepted_result,actual_result)
            res = 'Pass'
        except AssertionError as e:
            res = 'Failed'
            print('请求出错，错误信息：{}'.format(e))
            raise e
        finally:
            self.t.write_data(case[0] + 1, 9, res)


if __name__ == '__main__':
    t = TestCases().test_cases()
