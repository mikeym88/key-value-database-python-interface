# Python Interface for a Key-Value Database

This is a Python module that provides an interface, the `KeyValueDatabaseInterface()` class, for a simple Key-Value 
Database.  If such a database does not exists, it creates ones using [SQLAlchemy](https://www.sqlalchemy.org/). 
The interface has several CRUD methods so that it can interface with the database.

Some methods of the `KeyValueDatabaseInterface()` class return an object of type `KeyValue()`, which is a class used
to abstract the Key-Value entries in the database. **This can and probably will change in the future** so that the
implementation can be hidden. Instead, a dictionary or a tuple will probably be returned instead.

By default the module uses [SQLite3](https://www.sqlite.org/) as a database, but it can [support any of the ones
supported by SQLALchemy](https://docs.sqlalchemy.org/en/latest/core/engines.html).

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


## Example

The following code showcases how to use the `kv_db_interface` module. It can also be found in the `example.py` file.

```python
from kv_db_interface import KeyValueDatabaseInterface


def main():
    kv_db = KeyValueDatabaseInterface()
    # the value will be converted into bytes
    kv_db.insert("Item 1", "Value 1")
    # insert_multiple() can accept a dictionary or a list containing Tuples, Lists, and/or Ditionaries
    # Note: only the first 2 items of the sub-list or tuples will be looked at
    kv_db.insert_multiple([("Item 2", 2), ["Item 3", "Value 3"], {"Item 4" : 1234, "Item to be Deleted": "Some Value"}])

    print("Values inserted so far.")
    results = kv_db.get_all()  # Results is a List<KeyValue>

    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

    # Deleting an entry
    print("\r\n\r\nDeleting a value. Remaining values:")
    entries_to_remove = ["Item to be Deleted"]  # must be a list
    kv_db.remove(entries_to_remove)
    results = kv_db.get_all()  # Results is a List<KeyValue>

    for i in range(0, len(results)):
        print(results[i].key, int.from_bytes(results[i].value, byteorder="little"))

    # Updating an entry
    kv_db.update("Item 1", "Value 1 UPDATED")
    print("\r\nUpdated Item 1: %s" % str(kv_db.get("Item 1").value))

    # Remove remaining items:
    entries_to_remove = ["Item 1", "Item 2", "Item 3", "Item 4"]  # must be a list
    kv_db.remove(entries_to_remove)

    if len(kv_db.get_all()) == 0:
        print("All items removed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program ended by user.")

    exit(0)
```