# Python Interface for a Key-Value Database

This is a Python module that provides an interface, the `KeyValueDatabaseInterface()` class, for a simple Key-Value 
Database.  If such a database does not exists, it creates ones using [SQLAlchemy](https://www.sqlalchemy.org/). 
The interface has several CRUD methods so that it can interface with the database.

Some methods of the `KeyValueDatabaseInterface()` class return an object of type `KeyValue()`, which is a class used
to abstract the Key-Value entries in the database. **This can and probably will change in the future** so that the
implementation can be hidden. Instead, a dictionary or a tuple will probably be returned instead.

By default the module uses [SQLite3](https://www.sqlite.org/) as a database, but it can [support any of the ones
supported by SQLALchemy](https://docs.sqlalchemy.org/en/latest/core/engines.html).

## Database

Currently SQLite defaults as the default database. It's a local database saved to a `.db` file. You can open and view
their content using 

## Python Google Protocol Buffer Message() Class Document

Google provides document on the Python Protobuf classes: <https://developers.google.com/protocol-buffers/docs/reference/python/>.
The [Message() class](https://developers.google.com/protocol-buffers/docs/reference/python/google.protobuf.message.Message-class) 
is of particular use.

## KeyValueDatabaseInterface Methods

`KeyValueDatabaseInterface()`: An interface class for a simple Key-Value Relational Database. Has several different
CRUD methods

`get_all()`: A method that returns all the Key-Value pairs in the database
* return: list of all Key-Value pairs from the database
* rtype: List<KeyValue>

`get(key)`: Returns the entry associated with the key.
* param key: the key of the entry to be retrieved from the database
* type key: string
* return: entry associated with that key
* rtype: KeyValue
 
`get_multiple(keys)`: Returns a list of entries associated with the provided keys.
* param keys: A list of keys for which to retrieve the entries from the database.
* type keys: List<string>
* return: A list of Key-Value pairs
* rtype: List<KeyValue>

`insert(self, key, value)`: Insert a single entry into the database.
* param key: The key for the entry.
* type key: string
* param value: The associated value.
* return: True is the insertion was successful; False otherwise.
* rtype: bool

`insert_multiple(kv_values)`: Insert multiple Key-Value entries.
* param kv_values: A set of Key-Value pairs.
* type kv_values: List<Tuple, List, or Dictionary> or Dictionary<string,value>
* return: True is the insertions were successful; False otherwise.
* rtype: bool

`update(key, value)`: Updates the entry associated with the key with the value provided.
* param key: the entry's key
* param value: the new value of the entry
* return: void
        
`remove(keys)`: Remove the entries associate with the keys provided.
* param keys: The keys of the entries to remove
* type keys: List<string>
* return: void


## Examples

There are two example python files in the project:
* `example.py` shows how to use the custom Key-Value interface; and
* `example_protobuf.py` shows how add a serialized protocol buffer.