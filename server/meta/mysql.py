#_*_ coding: utf-8 _*_


import mysql.connector
from .schema import DBSchema, Table


class MySQLSChema(DBSchema):

    def _init_conn(self):
        if self._meta.conn is not None:
            self._meta.conn.close()
            self._meta.conn = None

        self._meta.conn = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='classicmodels'
        )

    def _close_conn(self):
        if self._meta.conn is not None:
            self._meta.conn.close()

    def _get_tables(self):
        qry = "select table_name from information_schema.tables" \
              " where table_schema in ('classicmodels')"
        crs = self._meta.conn.cursor()
        crs.execute(qry)
        t = dict()
        for (table_name, ) in crs:
            t[table_name] = Table(name=table_name)
        return t
