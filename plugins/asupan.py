# Amang Userbot
# Copyright (C) 2021-2022 amangtele
#
# This file is a part of < https://github.com/amangtele/AmangUserbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/amangtele/AmangUserbot/blob/main/LICENSE/>.


"""
◈ Perintah Tersedia
• asupan
•  Asupan video TikTok",
• ayang "Mencari Foto ayang kamu /nNote: Modul ini buat cwo yang jomblo."
•ppcp "Mencari Foto PP Couple Random."
•bokep "to send random porno videos."
•ppanime "Mencari Foto PP Couple Anime."
"""


from secrets import choice

from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterVoice
import asyncio
from asyncio import gather
from random import choice
from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from pyrogram import Client as amang


@amang_cmd(pattern="asupan$")
async def _(event):
    xx = await edit_or_reply(event, "`Tunggu Sebentar...`")
    try:
        asupannya = [
            asupan
            async for asupan in event.client.iter_messages(
                "@tedeasupancache", filter=InputMessagesFilterVideo
            )
        ]
        await event.client.send_file(
            event.chat_id, file=choice(asupannya), reply_to=event.reply_to_msg_id
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan video asupan.**")


@amang_cmd(pattern="desahcewe$")
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    xx = await edit_or_reply(event, "`Tunggu Sebentar...`")
    try:
        desahcewe = [
            desah
            async for desah in event.client.iter_messages(
                "@desahancewesangesange", filter=InputMessagesFilterVoice
            )
        ]
        await event.client.send_file(
            event.chat_id, file=choice(desahcewe), reply_to=event.reply_to_msg_id
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan desahan cewe.**")


@amang_cmd(pattern="desahcowo$")
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    xx = await edit_or_reply(event, "`Tunggu Sebentar...`")
    try:
        desahcowo = [
            desah
            async for desah in event.client.iter_messages(
                "@desahancowokkkk", filter=InputMessagesFilterVoice
            )
        ]
        await event.client.send_file(
            event.chat_id, file=choice(desahcowo), reply_to=event.reply_to_msg_id
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan desahan cowo.**")


CMD_HELP.update(
    {
        "asupan": f"**Plugin : **`asupan`\
        \n\n  »  **Perintah :** `{cmd}asupan`\
        \n  »  **Kegunaan : **Untuk Mengirim video asupan secara random.\
        \n\n  »  **Perintah :** `{cmd}desahcowo`\
        \n  »  **Kegunaan : **Untuk Mengirim voice desah cowo secara random.\
        \n\n  »  **Perintah :** `{cmd}desahcewe`\
        \n  »  **Kegunaan : **Untuk Mengirim voice desah cewe secara random.\
    "
    }
)
