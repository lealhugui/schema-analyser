# _*_ coding: utf-8 _*_


SCHEMA_TYPES = (
    "MYSQL",
    "MSSQL",
    "PGSQL",
)


def meta_factory():
    sub = tuple()
    attr = dict()
    return type('_meta', sub, attr)


class TableSize(object):

    table_size = None
    index_size = None

    def __init__(self, table_size, index_size):
        self.table_size = table_size
        self.index_size = index_size

class Table(object):
    """DataBase Table representation"""

    class _meta:
        pass

    name = None
    db_schema = None    

    _columns = _fks = _refs = _table_size = None

    def __init__(self, **kwargs):
        if self._meta is not None:
            self._meta = meta_factory()

        if "name" in kwargs:
            self.name = kwargs.pop("name")
        if "db_schema" in kwargs:
            self.db_schema = kwargs.pop("db_schema")

        if "table_size" in kwargs:
            self.table_size = kwargs.pop("table_size")

        for k in kwargs:
            setattr(self._meta, k, kwargs[k])

    def __str__(self):
        cols = ""
        for col in self.columns:
            cols += "{}".format(self.columns[col].name) if cols == "" else ", {}".format(self.columns[col].name)
        reffs = ""
        for fk in self.fk_refs:
            reffs += "{}".format(self.fk_refs[fk].name) if reffs == "" else ", {}".format(self.fk_refs[fk].name)
        fkss = ""
        for fk in self.fks:
            fkss += "{}".format(self.fks[fk].name) if fkss == "" else ", {}".format(self.fks[fk].name)
        return "{}.{}\n[{}]\n(fks:{})\n(refs:{})".format(self.db_schema, self.name, cols, fkss, reffs)

    def set_properties(self, dbschema_instance):
        """Global setter for the properties. It should recieve an DBSchema instance and it will load the
        dicts containing colums, fks, and fk_refs"""
        if not issubclass(dbschema_instance.__class__, DBSchema):
            raise ValueError("dbschema_instance is not a valid DBSchema")

        self._columns = dbschema_instance._get_table_columns(self)
        self._fks = dbschema_instance._get_fks(self)
        self._refs = dbschema_instance._get_refs(self)
        self._pk = dbschema_instance._get_pk(self)

    @property
    def columns(self):
        """Columns of the table"""
        return self._columns

    @property
    def fks(self):
        """Foreign Keys on the table"""
        return self._fks

    @property
    def fk_refs(self):
        """Foreign Keys pointing to the table"""
        return self._refs

    @property
    def pk(self):
        """Primary Keys of the table"""
        return self._pk
    
    @property
    def table_size(self, dbschema_instance):
        if self._table_size is None:
            self._table_size = dbschema_instance._get_table_size(self)
        return self._table_size


class Column(object):
    """Database Table's column representation"""

    class _meta:
        pass

    def __init__(self, **kwargs):

        self.name = None
        self.column_type = None
        self.allow_null = None

        if self._meta is not None:
            self._meta = meta_factory()

        if "name" in kwargs:
            self.name = kwargs.pop("name")

        if "column_type" in kwargs:
            self.column_type = kwargs.pop("column_type")

        if "allow_null" in kwargs:
            self.allow_null = kwargs.pop("allow_null")

        for k in kwargs:
            setattr(self._meta, k, kwargs[k])


class ForeignKey(object):

    class _meta:
        pass

    def __init__(self, **kwargs):
        if self._meta is not None:
            self._meta = meta_factory()
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

    def _init_conn(self, db_dict, schemas=[]):
        """Abstract method for initializing the connection"""
        raise NotImplementedError()

    def _close_conn(self):
        """Abstract method for closing the connection"""
        raise NotImplementedError()

    def get_table_info(self, table_schema, table_name, is_lazy = True):
        """Abstract method for returning ONE table information"""
        table = Table(name=table_name, db_schema=table_schema)
        if not is_lazy:
            table.set_properties(self)


    def _get_tables(self):
        """Abstract method for getting all the tables from the defined work schemas"""
        raise NotImplementedError()

    def _get_table_columns(self, table_instance):
        """Abstract method for getting a list of table columns instance"""
        raise NotImplementedError()

    def _get_fks(self, table_instance):
        """Abstract method for getting all Foreign Keys on a table"""
        raise NotImplementedError()

    def _get_refs(self, table_instance):
        """Abstract method for getting all Foreign Keys referencing a table"""
        raise NotImplementedError()

    def _get_pk(self, table_instance):
        """Abstract method for getting all Columns of the Table's PK"""
        raise NotImplementedError()

    def _get_table_size(self, table_instance):
        """Abstract method for getting the table disk usage information"""
        raise NotImplementedError()