#_*_ coding: utf-8 _*_

from .schema import SCHEMA_TYPES
from .mysql import MySQLSchema

import dj_database_url
def get_schema_instance(db_type, schemas=[]):
    """Factory of the DB_INSTANCE which will be used for DB introspection.
    Based on the db_type, the given env variable will be parsed as a
    '12 factor' database URL, and will be used as parameters for the DB
    connection.
    The format of the name of the env variable used will be:
    [db_type]_DATABASE_URL
    The value of the env variable must follow the standard:
    [db_type]://[user]:[password]@[host]/[db_name]

    More on these standards, on "https://github.com/kennethreitz/dj-database-url"
    """
    cfg = None
    if db_type not in SCHEMA_TYPES:
        raise Exception("Unknow schema type")

    if db_type == "MY_SQL":
        cfg = dj_database_url.config(env='MYSQL_DATABASE_URL')
        return MySQLSchema(cfg, schemas)
