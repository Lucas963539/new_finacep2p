import json
import logging.handlers
import os

import pymysql
from bs4 import BeautifulSoup

import yaml

from config import DIR_PATH, DB_HOST, DB_USER, DB_PWD, DB_NAME, DB_PORT


# 测试数据读取工具----json格式
def read_json(filename, key):
    file_path = DIR_PATH + os.sep + "data" + os.sep + filename
    with open(file_path, mode='r', encoding='utf-8') as f:
        arry = []
        result = json.load(f)
        for data in result.get(key):
            arry.append(tuple(data.values())[1:])
        return arry


# yaml格式测试数据读取
def read_yaml(filename, key):
    file_path = DIR_PATH + os.sep + "data" + os.sep + filename
    with open(file_path, mode='r', encoding='utf-8') as f:
        arry = []
        result = yaml.safe_load(f)
        # for data in result.get(key):
        #     data.get(value)
        #     print(data)
        # return data

        for data in result.get(key):
            arry.append(tuple(data.values())[1:])
        return arry


# 封装日志
class GetLog:

    @classmethod
    def get_log(cls):
        cls.log = None
        if cls.log is None:
            # 1. 获取日志器
            cls.log = logging.getLogger()
            # 设置日志器级别
            cls.log.setLevel(logging.INFO)
            # 2. 获取处理器
            # file_path = DIR_PATH + os.sep + "log" + os.sep + "{}.log".format(time.strftime("%Y%m%d"))
            file_path = DIR_PATH + os.sep + "log" + os.sep + "p2p_test.log"
            # TimedRotatingFileHandler 此方法可用来将日志保存到文件里，并且文件将按时间来分割
            tf = logging.handlers.TimedRotatingFileHandler(
                filename=file_path,
                when='midnight',  # 按多长时间保存
                interval=1,  # 保存的间隔时间
                backupCount=3,  # 备份数量
                encoding='utf-8'
            )
            # 3. 获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)
            # 4. 将格式器添加到处理器
            tf.setFormatter(fm)
            # 5. 将处理器添加到日志器中
            cls.log.addHandler(tf)
        return cls.log


# 封装提取HTML 工具
def parser_html(result):
    # 1. 获取html
    html = result.json().get('description').get('form')
    # 2.提取beatuifulsoup对象
    bs = BeautifulSoup(html, "html.parser")
    # 3. 提取url
    bs_url = bs.form.get('action')
    # 4. 查找遍历所有的input标签 5.遍历组装data  data={"SSS":"AAA","XXX":"VVV"}
    data = {}
    for bs_input in bs.find_all('input'):
        # bs.find_all('input'):<input name='Version' type='hidden' value='10'/><input name='CmdId' type='hidden' value='UserRegister'/>...

        data[bs_input.get('name')] = bs_input.get('value')
        # data={ "Version":"10","CmdId":"UserRegister"}
    return bs_url, data


"""
    分析：SQL如果是查询语句就返回所有结果
            如果是非查询语句（DML）就返回受影响行数
"""


# 封装数据库工具
def conn_mysql(sql):
    conn = None
    cursor = None
    try:
        # 1. 创建链接对象
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PWD,
            database=DB_NAME,
            port=DB_PORT,
            charset="utf8",
            autocommit=True
        )

        # 2. 创建游标对象
        cursor = conn.cursor()
        # 3. 执行SQL语句
        cursor.execute(sql)
        # 判定SQL是否为查询语句，如果是就返回所有结果
        keyword = sql.split()[0].lower()
        if keyword == "select":
            result = cursor.fetchall()
            print(f'查询结果为：{result}')
            return result
        # 如果不是就返回受影响行数
        else:
            result = cursor.rowcount
            print(f"影响行数为：{result}")
            return result
    except Exception as e:
        print(f'SQL语句执行有误，错误信息：{e}')
        GetLog().get_log().error(e)
        # 语句执行失败，回滚数据
        conn.rollback()
        raise

    finally:
        # 4. 关闭游标
        cursor.close()
        # 5.关闭连接
        conn.close()


# 封装清除数据工具
def clean_data():
    # 1.删除 mb_member_info
    sql1 = """
    delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id=m.id where m.phone in ("1360000001","1360000002","1360000003","1360000004");
    """
    conn_mysql(sql1)

    # 2.删除 mb_member_login_log
    sql2 = """
    delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id=m.id where m.phone in ("1360000001","1360000002","1360000003","1360000004");
    """
    conn_mysql(sql2)

    # 3.删除 mb_member_register_log
    sql3 = """
    delete from mb_member_register_log where phone in ("1360000001","1360000002","1360000003","1360000004");
    """
    conn_mysql(sql3)

    # 4.删除 mb_member
    sql4 = """
    delete from mb_member where phone in ("1360000001","1360000002","1360000003","1360000004");
    """
    conn_mysql(sql4)






if __name__ == '__main__':
    # print(read_json("tender_data.json", "tender"))
    # print(read_yaml("approve_trust.yaml", "img_code"))

    # GetLog.get_log().info("信息级别测试")
    ## --alluredir='/Users/jiangcheng/PycharmProjects/new_finacep2p/allure_result' --clean-alluredir
    # parser_html()
    sql = "select * from student"
    sql2 = "delete from student where name = 'ToM'"
    print(conn_mysql(sql2))