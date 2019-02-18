from sqlalchemy.ext.declarative import declarative_base
import argparse
from sqlalchemy import *
from sqlalchemy.orm import *
import json
import re
from pprint import pprint

Base = declarative_base()


class KeyValue(Base):
    __tablename__ = "kvtable"

    id = Column(Integer, primary_key=True)
    key = Column(String(), nullable=False, unique=True)
    value = Column(BLOB, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value


def get_db_connection_string_from_settings_file(filename="settings.json"):
    json_data = open(filename).read()
    settings = json.loads(json_data)
    # pprint(settings)

    # dialect+driver://username:password@host:port/database
    db_dialect = settings['databaseEngine'] if 'databaseEngine' in json_data else 'sqlite'
    db_driver = "+" + settings['driver'] if 'driver' in json_data else ''
    db_name = settings['databaseName'] if 'databaseName' in json_data else 'kv_db'
    db_username = settings['username'] if 'username' in json_data else ''
    db_password = settings['password'] if 'password' in json_data and len(db_username) > 0 else ''
    db_credentials = ""

    if len(db_username) > 0:
        db_credentials += db_username
        if len(db_password) > 0:
            db_credentials += ":" + db_password
        db_credentials += "@"
    hostname = settings['hostname'] if 'hostname' in json_data else 'localhost'

    port = settings['port'] if 'port' in json_data else None

    if port is not None and (port > 0):
        port = ":" + re.sub('[^0-9]', '', str(port))
    else:
        port = ''

    if db_dialect == 'sqlite':
        port = ''
        hostname = ''
        db_driver = ''
        db_credentials = ''

    return '%s%s://%s%s%s/%s.db' % (db_dialect, db_driver, db_credentials, hostname, port, db_name)


def get_all(session):
    return session.query(KeyValue).all()


def get(session, key):
    return session.query(KeyValue).filter(KeyValue.key == key).all()


def get_multiple(session, keys):
    if type(keys) is not list:
        raise TypeError("A list of keys is expected. Got %s instead." % str(type(keys)))
    raise NotImplemented


def insert(session, key, value):
    if type(value) is str:
        session.add(KeyValue(key, bytes(value, 'UTF-8')))
    elif type(value) is int:
        session.add(KeyValue(key, value.to_bytes(value.bit_length() + 7, byteorder="little")))
    # TODO: add other cases
    else:
        raise TypeError("Type %s is not supported." % str(type(value)))

    session.commit()
    return


"""
def insert(session, key_values):
    raise NotImplemented
"""


def update(session, key, value):
    raise NotImplemented


def main():
    conn_string = get_db_connection_string_from_settings_file()
    print("Connecting to: %s" % conn_string)

    db_engine = create_engine(conn_string)
    Base.metadata.create_all(db_engine)
    Base.metadata.bind = db_engine

    session = sessionmaker(bind=db_engine)()
    insert(session, "1", "somethingasdasd")
    insert(session, "2", 1)

    results = get(session, "2")
    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

    results = get_all(session)
    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

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
