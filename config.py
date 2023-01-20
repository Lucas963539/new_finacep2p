# 全局项目地址
import os

HOST = "http://user-p2p-test.itheima.net"

# 全局项目路径 --->  /Users/jiangcheng/PycharmProjects/new_finacep2p
DIR_PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    print(DIR_PATH + "/member/public/login")

# 全局数据库连接参数
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PWD = "Jc18723132997"
DB_PORT = 3306
DB_NAME= "mytest"
DB_CHARSET = "utf8"
DB_AUTOCOMMIT = True



