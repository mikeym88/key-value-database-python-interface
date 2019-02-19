from kv_db_interface import KeyValueDatabaseInterface
import annoucement_pb2 as announcement_message


def main():
    kv_db = KeyValueDatabaseInterface(connection_string="sqlite:///proto_buf.db")
    announcement = announcement_message.Annoucement()
    announcement.sender = "Mikey"
    announcement.recipients.extend(['Joey', 'Sammy'])
    announcement.message = "S.O.S."
    kv_db.insert("message1", announcement.SerializeToString())
    print("Key-Value Inserted: { '%s' : '%s' }" % (kv_db.get("message1").key, kv_db.get("message1").value))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program ended by user.")

    exit(0)
