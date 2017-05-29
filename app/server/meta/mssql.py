# _*_ coding: utf-8 _*_

# TODO: there is a TOP X in the main query, just for the testing

import pymssql
from .schema import DBSchema, Table, Column, ForeignKey


class MSSqlSchema(DBSchema):
	"""Introspection class for MS SQL Server Database"""

	def _init_conn(self, db_dict, schemas=[]):
		if self._meta.conn is not None:
			try:
				self._meta.conn.close()
			except Exception:
				pass
		self._meta.conn = None
		self._meta.work_schemas = schemas

		conn = pymssql.connect(
			user=db_dict["USER"],
			password=db_dict["PASSWORD"],
			host=db_dict["HOST"],
			database=db_dict["NAME"])

		self._meta.conn = conn

	def _close_conn(self):
		if self._meta.conn is not None:
			try:
				self._meta.conn.close()
			except Exception:
				pass

	def _get_tables(self):

		qry = "select TOP 50 TABLE_NAME, TABLE_CATALOG from information_schema.tables where TABLE_TYPE != 'VIEW' "
		if len(self._meta.work_schemas) > 0:
			schemas = ""
			for scm in self._meta.work_schemas:
				schemas += "'{}'".format(scm) if schemas == "" else ", '{}'".format(scm)
			qry += " and TABLE_CATALOG in ({})".format(schemas)
		result = dict()
		with self._meta.conn.cursor(as_dict=True) as crs:
			crs.execute(qry)
			tbls = crs.fetchall()

			for tbl in tbls:
				table_inst = Table(
					name=tbl.pop("TABLE_NAME"),
					db_schema=tbl.pop("TABLE_CATALOG"),
					**tbl)
				table_inst.set_properties(self)
				result[table_inst.name] = table_inst

			# for k in result:
			# 	result[k].set_properties(self)

		return result

	def _get_table_columns(self, table_instance):
		qry = "" \
			"select COLUMN_NAME, DATA_TYPE, IS_NULLABLE from information_schema.columns " \
			"where TABLE_CATALOG='{}' and table_name='{}'".format(
				table_instance.db_schema,
				table_instance.name
			)
		with self._meta.conn.cursor(as_dict=True) as crs:
			crs.execute(qry)
			colmns = crs.fetchall()
			result = dict()
			for clm in colmns:

				clm_inst = Column(
					name=clm.pop("COLUMN_NAME"),
					column_type=clm.pop("DATA_TYPE"),
					allow_null=clm.pop("IS_NULLABLE") == "YES",
					**clm
				)
				result[clm_inst.name] = clm_inst
		return result

	def _get_fks(self, table_instance):
		qry = "" \
			" SELECT O.NAME AS CONSTRAINT_NAME      " \
			" FROM 											" \
			" 	SYS.FOREIGN_KEY_COLUMNS AS FK				" \
			" 	INNER JOIN SYS.OBJECTS O ON O.OBJECT_ID = 	" \
			" 	FK.CONSTRAINT_OBJECT_ID						" \
			" WHERE 										" \
			" 	FK.PARENT_OBJECT_ID = (						" \
			" 		SELECT OBJECT_ID FROM SYS.TABLES		" \
			" 		WHERE NAME='{}'							" \
			" 	) GROUP BY O.NAME							".format(
				table_instance.name
			)

		with self._meta.conn.cursor(as_dict=True) as crs:
			crs.execute(qry)
			foreign_keys = crs.fetchall()
			result = dict()
			for fkey in foreign_keys:
				fk_inst = ForeignKey(name=fkey.pop("CONSTRAINT_NAME"), **fkey)
				result[fk_inst.name] = fk_inst
		return result

	def _get_refs(self, table_instance):
		qry = "" \
			" SELECT O.NAME AS CONSTRAINT_NAME      " \
			" FROM 											" \
			" 	SYS.FOREIGN_KEY_COLUMNS AS FK				" \
			" 	INNER JOIN SYS.OBJECTS O ON O.OBJECT_ID = 	" \
			" 	FK.CONSTRAINT_OBJECT_ID						" \
			" WHERE 										" \
			" 	FK.REFERENCED_OBJECT_ID = (					" \
			" 		SELECT OBJECT_ID FROM SYS.TABLES		" \
			" 		WHERE NAME='{}'							" \
			" 	) GROUP BY O.NAME							".format(
				table_instance.name
			)

		with self._meta.conn.cursor(as_dict=True) as crs:
			crs.execute(qry)
			foreign_keys = crs.fetchall()
			result = dict()
			for fkey in foreign_keys:
				fk_inst = ForeignKey(name=fkey.pop("CONSTRAINT_NAME"), **fkey)
				result[fk_inst.name] = fk_inst
		return result

	def _get_pk(self, table_instance):
		colmns = ", ".join(["'{}'".format(k) for k in table_instance.columns])
		qry = "" \
			" SELECT k.COLUMN_NAME FROM information_schema.table_constraints t  " \
			" INNER JOIN information_schema.key_column_usage k  	  " \
			" ON k.constraint_name=t.constraint_name and			  " \
			"	k.TABLE_CATALOG=t.TABLE_CATALOG and 				  " \
			"	k.table_name=t.table_name							  " \
			" WHERE t.constraint_type='PRIMARY KEY'  				  " \
			" AND k.TABLE_CATALOG='{}'  							  " \
			" AND k.table_name='{}'									  " \
			" AND k.COLUMN_NAME IN ({}) 							  ".format(
				table_instance.db_schema,
				table_instance.name,
				colmns
			)
		with self._meta.conn.cursor(as_dict=True) as crs:
			crs.execute(qry)
			colmns = crs.fetchall()
			result = dict()
			for clm in colmns:
				clm_inst = Column(name=clm.pop("COLUMN_NAME"), **clm)
				result[clm_inst.name] = clm_inst
		return result
