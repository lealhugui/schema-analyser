#_*_ coding: utf-8 _*_

from .schema import SCHEMA_TYPES
from .mysql import MySQLSChema

def get_schema_instance(db_type):
    """Factory"""
    if db_type not in SCHEMA_TYPES:
        raise Exception("Unknow schema type")

    if db_type == "MY_SQL":
        return MySQLSChema()