#_*_ coding: utf-8 _*_

from meta import get_schema_instance

CACHE = None

def main():
    """Main script mode function"""

    db = "world"
    schemas = ["world"]
    with get_schema_instance("MY_SQL", db, schemas) as s:
        CACHE = s.tables
    print([str(CACHE[t]) for t in CACHE])



#if __name__ != "__main__":
#    raise Exception("Script mode should not be imported!")
#else:
#    main()

if __name__ == "__main__":
    main()
    