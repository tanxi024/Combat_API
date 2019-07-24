# _*_coding:utf-8_*_
# @Time     :2019/4/10 13:51
# @Author   :Tanxi
# @Email    :1410510771@qq.com
# @File     :test_addloan.py
# @Software :PyCharm Community Edition

import json
import unittest

from ddt import ddt, data, unpack

from Combat_API.common import project_path
from Combat_API.common.doExcell import PyExcel
from Combat_API.common.do_mysql import DoMySql
from Combat_API.common.httpRequest import HttpRequest
from Combat_API.common.get_data import GetData
from Combat_API.common.python_logging import MyLogger
from Combat_API.common.read_config import ReadConfig
from Combat_API.common import get_data

# 测试加标
log = MyLogger()


@ddt
class TestCases(unittest.TestCase):
    # 读取测试用例
    a = ReadConfig(project_path.conf_path)
    sheetname = 'add_loan'
    pre_url = a.read_str('reqUrl', 'pre_url')
    t = PyExcel(project_path.case_path, sheetname)
    test_data = t.read_data('addloanCase')

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

        # 获取参数化的手机号及密码和member_id
        case[4] = get_data.replace(case[4])

        # 替换参数中的loanid
        if case[5] is not None:
            sql = eval(case[5])['loanid']
            loan_id = DoMySql().do_mysql(sql)[0]
            setattr(GetData, 'loanid', loan_id)

        try:
            # 发起请求
            req = HttpRequest(self.pre_url, method)
            actual_result = req.http_request(case[1], case[2], json.loads(case[4]), cookies=getattr(GetData, 'COOKIE'))

            # 写入实际结果
            self.t.write_data(case[0] + 1, 9, json.dumps(actual_result.json(), ensure_ascii=False))
            log.info('实际结果是：{}'.format(actual_result.json()))

            # 获取登录cookies
            if actual_result.cookies:
                setattr(GetData, 'COOKIE', actual_result.cookies)

            # # 加标请求之后，需查询数据库所加标的id
            # if case[5] is not None:
            #     sql = eval(case[5])['loanid']
            #     loan_id = DoMySql().do_mysql(sql)[0]
            #     setattr(GetData, 'LOAN_ID', loan_id)

            excepted_result = json.loads(case[6])
            log.info('期望结果是：{}'.format(excepted_result))

            self.assertDictEqual(excepted_result, actual_result.json())
            res = 'Pass'
        except Exception as e:
            res = 'Failed'
            print('请求出错，错误信息：{}'.format(e))
            raise e
        finally:
            self.t.write_data(case[0] + 1, 10, res)


if __name__ == '__main__':
    TestCases().test_cases()
