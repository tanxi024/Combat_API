# -*-coding:utf-8-*-
# @Time      :2019/3/30/030 19:52
# @Author    :Tanxi
# @Email     :1410510771@qq.com
# @File      :test_withdraw.py
# @Software  :PyCharm Community Edition

import json
import unittest

from ddt import ddt, data, unpack

from Combat_API.common import project_path
from Combat_API.common.doExcell import PyExcel
from Combat_API.common.httpRequest import HttpRequest
from Combat_API.common.get_data import GetData
from Combat_API.common.do_mysql import DoMySql
from Combat_API.common.python_logging import MyLogger
from Combat_API.common.read_config import ReadConfig
from Combat_API.common import get_data

# 测试提现
log = MyLogger()

COOKIES = None


@ddt
class TestCases(unittest.TestCase):
    # 读取测试用例
    a = ReadConfig(project_path.conf_path)
    sheetname = 'withdraw'
    pre_url = a.read_str('reqUrl', 'pre_url')
    t = PyExcel(project_path.case_path, sheetname)
    test_data = t.read_data('withdrawCase')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 写用例
    @data(*test_data)
    # @unpack
    def test_cases(self, case):

        # global COOKIES #全局变量

        log.info('{}用例开始执行：'.format(self.sheetname + '_' + str(case[0])))
        method = case[2]
        # 获取参数化的登录手机号码及密码
        case[4] = get_data.replace(case[4])

        # 请求之前，查询数据库账户剩余金额
        if case[5] is not None:
            sql = eval(case[5])['LeaveAmount']
            before_amount = DoMySql().do_mysql(sql)[0]

        # 发起请求
        req = HttpRequest(self.pre_url, method)
        # actual_result = req.http_request(case[1], case[2], json.loads(case[4]), cookies=COOKIES)  #全局变量
        actual_result = req.http_request(case[1], case[2], json.loads(case[4]), cookies=getattr(GetData, 'COOKIE'))

        # 写入实际结果
        self.t.write_data(case[0] + 1, 9, json.dumps(actual_result.json(), ensure_ascii=False))
        log.info('实际结果是：{}'.format(actual_result.json()))

        # 获取登录cookies
        if actual_result.cookies:
            # COOKIES = actual_result.cookies #全局变量更新
            setattr(GetData, 'COOKIE', actual_result.cookies)
        try:
            # 请求之后，再次查询数据库账户剩余金额
            if case[5] is not None:
                sql = eval(case[5])['LeaveAmount']
                withdraw_amount = eval(case[4])['amount']
                after_amount = DoMySql().do_mysql(sql)[0]
                expect_amount = float(before_amount) - float(withdraw_amount)
                expect_amount = ("%.2f" % expect_amount)  # 强制保留两位小数,四舍五入
                # expect_amount = round(expect_amount, 2)  # 保留两位小数，四舍五入，但只有一位小数时不会显示两位小数
                self.assertEqual(float(expect_amount), float(after_amount))

            # 判断是否需要替换期望值中的LeaveAmount
            if case[6].find('expect_amount') != -1:
                case[6] = case[6].replace('expect_amount', str(expect_amount))
            excepted_result = json.loads(case[6])
            log.info('期望结果是：{}'.format(excepted_result))

            self.assertDictEqual(excepted_result, actual_result.json())
            # self.assertEqual(excepted_result,actual_result)
            res = 'Pass'
        except AssertionError as e:
            res = 'Failed'
            print('请求出错，错误信息：{}'.format(e))
            raise e
        finally:
            self.t.write_data(case[0] + 1, 10, res)


if __name__ == '__main__':
    a = TestCases()
    a.test_cases()
