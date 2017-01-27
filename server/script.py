#_*_ coding: utf-8 _*_

from meta import get_schema_instance

def main():
    """Main script mode function"""

    with get_schema_instance("MY_SQL") as s:
        print(s)
        print([s.tables[t].name for t in s.tables])

if __name__ != "__main__":
    raise Exception("Script mode should not be imported!")
else:
    main()
