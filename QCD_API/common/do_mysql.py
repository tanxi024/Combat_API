# _*_coding:utf-8_*_
# @Time     :2019/3/28 11:07
# @Author   :Tanxi
# @Email    :1410510771@qq.com
# @File     :do_mysql.py
# @Software :PyCharm Community Edition

from mysql import connector
from Combat_API.common.read_config import ReadConfig
from Combat_API.common import project_path


class DoMySql:
    '''操作数据库的类  查询'''
    def do_mysql(self, query, flag=1):
        '''
        :param query: 查询语句
        :param flag: 标志位 1-获取一条数据；2-获取多条数据
        :return:
        '''
        db_config = ReadConfig(project_path.conf_path).read_itera('DB', 'db_config')

        cnn = connector.connect(**db_config)#建立连接
        cursor = cnn.cursor()

        cursor.execute(query)

        if flag == 1:
            res = cursor.fetchone()
        else:
            res = cursor.fetchall()

        return res

if __name__ == '__main__':
    query='select LeaveAmount from member where mobilephone = "15211467285"'
    res=DoMySql().do_mysql(query,1)
    print('数据库的查询结果1：{}'.format(type(res[0])))