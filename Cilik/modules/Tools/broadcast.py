# Cilik-PyroBot

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from requests import get

from Cilik.helpers.adminHelpers import DEVS

from Cilik.modules.Ubot.help import add_command_help

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/grey423/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001473548283, -1001390552926, -1001687155877]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST

@Client.on_message(
    filters.group & filters.command("cgcast", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command("gcast", [".", "-", "^", "!"]) & filters.me)
async def ucup_gcast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.reply_text("`Global Broadcasting!`")
        sent = 0
        failed = 0
        async for dialog in client.iter_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "supergroup",
                "group",
            ]:
                chat = dialog.chat.id
                if chat not in GCAST_BLACKLIST:
                    try:
                        await msg.copy(chat)
                        sent = sent + 1
                        await asyncio.sleep(0.1)
                    except:
                        failed = failed + 1
                        await asyncio.sleep(0.1)

        return await yanto.edit_text(
            f"Done in {sent} chats, error in {failed} chat(s)"
        )
        return 
    if len(message.command) < 2:
        await message.reply_text(
             "**usage**:\n.gcast <text> or reply to message"
        )
        return
    yanto = await message.reply_text("`Global Broadcasting!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "supergroup",
             "group",
        ]:
             chat = dialog.chat.id
             if chat not in GCAST_BLACKLIST:
                 try:
                     await client.send_message(chat, text=panjul)
                     sent = sent + 1
                     await asyncio.sleep(0.1)
                 except:
                     failed = failed + 1
                     await asyncio.sleep(0.1)
                                       
    return await yanto.edit_text(
        f"Done in {sent} chats, error in {failed} chat(s)"
    )


@Client.on_message(filters.command("gucast", [".", "-", "^", "!", "?"]) & filters.me)
async def jamal_gucast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.reply_text("`Global Broadcasting to users!`")
        sent = 0
        failed = 0
        async for dialog in client.iter_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "private",
            ]:
                chat = dialog.chat.id
                if chat not in GCAST_BLACKLIST:
                    try:
                        await msg.copy(chat)
                        sent = sent + 1
                        await asyncio.sleep(0.1)
                    except:
                        failed = failed + 1
                        await asyncio.sleep(0.1)

                await yanto.edit_text(
                    f"✅ **Gucast Successfully\nSend to:** {sent} **Chats\n Failed to send :** {failed} **Chats**"
                )
        return 
    if len(message.command) < 2:
        await message.reply_text(
             "**usage**:\n.gucast <text> or reply to message"
        )
        return
    yanto = await message.reply_text("`Global Broadcasting to users!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "private",
        ]:
             chat = dialog.chat.id
             if chat not in GCAST_BLACKLIST:
                 try:
                     await client.send_message(chat, text=panjul)
                     sent = sent + 1
                     await asyncio.sleep(0.1)
                 except:
                     failed = failed + 1
                     await asyncio.sleep(0.1)
                                        
                 await yanto.edit_text(
                     f"**✅ Gucast Successfully\nSend to:** {sent} **Chats\n Failed to send :** {failed} **Chats**"
                 )

add_command_help(
    "gcast",
    [
        [
            ".gcast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk.",
        ],
        [
            ".gucast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk.",
        ],
    ],
)
