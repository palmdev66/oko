import asyncio

from telethon import TelegramClient, events

from config import *
from database import add_chat_id, get_all_chat_ids


async def start():
    global client
    client = TelegramClient(MAIN_ACCOUNT_SESSION_NAME, MAIN_ACCOUNT_API_ID, MAIN_ACCOUNT_API_HASH, system_version="4.16.30-vxCUSTOM")
    await client.connect()
    print("Соединились")
    dialogs = await client.get_dialogs()
    all_chat_ids = get_all_chat_ids()
    for dialog in dialogs:
        if dialog.is_user and int(dialog.id) not in all_chat_ids:
            add_chat_id(dialog.id)
            with open("chat_ids.txt", "a") as f:
                f.write(str(dialog.id) + "\n")

    print("Проверили все старые диалоги")

    @client.on(events.NewMessage(incoming=True))
    async def tracking_handler(event):
        chat_ids = get_all_chat_ids()
        if int(event.chat_id) not in chat_ids:
            add_chat_id(event.chat_id)
            with open("chat_ids.txt", "a") as f:
                f.write(str(event.chat_id) + "\n")

    await client.run_until_disconnected()


def main():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    tasks = []
    task = loop.create_task(start())
    tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
