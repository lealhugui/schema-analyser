# _*_ coding: utf-8 _*_

from server.meta import get_schema_instance
# import json


def main():
	"""Main script mode function"""
	with get_schema_instance("MSSQL", ['SIS_OS_ERPCL_DESENV', ]) as s:
		s.tables


if __name__ == "__main__":
	main()
