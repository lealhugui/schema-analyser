# _*_ coding: utf-8 _*_

# 
import psycopg2
from  psycopg2.extras import DictCursor
from .schema import DBSchema, Table, Column, ForeignKey


class PGSchema(DBSchema):
	"""Introspection Schema for PostgreSQL Database"""

	def _init_conn(self, db_dict, schemas=[]):
		if self._meta.conn is not None:
			try:
				self._meta.conn.close()
			except Exception:
				pass
			self._meta.conn = None
		self._meta.work_schemas = schemas

		self._meta.conn = psycopg2.connect(
			user=db_dict["USER"],
			password=db_dict["PASSWORD"],
			host=db_dict["HOST"],
			database=db_dict["NAME"],
			cursor_factory=DictCursor
		)

	def _close_conn(self):
		if self._meta.conn is not None:
			try:
				self._meta.conn.close()
			except Exception:
				pass

	def _get_tables(self):

		qry = "select TABLE_NAME, TABLE_SCHEMA from information_schema.tables"
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
				tbl = dict(tbl)				
				table_inst = Table(
					name=tbl.pop("table_name", None),
					db_schema=tbl.pop("table_schema", None),
					**tbl)
				table_inst.set_properties(self)
				result[table_inst.name] = table_inst

		return result

	def _get_table_columns(self, table_instance):
		qry = "" \
			"select COLUMN_NAME, DATA_TYPE, IS_NULLABLE from information_schema.columns " \
			"where table_schema='{}' and table_name='{}'".format(
				table_instance.db_schema,
				table_instance.name
			)
		with self._meta.conn.cursor() as crs:
			crs.execute(qry)
			colmns = crs.fetchall()
			result = dict()
			for clm in colmns:
				clm = dict(clm)
				clm_inst = Column(
					name=clm.pop("column_name"),
					column_type=clm.pop("data_type"),
					allow_null=clm.pop("is_nullable") == "YES",
					**clm
				)
				result[clm_inst.name] = clm_inst
		return result

	def _get_fks(self, table_instance):
		qry = "" \
			"SELECT tc.constraint_name " \
			" FROM information_schema.table_constraints AS tc " \
			" JOIN information_schema.key_column_usage AS kcu " \
			"   ON tc.constraint_name = kcu.constraint_name " \
			" WHERE constraint_type = 'FOREIGN KEY' AND tc.TABLE_SCHEMA = '{}' AND tc.TABLE_NAME = '{}' ".format(
				table_instance.db_schema,
				table_instance.name
			)

		with self._meta.conn.cursor() as crs:
			crs.execute(qry)
			foreign_keys = crs.fetchall()
			result = dict()
			for fkey in foreign_keys:
				fkey = dict(fkey)
				fk_inst = ForeignKey(name=fkey.pop("constraint_name"), **fkey)
				result[fk_inst.name] = fk_inst
		return result

	def _get_refs(self, table_instance):
		qry = "" \
			" SELECT tc.constraint_name " \
			" FROM information_schema.table_constraints tc " \
			" JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name " \
			" JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name " \
			" WHERE constraint_type = 'FOREIGN KEY' " \
			" AND ccu.table_schema='{}' " \
			" AND ccu.table_name='{}' ".format(
				table_instance.db_schema,
				table_instance.name
			)

		with self._meta.conn.cursor() as crs:
			crs.execute(qry)
			foreign_keys = crs.fetchall()
			result = dict()
			for fkey in foreign_keys:
				fkey = dict(fkey)
				fk_inst = ForeignKey(name=fkey.pop("constraint_name"), **fkey)
				result[fk_inst.name] = fk_inst
		return result

	def _get_pk(self, table_instance):
		
		colmns = ", ".join(["'{}'".format(k) for k in table_instance.columns])
		qry = "" \
			" SELECT a.attname as COLUMN_NAME " \
			" FROM   pg_index i " \
			" JOIN   pg_attribute a ON a.attrelid = i.indrelid " \
			"					  AND a.attnum = ANY(i.indkey) " \
			" WHERE  i.indrelid = '{}.{}'::regclass " \
			" AND	i.indisprimary " \
			" AND   a.attname IN ({}) ".format(
				table_instance.db_schema,
				table_instance.name,
				colmns
			)
		
		with self._meta.conn.cursor() as crs:
			crs.execute(qry)
			colmns = crs.fetchall()
			result = dict()
			for clm in colmns:
				clm = dict(clm)
				clm_inst = Column(name=clm.pop("column_name"), **clm)
				result[clm_inst.name] = clm_inst
		return result