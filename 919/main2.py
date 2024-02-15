from time import sleep

from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import BlockRequest

from config import *


def delete_user(client, chat_id):
    chat_id = int(str(chat_id).strip())
    print("Удаляем ", chat_id)
    try:
        client.get_dialogs()
    except Exception as e:
        print("[WARNING] Не смогли получить диалоги")
    try:
        client(BlockRequest(chat_id))
    except Exception as e:
        print("[WARNING] Возможно не получилось заблокировать")
    try:
        client.delete_dialog(chat_id, revoke=True)
    except Exception as e:
        print("[WARNING] Возможно не удалили диалог")
    print("Удалили ", chat_id)


def check_blockers():
    lines = []
    chat_id = None
    try:
        with open("chats_to_block.txt", "r+", encoding="utf-8") as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()

        if not lines:
            return
        client = TelegramClient(MAIN_ACCOUNT_SESSION_NAME_2, MAIN_ACCOUNT_API_ID, MAIN_ACCOUNT_API_HASH)
        client.connect()
        try:
            while lines:
                chat_id = lines.pop()
                delete_user(client, chat_id)
        except Exception as e:
            print(f"[ERROR_2] {e}")
        finally:
            client.disconnect()
    except Exception as e:
        print(f"[ERROR] {e}")
        if chat_id is not None:
            lines += [chat_id]
        with open("chats_to_block.txt", "a") as file:
            for line in lines:
                file.write(line.strip() + "\n")


while True:
    check_blockers()
    sleep(5)
