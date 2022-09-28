# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Cilik-PyroBot 

import asyncio
import os
from pyrogram import Client, filters, raw
from pyrogram.types import Message, User
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw import functions

from datetime import datetime
from config import *
from Cilik import *
from Cilik.helpers.adminHelpers import DEVS
from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.constants import First


from Cilik.helpers.PyroHelpers import ReplyCheck
from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.command("id", [".", "-", "^", "!", "?"]) & filters.me)
async def get_id(client: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID:** `{rep.audio.file_id}`\n"
            file_id += "**File Type:** `audio`"

        elif rep.document:
            file_id = f"**File ID:** `{rep.document.file_id}`\n"
            file_id += f"**File Type:** `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`\n"
            file_id += "**File Type**: `Photo`"

        elif rep.sticker:
            file_id = f"**Sicker ID:** `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set:** `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji:** `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker:** `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker:** `False`\n"
            else:
                file_id += "**Sticker Set:** __None__\n"
                file_id += "**Sticker Emoji:** __None__"

        elif rep.video:
            file_id = f"**File ID:** `{rep.video.file_id}`\n"
            file_id += "**File Type:** `Video`"

        elif rep.animation:
            file_id = f"**File ID:** `{rep.animation.file_id}`\n"
            file_id += "**File Type:** `GIF`"

        elif rep.voice:
            file_id = f"**File ID:** `{rep.voice.file_id}`\n"
            file_id += "**File Type:** `Voice Note`"

        elif rep.video_note:
            file_id = f"**File ID:** `{rep.animation.file_id}`\n"
            file_id += "**File Type:** `Video Note`"

        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"  •  **Longitude:** `{rep.location.longitude}`\n"
            file_id += f"  •  **Latitude:** `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**Location:**\n"
            file_id += f"  •  **Longitude:** `{rep.venue.location.longitude}`\n"
            file_id += f"  •  **Latitude:** `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address:**\n"
            file_id += f"  •  **Title:** `{rep.venue.title}`\n"
            file_id += f"  •  **Detailed:** `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = f"👀 **Forwarded User ID:** `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = (
                f"🙋‍♂️ **From User ID:** `{message.reply_to_message.from_user.id}`\n"
            )
        user_detail += f"💬 **Message ID:** `{message.reply_to_message.message_id}`"
        await message.reply(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = f"👀 **Forwarded User ID:** `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = (
                f"🙋‍♂️ **From User ID:** `{message.reply_to_message.from_user.id}`\n"
            )
        user_detail += f"💬 **Message ID:** `{message.reply_to_message.message_id}`\n\n"
        user_detail += file_id
        await message.reply(user_detail)

    else:
        await message.reply(f"👥 **Chat ID:** `{message.chat.id}`")


#info user variable

WHOIS = (
    "**Info Account** 👤\n"
    "[Link Profile](tg://user?id={user_id})\n\n"
    "**🆔 ID:** `{user_id}`\n"
    "**📝 Name:** `{first_name}`\n"
    "**📌 Bio:** `{bio}`\n"
    "**🌐 Username:** `{username}`\n"
    "**👀 Last Online:** `{last_online}`\n"
    "**📊 Common Groups:** `{common_groups}`"
)

WHOIS_PIC = (
    "**Info Account** 👤\n"
    "[Link Profile](tg://user?id={user_id})\n\n"
    "**🆔 ID:** `{user_id}`\n"
    "**📝 Name:** `{first_name}`\n"
    "**📌 Bio:** `{bio}`\n"
    "**🌐 Username:** `{username}`\n"
    "**👀 Last Online:** `{last_online}`\n"
    "**📊 Common Groups:** `{common_groups}`\n"
    "**Profile Pics:** `{profile_pics}`\n\n"
    "**Last Updated:** `{profile_pic_update}`"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "Recently"
    elif user.status == "within_week":
        return "Within the last week"
    elif user.status == "within_month":
        return "Within the last month"
    elif user.status == "long_time_ago":
        return "A long time ago :("
    elif user.status == "online":
        return "Currently Online"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.last_online_date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


async def GetCommon(bot: Client, get_user):
    common = await bot.send(
        functions.messages.GetCommonChats(
            user_id=await bot.resolve_peer(get_user), max_id=0, limit=0
        )
    )
    return common


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


def ProfilePicUpdate(user_pic):
    return datetime.fromtimestamp(user_pic[0].date).strftime("%d.%m.%Y, %H:%M:%S")


@Client.on_message(filters.command(["whois", "info"], [".", "-", "^", "!", "?"]) & filters.me)
async def who_is(bot: Client, message: Message):
    cmd = message.command
    Man = await message.reply("💈 `Processing...`")
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await bot.get_users(get_user)
    except PeerIdInvalid:
        return await edit_or_reply(message, "Mon maap nih gw gk kenal ini orang.")

    user_details = await bot.get_chat(get_user)
    bio = user_details.bio
    user_pic = await bot.get_profile_photos(user.id)
    pic_count = await bot.get_profile_photos_count(user.id)
    common = await GetCommon(bot, user.id)

    if not user.photo:
        await message.edit(
            WHOIS.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                common_groups=len(common.chats),
                bio=bio if bio else "`Bio nya gk ada cok.`",
            ),
            disable_web_page_preview=True,
        )
    elif user.photo:
        await bot.send_photo(
            message.chat.id,
            user_pic[0].file_id,
            caption=WHOIS_PIC.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                profile_pics=pic_count,
                common_groups=len(common.chats),
                bio=bio if bio else "`Bio nya gk ada cok.`",
                profile_pic_update=ProfilePicUpdate(user_pic),
            ),
            reply_to_message_id=ReplyCheck(message),
        )
        await Man.delete()

add_command_help(
    "info",
    [
        [".id", "Send id of what you replied to."],
        [".whois or .info", "Untuk mencari ingfo target."],
        [".sg", "Reply to a user to find name history."],
    ],
)
