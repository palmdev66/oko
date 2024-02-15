import asyncio

from config import *

from telethon import TelegramClient, events


active_chat_ids = [None] * len(ACCOUNTS)


def convert():
    global active_chat_ids
    for chat_id in active_chat_ids:
        if chat_id is not None:
            with open("chat_ids.txt", "a") as f:
                f.write(str(chat_id) + "\n")


def get_next_chat_id(number):
    global active_chat_ids
    with open("chat_ids.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            active_chat_ids[number] = None
            return
        chat_id_to_return = lines[0].strip()
        active_chat_ids[number] = chat_id_to_return
        del lines[0]

    with open("chat_ids.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    return chat_id_to_return


def delete_user(chat_id):
    print("Добавили на удаление ", chat_id)
    with open("chats_to_block.txt", "a") as f:
        f.write(str(chat_id) + "\n")


async def parse_message(text):
    text_lines = text.split("\n")
    phone = None
    email = None
    chat_id = None
    for line in text_lines:
        if "**ID:**" in line:
            chat_id = line.split()[-1].replace("`", "").strip()
        if "**Телефон(ы):**" in line:
            phone = line.split()[-1].replace("`", "").strip()
        if "**Почта(ы):**" in line:
            email = line.split()[-1].replace("`", "").strip()

    if not phone and not email:
        delete_user(chat_id)
    if phone and not (phone.startswith("7") or phone.startswith("375")):
        delete_user(chat_id)


async def add_account(account):
    client_number = account[-1]
    client = TelegramClient(account[0], account[1], account[2], system_version="4.16.30-vxCUSTOM")
    await client.connect()

    print(f"gb{client_number+1} соединился")

    while True:
        new_chat = get_next_chat_id(client_number)
        if new_chat:
            print(f"gb{client_number + 1} получил chat_id={new_chat} и пытается отправить")
            await client.send_message(GB_USERNAME, f"#{new_chat}")
            print(f"gb{client_number + 1} отправил chat_id={new_chat}")
            break
        await asyncio.sleep(3)

    @client.on(events.NewMessage(incoming=True))
    async def tracking_handler(event):
        if event.chat_id != GB_CHAT_ID:
            return

        if "**Выберите направление поиска**" in event.message.text:
            await event.message.click(0)
            return

        if "**ID:**" in event.message.text:
            await parse_message(event.message.text)
            while True:
                n_chat = get_next_chat_id(client_number)
                if n_chat:
                    print(f"gb{client_number+1} получил chat_id={n_chat} и пытается отправить")
                    await client.send_message(GB_USERNAME, f"#{n_chat}")
                    print(f"gb{client_number+1} отправил chat_id={n_chat}")
                    break
                await asyncio.sleep(3)
            return

        if "Технические работы" in event.message.text:
            global active_chat_ids
            n_chat = active_chat_ids[client_number]
            await client.send_message(GB_USERNAME, f"#{n_chat}")
            return

    await client.run_until_disconnected()


def main():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()

    tasks = []
    for i, account in enumerate(ACCOUNTS):
        account += [i]
        task = loop.create_task(add_account(account))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    try:
        main()
    except:
        convert()
