# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Cilik-PyroBot 

import os

import asyncio
import random
from asyncio import sleep
from datetime import datetime

from pyrogram import Client, filters, raw
from pyrogram.types import Message

from Cilik import *
from Cilik.helpers.basic import edit_or_reply
from Cilik.utils import s_paste

from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.command("limit", [".", "-", "^", "!", "?"]) & filters.me)
async def spamban(client: Client, m: Message):
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    wait_msg = await m.reply("💈 `Processing...`")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await wait_msg.edit_text(f"-⋟ {status.text}")
    
    
@Client.on_message(filters.me & filters.command(["q", "quotly"], [".", "-", "^", "!", "?"]))
async def quotly(bot: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("`Reply to any users`")
    Cilik = await message.reply("```Making a Quote```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            await sleep(4)
            msg = await bot.get_history("@QuotLyBot", 1)
            is_sticker = True
        except:
            await sleep(1)
            progress += random.randint(0, 5)
            if progress > 100:
                await Cilik.edit("There was a long running error")
                return
            try:
                await Cilik.edit("```Making a Quote\nProcessing {}%```".format(progress))
            except:
                await Cilik.edit("ERROR")

    if msg_id := msg[0]["message_id"]:
        await asyncio.gather(
            Cilik.delete(),
            bot.copy_message(message.chat.id, "@QuotLyBot", msg_id),
        )


@Client.on_message(filters.command("stats", [".", "-", "^", "!", "?"]) & filters.me)
async def stats(client: Client, message: Message):
    yanto = await message.reply_text("📊 `Collecting stats`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh=await client.get_me()
    group = ["supergroup", "group"]
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == "private":
            u += 1
        elif dialog.chat.type == "bot":
            b += 1
        elif dialog.chat.type == "group":
            g += 1
        elif dialog.chat.type == "supergroup":
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == "channel":
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await yanto.edit_text(
        """📊 **Stats Me**
**Private Chats :** `{}`
**Groups:** `{}`
**Super Groups:** `{}`
**Channels:** `{}`
**Admins:** `{}`
**Bots:** `{}`
**⏱ It Took:** `{}`""".format(
            u, g, sg, c, a_chat, b, ms
        )
    )



add_command_help(
    "misc",
    [
        [
            ".q or .quote",
            "To Make a Quote",
        ],
        [".limit", "Check Limit telegram from @SpamBot."],
        [".stats", "To Check Your Account Status, how Joined Chats."],
        [".tgm", "Reply to Media as args to upload it to telegraph."],
        [".clone", "To Clone someone Profile."],
        [".revert", "To Get Your Account Back."],
        [".carbon", "Carbonised Text."],
    ],
)
