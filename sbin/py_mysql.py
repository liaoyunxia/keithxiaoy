import sys

import MySQLdb as mysql
import syslog


class MysqlClient():
    def __init__(self, TEST_ENV):
        """mysql info"""
        if TEST_ENV:
            self.dbHost = 'testcmcaifu.mysql.rds.aliyuncs.com'
            self.dbUser = 'django'
            self.dbPass = '88888888'
            self.dbName = 'factoring_default'
        else:
            self.dbHost = 'cmcaifudefault.mysql.rds.aliyuncs.com'
            self.dbUser = 'django'
            self.dbPass = '88888888'
            self.dbName = 'cmcaifu_default'
        self.port = 3306
        self._conn()

    def _conn(self):
        '''mysql connect'''
        self.conn = mysql.Connection(self.dbHost, self.dbUser, self.dbPass, self.dbName, int(self.port), charset='utf8mb4')
        self.conn.autocommit(True)
        self.conn.select_db(self.dbName)
        self.cur = self.conn.cursor()
        self.setName()

    def setName(self):
        '''set name for utf-8'''
        self.cur.execute("SET NAMES 'utf8'")
        self.cur.execute("SET CHARACTER SET 'utf8'")
        self.cur.execute('SET character_set_connection=utf8;')

    def _close(self):
        '''close the mysql connect'''
        # self.cur.close()

    def selectQuery(self, params):
        par = ','.join(params['name'])
        sql = "select " + par + " from " + params['tbl'] + " " + params['prefix']
        self.sql = sql
        self.queryNum = self.cur.execute(sql)
        self.params = params

    def query(self, sql):
        try:
            self.queryNum = self.cur.execute(sql.encode('utf-8'))
            return True
        except Exception as e:
            self.write_log('query_error', '{}'.format(e))
            return False

    def getSql(self):
        fetch = self.cur.fetchall()
        for inv in fetch:
            yield dict(zip(self.params['name'], inv))

    def fn(self):
        return self.cur.rowcount

    def getTableList(self, tblName):
        try:
            self.cur.execute("desc " + tblName)
            return [row[0] for row in self.cur.fetchall()]
        except:
            sys.exit(0)

    def getDbList(self):
        try:
            self.cur.execute("show tables")
            return [row[0] for row in self.cur.fetchall()]
        except:
            sys.exit(0)

    def __del__(self):
        try:
            self.__close__()
        except:
            "the connect could not close"

    def write_log(self, method, msg):
        syslog.openlog(method, syslog.LOG_LOCAL0)
        syslog.syslog(syslog.LOG_INFO, msg)

    def close(self):
        self.conn.close()
