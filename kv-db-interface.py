from sqlalchemy.ext.declarative import declarative_base
import argparse
from sqlalchemy import *
from sqlalchemy.orm import *
import json
import re
import sys

class KeyValue(declarative_base()):
    __tablename__ = "kvtable"

    id = Column(Integer, primary_key=True)
    key = Column(String(), nullable=False, unique=True)
    value = Column(BLOB, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value


class KeyValueDatabaseInterface(object):
    """
    An interface class for a simple Key-Value Relational Database. Has several different CRUD methods
    """
    def __init__(self, connection_string=None, connection_file=None):
        conn_string = "sqlite:///kv_db.db"
        if connection_string is not None:
            conn_string = connection_string
        elif connection_file is not None:
            conn_string = self.get_db_connection_string_from_settings_file()

        print("Connecting to: %s" % conn_string)
        db_engine = create_engine(conn_string)
        declarative_base().metadata.create_all(db_engine)
        declarative_base().metadata.bind = db_engine

        self.session = sessionmaker(bind=db_engine)()


    def _convert_to_supported_type(self, value):
        """
        Private function that converts a value to bytes so that it can be inserted as a blob in the database.

        :param value: the value to be converted to bytes
        :return: value
        :rtype: bytes
        """
        if type(value) is str:
            return bytes(value, 'UTF-8')
        elif type(value) is int:
            return value.to_bytes(value.bit_length() + 7, byteorder="little")
        # TODO: add other cases
        else:
            raise TypeError("Type %s is not supported." % str(type(value)))


    def get_db_connection_string_from_settings_file(self, filename="settings.json"):
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

    def get_all(self):
        """
        A method that returns all the Key-Value pairs in the database

        :return: list of all Key-Value pairs from the database
        :rtype: List<KeyValue>
        """
        return self.session.query(KeyValue).all()

    def get(self, key):
        """
        Returns the entry associated with the key.

        :param key: the key of the entry to be retrieved from the database
        :type key: string
        :return: entry associated with that key
        :rtype: KeyValue
        """
        return self.session.query(KeyValue).filter(KeyValue.key == key).first()

    def get_multiple(self, keys):
        """
        Returns a list of entries associated with the provided keys.

        :param keys: A list of keys for which to retrieve the entries from the database.
        :type keys: List<string>
        :return: A list of Key-Value pairs
        :rtype: List<KeyValue>
        """
        if type(keys) is not list:
            raise TypeError("A list of keys is expected. Got %s instead." % str(type(keys)))
        return self.session.query(KeyValue).filter(KeyValue.key.in_(keys)).all()

    def insert(self, key, value):
        """
        Insert a single entry into the database.

        :param key: The key for the entry.
        :type key: string
        :param value: The associated value.
        :return: True is the insertion was successful; False otherwise.
        :rtype: bool
        """
        try:
            self.session.add(KeyValue(key, self._convert_to_supported_type(value)))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("Exception encountered %s" % e.with_traceback(sys.exc_info()[2]))
            return False
        return True

    def insert_multiple(self, kv_values):
        """
        Insert multiple Key-Value entries.
        :param kv_values: A set of Key-Value pairs.
        :type kv_values: List<Tuple, List, or Dictionary> or Dictionary<string,value>
        :return: True is the insertions were successful; False otherwise.
        :rtype: bool
        """
        try:
            if type(kv_values) is not dict and type(kv_values) is not list:
                raise TypeError("Type %s is not supported." % str(type(kv_values)))

            def add_dict(session, dictionary):
                for key in list(dictionary.keys()):
                    session.add(KeyValue(key, self._convert_to_supported_type(dictionary[key])))

            if type(kv_values) is dict:
                add_dict(kv_values)

            if type(kv_values) is list:
                for entry in kv_values:
                    if type(entry) is tuple or type(entry) is list:
                        self.session.add(KeyValue(entry[0], self._convert_to_supported_type(entry[1])))
                    if type(entry) is dict:
                        add_dict(self.session, entry)

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("Exception encountered %s" % e.with_traceback(sys.exc_info()[2]))
            return False
        return True

    def update(self, key, value):
        """
        Updates the entry associated with the key with the value provided.
        :param key: the entry's key
        :param value: the new value of the entry
        :return: void
        """
        kv_entry = self.get(key)
        kv_entry.value = self._convert_to_supported_type(value)
        self.session.commit()

    def remove(self, keys):
        """
        Remove the entries associate with the keys provided.
        :param keys:
        :type keys: List<string>
        :return: void
        """
        if type(keys) is not list:
            raise TypeError("A list of keys is expected. Got %s instead." % str(type(keys)))
        for kv_entry in self.get_multiple(keys):
            self.session.delete(kv_entry)
        self.session.commit()


def test():
    kvDb = KeyValueDatabaseInterface(connection_file='settings.json')
    # insert() TEST
    print("insert() test... "),
    kvDb.insert("1", "original")
    kvDb.insert("2", 1)

    # insert_multiple() TEST
    print("insert_multiple() test... ")
    kvDb.insert_multiple([("3", "4"), ["4", "5"], {"6": "7"}])

    # get() TEST
    print("get() test... ")
    results = kvDb.get("2")
    print(results.key, int.from_bytes(results.value, byteorder="little"))

    # get_all() TEST
    print("get_all() test... ")
    results = kvDb.get_all()
    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

    # get_multiple() TEST
    print("get_multiple() test... ")
    results = kvDb.get_multiple(["1", "2"])
    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

    # update() TEST
    print("update() test... ")
    kvDb.update("1", "updated")
    results = kvDb.get("1")
    print(results.key, int.from_bytes(results.value, byteorder="little"))

    # remove() TEST
    print("remove() test... ")
    kvDb.remove(["1", "2", "3", "4", "5", "6", "7"])
    results = kvDb.get_all()
    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))
    print("Done.")
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
        test()
    except KeyboardInterrupt:
        print("Program ended by user.")

    exit(0)
