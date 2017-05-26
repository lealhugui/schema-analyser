# _*_ coding: utf-8 _*_

from server.meta import get_schema_instance
import json

def main():
	"""Main script mode function"""
	l = list()
	CACHE = None
	with get_schema_instance("MSSQL", ['SIS_OS_ERPCL_DESENV', ]) as s:
		CACHE = s.tables
	for t in CACHE:
		l.append(t.__dict__)

	with open('dump.json', 'r') as j:
		j.write(json.dumps(l))


if __name__ == "__main__":
	main()
