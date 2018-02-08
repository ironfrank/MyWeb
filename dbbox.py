#-*- coding:utf-8 -*-
import MySQLdb
import sys


class DB(object):
    dbconn = None
    dbcur = None
    sqlQueue = []

    def __init__(self, db_name, host_ip):
        # type: () -> object
        self.dbconn = MySQLdb.connect(
            host=host_ip,
            user='root',
            passwd='root',
            port=3306,
            charset='utf8')
        self.dbcur = self.dbconn.cursor()
        self.dbconn.select_db(db_name)

    def __del__(self):
        self.dbcur.close()
        self.dbconn.close()

    def query_tmp_table(self):
        self.dbcur.execute("SELECT id,type,name,url FROM tmp;")
        rows = self.dbcur.fetchall()  # all rows in table
        return rows

    def query_film_table(self, param):
        execute_sql = "SELECT name,link FROM resource_center WHERE name LIKE '%%%s%%' AND link!='';" % (
            param)
        self.dbcur.execute(execute_sql)
        rows = self.dbcur.fetchall()  # all rows in table
        return rows

    def query_type_table(self, type_param):
        self.dbcur.execute(
            "SELECT * FROM piaohua WHERE type='%s';" % (type_param))
        rows = self.dbcur.fetchall()  # all rows in table
        return rows
