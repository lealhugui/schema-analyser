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

    _columns = _fks = _refs = None

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
        reffs = ""
        for fk in self.fk_refs:
            reffs += "{}".format(self.fk_refs[fk].name) if reffs == "" else ", {}".format(self.fk_refs[fk].name)
        fkss = ""
        for fk in self.fks:
            fkss += "{}".format(self.fks[fk].name) if fkss == "" else ", {}".format(self.fks[fk].name)            
        return "{}.{}\n[{}]\n(fks:{})\n(refs:{})".format(self.db_schema, self.name, cols, fkss, reffs)

    def set_properties(self, dbschema_instance):
        """Global setter for the properties. It should recieve an DBSchema instance and it will load the dicts containing colums, fks, and fk_refs"""
        if not issubclass(dbschema_instance.__class__, DBSchema):
            raise ValueError("dbschema_instance is not a valid DBSchema")

        self._columns = dbschema_instance._get_table_columns(self)
        self._fks = dbschema_instance._get_fks(self)
        self._refs = dbschema_instance._get_refs(self)

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

class Column(object):
    """Database Table's column representation"""

    class _meta:
        pass

    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.pop("name")

        for k in kwargs:
            setattr(self._meta, k, kwargs[k])

class ForeignKey(object):

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
        raise NotImplementedError()

    def _close_conn(self):
        """Abstract method for closing the connection"""
        raise NotImplementedError()

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


