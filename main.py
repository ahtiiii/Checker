import os
import asyncio
from pyrogram import Client, compose, filters, enums
import re
from pathlib import Path
from defs import getcards
from plugins.func.users_sql import *

# Define the path to your session file
session_file_path = "scrapper.session"  # Replace with your actual session file name if different

plugins = dict(root="plugins")

async def main():
    # Check if the session file exists and delete it
    if os.path.exists(session_file_path):
        os.remove(session_file_path)
        print(f"Deleted existing session file: {session_file_path}")

    user = Client("scrapper",
                  api_id="27649783",
                  api_hash="834fd6015b50b781e0f8a41876ca95c8")
    bot = Client("my_bot",
                 api_id="27649783",
                 api_hash="834fd6015b50b781e0f8a41876ca95c8",
                 bot_token="7434458946:AAGNmwZDk94caicG1d-SDqWWQYUP8UcOtaI",
                 plugins=plugins)
    clients = [user, bot]
    bot.set_parse_mode(enums.ParseMode.HTML)

    @bot.on_message(filters.command('adm_test'))
    async def cmd_help(client, message):
        await message.reply_text("i am working", message.id)

    @bot.on_message(filters.command('scr'))
    async def cmd_scr(client, message):
        msg = message.text[len('/scr '):]
        splitter = msg.split(' ')
        if len(msg) == 0:
            resp = f"""
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username 50</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz 50</code>
            """
            await message.reply_text(resp, message.id)
        else:
            #
            user_id = str(message.from_user.id)
            chat_type = str(message.chat.type)
            chat_id = str(message.chat.id)
            # PLAN CHECK

            regdata = fetchinfo(user_id)
            results = str(regdata)
            if results == 'None':
                resp = "𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 𝗬𝗘𝗧 ⚠️. 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥 𝗙𝗜𝗥𝗦𝗧 𝗕𝗬 𝗨𝗦𝗜𝗡𝗚 /register 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘."
                await message.reply_text(resp, message.id)
            else:
                # HERE
                # PM AND AUTH CHECK
                pm = fetchinfo(user_id)
                status = pm[2]
                role = status
                GROUP = open("plugins/group.txt").read().splitlines()
                if chat_type == "ChatType.PRIVATE" and status == "FREE":
                    resp = "𝗢𝗡𝗟𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗔𝗥𝗘 𝗔𝗟𝗟𝗢𝗪𝗘𝗗 𝗧𝗢 𝗨𝗦𝗘 𝗕𝗢𝗧 𝗜𝗡 𝗣𝗘𝗥𝗦𝗢𝗡𝗔𝗟 ⚠️.𝗬𝗢𝗨 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗙𝗥𝗘𝗘𝗟𝗬 𝗕𝗢𝗧 𝗛𝗘𝗥𝗘 @cyberpirateschats"
                    await message.reply_text(resp, message.id)
                else:
                    url = splitter[0]
                    print(url)
                    if splitter[1].isdigit():
                        limit = int(splitter[1])
                    else:
                        limit = 0
                    if limit <= 0:
                        resp = "𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌"
                        await message.reply_text(resp, message.id)
                    else:
                        chat = url
                        try:
                            await getcards(client, chat, limit, message)
                        except Exception as e:
                            e = str(e)
                            first_error = "Error : local variable 'file_name' referenced before assignment"
                            sec_error = 'Telegram says: [400 USERNAME_NOT_OCCUPIED] - The username is not occupied by anyone (caused by "contacts.ResolveUsername")'
                            third_error = "local variable 'file_name' referenced before assignment"
                            fourth_error = 'Telegram says: [400 USERNAME_INVALID] - The username is invalid (caused by "contacts.ResolveUsername")'
                            if e == first_error:
                                resp = "No CC Found"
                                await bot.delete_messages(message.chat.id, delete.id)
                                await message.reply_text(text=resp,
                                                         reply_to_message_id=message.id)
                            elif e == sec_error:
                                resp = "𝗪𝗿𝗼𝗻𝗴 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 ❌"
                                await bot.delete_messages(message.chat.id, delete.id)
                                await message.reply_text(text=resp,
                                                         reply_to_message_id=message.id)
                            elif e == third_error:
                                resp = "𝗡𝗼 𝗖𝗖 𝗙𝗼𝘂𝗻𝗱 ❌"
                                await bot.delete_messages(message.chat.id, delete.id)
                                await message.reply_text(text=resp,
                                                         reply_to_message_id=message.id)
                            elif e == fourth_error:
                                resp = "𝗪𝗿𝗼𝗻𝗴 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 ❌"
                                await bot.delete_messages(message.chat.id, delete.id)
                                await message.reply_text(text=resp,
                                                         reply_to_message_id=message.id)
                            else:
                                await bot.delete_messages(message.chat.id, delete.id)
                                await message.reply_text(text=e,
                                                         reply_to_message_id=message.id)

    print("Done Bot Active ✅")

    await compose(clients)

asyncio.run(main())
