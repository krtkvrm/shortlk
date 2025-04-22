from __future__ import print_function
import pymysql as mysql
import os


class DB:
    def __init__(self, debug=False):
        self.db = mysql.connect(os.environ['db_host'],
                                os.environ['db_user'],
                                os.environ['db_passwd'],
                                os.environ['db_prod'])
        self.cursor = self.db.cursor()
        self.debug = debug

    def search(self, tables, columns="*", where='TRUE', index=''):
        if index:
            index = ""

        query = ""
                SELECT {0}
                FROM {1}
                WHERE {2};
                """.format(columns, tables, where)

        if self.debug:
            print(query)

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add(self, table, values, columns=''):
        if columns:
            columns = '({})'.format(columns)

        query = """
                INSERT INTO {0}{1}
                VALUES ({2}) ;
                """.format(table, columns, values)

        if self.debug:
            print(query)

        try:
            self.cursor.execute(query)
            self.db.commit()
            return 0
        except BaseException:
            self.db.rollback()
            return 1
