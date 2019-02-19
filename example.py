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
