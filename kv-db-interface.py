from sqlalchemy.ext.declarative import declarative_base
import argparse
from sqlalchemy import *
from sqlalchemy.orm import *
import json
from pprint import pprint

Base = declarative_base()


class KeyValues(Base):
    __tablename__ = "kvtable"

    id = Column(Integer, primary_key=True)
    key = Column(String(), nullable=False, unique=True)
    value = Column(BLOB, nullable=False)


def main():
    json_data = open('settings.json').read()
    settings = json.loads(json_data)
    pprint(settings)

    sql_engine = settings['databaseEngine'] if 'databaseEngine' in json_data else 'sqlite'
    db_name = settings['databaseName'] if 'databaseName' in json_data else 'kv_db'
    hostname = settings['hostname'] if 'hostname' in json_data else ''

    if hostname == 'sqlite':
        hostname = ''

    db_engine = create_engine('%s://%s/%s.db' % (sql_engine, hostname, db_name))
    Base.metadata.create_all(db_engine)
    Base.metadata.bind = db_engine

    dbSession = sessionmaker(bind=db_engine)
    session = dbSession()
    
    return


def get_options():
    parser = argparse.ArgumentParser(
        description="Interface for a simple key-value database.",
        epilog="...",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    options = parser.parse_args()

    return options


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except KeyboardInterrupt:
        print("Program ended by user.")
        exit(0)
