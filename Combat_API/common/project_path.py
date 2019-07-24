# -*-coding:utf-8-*-
# @Time      :2019/3/13/013 12:45
# @Author    :Tanxi
# @Email     :1410510771@qq.com
# @File      :project_path.py
# @Software  :PyCharm Community Edition

import os

#获取当前项目所在路径（通过获取当前文件路径，再切割的方式）
project_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

#测试用例路径
case_path=os.path.join(project_path,'test_case','TestCase.xlsx')

#日志存放路径
log_path=os.path.join(project_path,'test_result','test_log','testlog.log')

#配置文件存放路径
conf_path=os.path.join(project_path,'config','config.conf')

#测试报告存放路径
report_path=os.path.join(project_path,'test_result','test_report','TestReport.html')

