from kv_db_interface import KeyValueDatabaseInterface
import annoucement_pb2 as announcement_message


def main():
    kv_db = KeyValueDatabaseInterface(connection_string="sqlite:///proto_buf.db")
    message_to_serialize = announcement_message.Annoucement()
    message_to_serialize.sender = "Mikey"
    message_to_serialize.recipients.extend(['Joey', 'Sammy'])
    message_to_serialize.message = "S.O.S."
    print("The following the printed Protbuf object:")
    print(message_to_serialize)

    print("This is how it showed up serialized:")
    print(message_to_serialize.SerializeToString())

    print("Inserting the message...")
    kv_db.insert("message1", message_to_serialize)
    print("Retrieving the message...")
    serialized_message_from_db = kv_db.get("message1").value
    print("This is how it looks like in after it is retrieve from the database:")
    print(serialized_message_from_db)

    print("Deserializing...")
    deserialized_object = announcement_message.Annoucement()
    deserialized_object.ParseFromString(serialized_message_from_db)
    print("Done. This is the deserialized message from the database:")
    print(deserialized_object)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program ended by user.")

    exit(0)
