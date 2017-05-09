#_*_ coding: utf-8 _*_


import pymysql.cursors
from .schema import DBSchema, Table, Column, ForeignKey


class MySQLSchema(DBSchema):

#    def __init__(self, database, schemas=[]):
#        super().__init__(database, schemas)

    def _init_conn(self, db_name, schemas=[]):
        if self._meta.conn is not None:
            self._meta.conn.close()
            self._meta.conn = None
        self._meta.work_schemas = schemas

        self._meta.conn = pymysql.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def _close_conn(self):
        if self._meta.conn is not None:
            self._meta.conn.close()

    def _get_tables(self):

        qry = "select * from information_schema.tables"
        if len(self._meta.work_schemas) > 0:
            schemas = ""
            for scm in self._meta.work_schemas:
                schemas += "'{}'".format(scm) if schemas == "" else ", '{}'".format(scm)
            qry += " where table_schema in ({})".format(schemas)
        result = dict()
        with self._meta.conn.cursor() as crs:
            crs.execute(qry)
            tbls = crs.fetchall()

            for tbl in tbls:
                table_inst = Table(
                    name=tbl.pop("TABLE_NAME"),
                    db_schema=tbl.pop("TABLE_SCHEMA"),
                    **tbl)
                table_inst.set_properties(self)
                result[table_inst.name] = table_inst

        return result

    def _get_table_columns(self, table_instance):
        qry = "select * from information_schema.columns " \
              "where table_schema='{}' and table_name='{}'".format(
                  table_instance.db_schema,
                  table_instance.name
              )
        with self._meta.conn.cursor() as crs:
            crs.execute(qry)
            colmns = crs.fetchall()
            result = dict()
            for clm in colmns:
                clm_inst = Column(name=clm.pop("COLUMN_NAME"), **clm)
                result[clm_inst.name] = clm_inst
        return result

    def _get_fks(self, table_instance):
        qry = " SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE" \
              " WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}' AND" \
              " REFERENCED_TABLE_NAME IS NOT NULL ".format(
                  table_instance.db_schema,
                  table_instance.name
              )
        
        with self._meta.conn.cursor() as crs:
            crs.execute(qry)
            foreign_keys = crs.fetchall()
            result = dict()
            for fkey in foreign_keys:
                fk_inst = ForeignKey(name=fkey.pop("CONSTRAINT_NAME"), **fkey)
                result[fk_inst.name] = fk_inst
        return result

    def _get_refs(self, table_instance):
        qry = " SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE" \
              " WHERE REFERENCED_TABLE_SCHEMA = '{}' " \
               "AND REFERENCED_TABLE_NAME = '{}'".format(
                  table_instance.db_schema,
                  table_instance.name
              )
        
        with self._meta.conn.cursor() as crs:
            crs.execute(qry)
            foreign_keys = crs.fetchall()
            result = dict()
            for fkey in foreign_keys:
                fk_inst = ForeignKey(name=fkey.pop("CONSTRAINT_NAME"), **fkey)
                result[fk_inst.name] = fk_inst
        return result        