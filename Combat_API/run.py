# _*_coding:utf-8_*_
# @Time     :2019/3/26 13:35
# @Author   :Tanxi
# @Email    :1410510771@qq.com
# @File     :run.py
# @Software :PyCharm Community Edition

import sys
sys.path.append('./')
import unittest
import HTMLTestRunnerNew

from Combat_API.common import project_path
from Combat_API.test_case import test_register
from Combat_API.test_case import test_login
from Combat_API.test_case import test_recharge
from Combat_API.test_case import test_withdraw
from Combat_API.test_case import test_addloan

#新建一个测试集
suite=unittest.TestSuite()

#添加用例
loader=unittest.TestLoader()
suite.addTests(loader.loadTestsFromModule(test_register))
suite.addTests(loader.loadTestsFromModule(test_login))
suite.addTests(loader.loadTestsFromModule(test_recharge))
suite.addTests(loader.loadTestsFromModule(test_withdraw))
suite.addTests(loader.loadTestsFromModule(test_addloan))

#执行用例 生成测试报告
with open(project_path.report_path,'wb') as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                            verbosity=2,
                                            title='Combat_API_qcd',
                                            description='前程贷接口自动化测试报告',
                                            tester='tanxi')

    runner.run(suite)


