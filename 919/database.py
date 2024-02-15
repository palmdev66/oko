import sqlite3


def get_connections():
    with sqlite3.connect("database") as connection:
        cursor = connection.cursor()
        return connection, cursor


def create_database():
    conn, cursor = get_connections()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS ChatIds(
            chat_id BIGINT);"""
    )


def get_all_chat_ids():
    connection, cursor = get_connections()
    cursor.execute("SELECT chat_id FROM ChatIds")
    chat_ids = set(row[0] for row in cursor.fetchall())
    connection.close()
    return chat_ids


def add_chat_id(chat_id):
    connection, cursor = get_connections()
    cursor.execute("INSERT INTO ChatIds (chat_id) VALUES (?)", (chat_id,))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
