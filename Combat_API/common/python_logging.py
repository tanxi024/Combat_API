# -*-coding:utf-8-*-
# @Time      :2019/2/28/028 13:11
# @Author    :Tanxi
# @Email     :1410510771@qq.com
# @File      :python_logging.py
# @Software  :PyCharm Community Edition

# 1：编写一个日志类，能够实现输出文件到指定文件和console
# 2：结合配置文件类实现日志类的可配置，具体参考老师的代码以及视频
# 3：结合日志类以及do_excel类，加上异常判断 与日志输出

import logging

from Combat_API.common import project_path, read_config


class MyLogger():

    def __init__(self):
        t = read_config.ReadConfig(project_path.conf_path)

        self.logger_name = t.read_str('log', 'logger_name')
        self.logger_level = t.read_str('log', 'logger_level')

        self.handlerno = t.read_int('log', 'handlerno')
        self.handler_level = t.read_str('log', 'handler_level')
        self.formatter = t.read_str('log','formatter')
        self.filename = project_path.log_path

    def my_logger(self,level,msg):
        #1、定义一个日志收集器，设置级别 getLogger setLevel
        mylogger=logging.getLogger(self.logger_name)
        mylogger.setLevel(self.logger_level)

        #2、指定输出渠道，设置级别 StreamHandler--控制台 FileHandler 输出指定文件 ||日志格式与输出渠道相关
        formatter=logging.Formatter(self.formatter)
        if self.handlerno==1: #指定输出渠道到控制台
            handler=logging.StreamHandler()
            handler.setLevel(self.handler_level)#设置级别
            handler.setFormatter(formatter)#设置日志信息格式
        else: #输出到指定文件

            handler=logging.FileHandler(self.filename,encoding='utf-8')
            handler.setLevel(self.handler_level)#设置级别
            handler.setFormatter(formatter)#设置日志信息格式

        #3、对接
        mylogger.addHandler(handler)
        # #判断最终输出的日志级别
        # if self.logger_level=='CRITICAL':
        #     level=self.logger_level
        # elif self.logger_level=='ERROR' and self.handler_level!='CRITICAL':
        #     level=self.logger_level
        # elif self.logger_level=='WARNING' and self.handler_level in ('DEBUG','INFO','WARNING'):
        #     level=self.logger_level
        # elif self.logger_level=='INFO' and self.handler_level in ('DEBUG','INFO'):
        #     level = self.logger_level
        # else:
        #     level=self.handler_level

        if level=='DEBUG':
            mylogger.debug(msg)
        elif level=='INFO':
            mylogger.info(msg)
        elif level == 'WARNING':
            mylogger.warning(msg)
        elif level == 'ERROR':
            mylogger.error(msg)
        else:
            mylogger.critical(msg)

        #最后需要记得移除输出渠道
        mylogger.removeHandler(handler)

    def debug(self,msg):
        self.my_logger('DUBUG',msg)

    def info(self,msg):
        self.my_logger('INFO',msg)

    def warning(self,msg):
        self.my_logger('WARNING',msg)

    def error(self,msg):
        self.my_logger('ERROR',msg)

    def critical(self,msg):
        self.my_logger('CRITICAL',msg)


# if __name__ == '__main__':
#     #MyLogger().my_logger('aaa')
#     MyLogger().info('bbb')
