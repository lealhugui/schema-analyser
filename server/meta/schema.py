#_*_ coding: utf-8 _*_

SCHEMA_TYPES = (
    "MY_SQL",
)

class Table(object):
    """DataBase Table representation"""

    class _meta:
        pass

    name = None
    db_schema = None
    columns = []

    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.pop("name")
        if "db_schema" in kwargs:
            self.db_schema = kwargs.pop("db_schema")

        for k in kwargs:
            setattr(self._meta, k, kwargs[k])

    def __str__(self):
        cols = ""
        for col in self.columns:
            cols += "{}".format(self.columns[col].name) if cols == "" else ", {}".format(self.columns[col].name)
        return "{}.{}[{}]".format(self.db_schema, self.name, cols)

class Column(object):
    """Database Table's column representation"""

    class _meta:
        pass

    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.pop("name")

        for k in kwargs:
            setattr(self._meta, k, kwargs[k])


class DBSchema(object):
    """Database Schema connector Abstract Class"""
    class _meta:
        conn = None
        tables = None
        work_schemas = None
        database = None

    def __init__(self, database, schemas=[]):
        self._meta.database = database
        self._meta.work_schemas = schemas

    def __enter__(self):
        self._init_conn(self._meta.database, self._meta.work_schemas)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close_conn()

    @property
    def tables(self):
        """Tables from schema"""
        if self._meta.tables is None:
            self._meta.tables = self._get_tables()
        return self._meta.tables

    def _init_conn(self, db_name, schemas=[]):
        """Abstract method for initializing the connection"""
        pass

    def _close_conn(self):
        """Abstract method for closing the connection"""
        pass

    def _get_tables(self):
        """Abstract method for getting all the tables from the defined work schemas"""
        pass
    
    def _get_table_columns(self, table):
        """Abstract method for getting a list of table columns instance"""
        if not isinstance(table, Table):
            raise Exception("Not a table Instance")


