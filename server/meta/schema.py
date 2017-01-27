#_*_ coding: utf-8 _*_

SCHEMA_TYPES = (
    "MY_SQL",
)

class Table(object):

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

class DBSchema(object):

    class _meta:
        conn = None
        tables = None

    def __enter__(self):
        self._init_conn()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close_conn()

    @property
    def tables(self):
        """Tables from schema"""
        if self._meta.tables is None:
            self._meta.tables = self._get_tables()
        return self._meta.tables

    def _init_conn(self):
        pass

    def _close_conn(self):
        pass

    def _get_tables(self):
        pass
