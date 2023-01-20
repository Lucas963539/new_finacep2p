import pymysql


class DBUtil:
    __conn = None

    # 获取数据库连接对象
    @classmethod
    def get_conn(cls):
        if cls.__conn is None:
            # cls.__conn = pymysql.connect("localhost", "root", "root", "p2p_mock")
            cls.__conn = pymysql.connect("localhost", "root", "iTest_2019_mysql", "p2p_mock")
        return cls.__conn

    # 关闭数据库连接对象
    @classmethod
    def close_conn(cls):
        if cls.__conn:
            cls.__conn.close()
            cls.__conn = None

    # 获取游标对象
    @classmethod
    def get_cursor(cls):
        # return cls.__conn.cursor()
        return cls.get_conn().cursor()

    # 关闭游标对象
    @classmethod
    def close_cursor(cls, cursor):
        if cursor:
            cursor.close()

    # 查询一条记录
    @classmethod
    def get_one(cls, sql):
        cursor = DBUtil.get_cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        DBUtil.close_cursor(cursor)
        DBUtil.close_conn()
        return result


if __name__ == '__main__':
    result = DBUtil.get_one("select * from t_book where id=1")
    print("result==", result)
