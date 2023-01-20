# Amang Userbot
# Copyright (C) 2021-2022 amangtele
#
# This file is a part of < https://github.com/amangtele/AmangUserbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/amangtele/AmangUserbot/blob/main/LICENSE/>.

import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

from Amang.dB import stickers
from Amang.dB.forcesub_db import get_forcesetting
from Amang.dB.gban_mute_db import is_gbanned
from Amang.dB.greetings_db import get_goodbye, get_welcome, must_thank
from Amang.dB.nsfw_db import is_profan
from Amang.fns.helper import inline_mention
from Amang.fns.tools import async_searcher, create_tl_btn, get_chatbot_reply

try:
    from ProfanityDetector import detector
except ImportError:
    detector = None
from . import LOG_CHANNEL, LOGS, asst, amang_bot, get_string, types, udB
from ._inline import something


@amang_bot.on(events.ChatAction())
async def Function(event):
    try:
        await DummyHandler(event)
    except Exception as er:
        LOGS.exception(er)


async def DummyHandler(amang):
    # clean chat actions
    key = udB.get_key("CLEANCHAT") or []
    if amang.chat_id in key:
        try:
            await amang.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(amang.chat_id):
        chat_count = (await amang.client.get_participantsamanga.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await amang.respond(file=sticker)
    # force subscribe
    if (
        udB.get_key("FORCESUB")
        and ((amang.user_joined oramanga.user_added))
        and get_forcesetting(amang.chat_id)
    ):
        user = await amang.get_user()
        if not user.bot:
            joinchat = get_forcesetting(amang.chat_id)
            try:
                await amang_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await amang_bot.edit_permissions(
                    amang.chat_id, user.id, send_messages=False
                )
                res = await amang_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(amang.chat_id, reply_toamanga.action_message.id)

    if amang.user_joined or amang.added_by:
        user = await amang.get_user()
        chat = await amang.get_chat()
        # gbans and @Amang checks
        if udB.get_key("amang_BANS"):
            try:
                is_banned = await async_searcher(
                    "https://bans.amang/api/status",
                    json={"userId": user.id},
                    post=True,
                    re_json=True,
                )
                if is_banned["is_banned"]:
                    await amang.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    await amang.client.send_message(
                        chat.id,
                        f'**@AmangBans:** Banned user detected and banned!\n`{str(is_banned)}`.\nBan reason: {is_banned["reason"]}',
                    )

            except BaseException:
                pass
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await amang.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await amang.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        # greetings
        elif get_welcome(amang.chat_id):
            user = await amang.get_user()
            chat = await amang.get_chat()
            title = chat.title or "this chat"
            count = (
                chat.participants_count
                or (await amang.client.get_participants(chat, limit=0)).total
            )
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(amang.chat_id)
            msgg = wel["welcome"]
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(amang, msg, med, btn)
            elif msg:
                send = await amang.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await amang.reply(file=med)
    elif (amang.user_left oramanga.user_kicked) and get_goodbyamangra.chat_id):
        user = await amang.get_user()
        chat = await amang.get_chat()
        title = chat.title or "this chat"
        count = (
            chat.participants_count
            or (await amang.client.get_participants(chat, limit=0)).total
        )
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(amang.chat_id)
        msgg = wel["goodbye"]
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(amang, msg, med, btn)
        elif msg:
            send = await amang.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await amang.reply(file=med)


@amang_bot.on(events.NewMessage(incoming=True))
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User):
        return
    key = udB.get_key("CHATBOT_USERS") or {}
    if e.text and key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            sleep = udB.get_key("CHATBOT_SLEEP") or 1.5
            await asyncio.sleep(sleep)
            await e.reply(msg)
    chat = await e.get_chat()
    if e.is_group and not sender.bot:
        if sender.username:
            await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and not sender.bot:
        if chat.username:
            await uname_stuff(e.sender_id, chat.username, chat.first_name)
    if detector and is_profan(e.chat_id) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()


@amang_bot.on(events.Raw(types.UpdateUserName))
async def uname_change(e):
    await uname_stuff(e.user_id, e.username, e.first_name)


async def uname_stuff(id, uname, name):
    if udB.get_key("USERNAME_LOG") :
        old_ = udB.get_key("USERNAME_DB") or {}
        old = old_.get(id)
        # Ignore Name Logs
        if old and old == uname:
            return
        if old and uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_2").format(old, uname),
            )
        elif old:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_3").format(f"[{name}](tg://user?id={id})", old),
            )
        elif uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_4").format(f"[{name}](tg://user?id={id})", uname),
            )

        old_[id] = uname
        udB.set_key("USERNAME_DB", old_)
