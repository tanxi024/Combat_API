# -*-coding:utf-8-*-
# @Time      :2019/3/10/010 10:29
# @Author    :Tanxi
# @Email     :1410510771@qq.com
# @File      :shizhan_1.py
# @Software  :PyCharm Community Edition

# 1：根据提供的注册登录接口，完成注册登录接口的请求，至少每个接口有5条用例，每个接口要至少有一个正向用例。
# 见TestCase_0310

# 2：要求如下：
# 1）http请求类（可以根据传递的method--get/post完成不同的请求），要求有返回值。
# 2）测试用例的数据存储在Excel中，并编写一个从Excel中读取数据的测试类，包含的函数能够读取测试数据，并且能够写回测试结果，要求有返回值。
# 3）新建一个run.py文件，在这里面完成Excel数据的读取以及完成用例的执行，并写回测试结果到Excel文档里面。
#    至此已经完成了接口自动化测试的第一步。

import requests
from Combat_API.common.python_logging import MyLogger

log = MyLogger()


class HttpRequest:
    def __init__(self, url, method):
        self.url = url
        self.method = method

    def http_request(self, module, interface_name, params, cookies=None):
        '''
        根据请求方法选择get或post，发起请求
        :param module:所有模块，用来拼接请求地址
        :param interface_name: 接口名，用来拼接请求地址
        :param params:请求参数
        :param cookies:请求的cookies
        :return:
        '''

        url = self.url + '/' + module + '/' + interface_name
        log.info('请求地址为：{}'.format(url))
        if self.method == 'get':
            req = requests.get(url, params=params, cookies=cookies)
        else:
            req = requests.post(url, data=params, cookies=cookies)
        log.info('返回结果为：{}'.format(req.text))
        return req
        # return req.json()

        # if __name__ == '__main__':
        #     t=HttpRequest('http://47.107.168.87:8080/futureloan/mvc/api','post')
        #     res=t.http_request('member','register',{"mobilephone":"15211467285","pwd":"t123456","regname":"Tan"})
        #     print(json.dumps(res))
        #     print(type(json.loads(res)))
