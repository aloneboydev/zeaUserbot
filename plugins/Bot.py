# Amang Userbot
# Copyright (C) 2021-2022 amangtele
#
# This file is a part of < https://github.com/amangtele/AmangUserbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/amangtele/AmangUserbot/blob/main/LICENSE/>.

from . import get_help

__doc__ = get_help("help_bot")

import os
import sys
import time
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from Amang.version import __version__ as AmangVer
from Amang.dB import DEVLIST
from . import HOSTED_ON, LOGS

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    AMANG_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    inline_pic,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    amang_cmd,
    amang_version,
    updater,
)


def AMANGPIC():
    return inline_pic() or choice(AMANG_IMAGES)


buttons = [
    [
        Button.url(get_string("bot_3"), "https://github.com/amangtele/AmangUserbot"),
        Button.url(get_string("bot_4"), "t.me/purapuranyagcsupport"),
    ]
]

# Will move to strings
alive_txt = """
◈ AmangUserbot​

  ◈ Version - {}
  ◈ Amang - {}
  ◈ Telethon - {}
"""

in_alive = "{}\n\n◈ <b>Amang Version -><b> <code>{}</code>\n◈ <bAmanga -></b> <code>{}</code>\n◈ <b>Python -></b> <code>{}</code>\n◈ <b>Waktu aktif -></b> <code>{}</code>\n◈ <b>Branch -></b> [ {} ]\n\n• <b>©↻˹ҡʏɴλɴ˼𐦝</b>"


@callback("alive")
async def alive(event):
    text = alive_txt.format(amang_version, AmangVer, __version__)
    await event.answer(text, alert=True)


@amang_cmd(
    pattern="alive( (.*)|$)",
)
async def lol(amang):
    match = amang.pattern_match.group(1).strip()
    inline = None
    if match in ["inline", "i"]:
        try:
            res = await amang.client.inline_query(asst.me.username, "alive")
            return await res[0].click(amang.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            header,
            f"{amang_version} [{HOSTED_ON}]",
            AmangVer,
            pyver(),
            uptime,
            kk,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("◈", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            f"{amang_version} [{HOSTED_ON}]",
            AmangVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("◈", a)
    if pic:
        try:
            await amang.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await amang.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await amang.reply(file=pic)
                await amang.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await amang.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        amang,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@amang_cmd(pattern="ping$", incoming=True, from_users=DEVLIST, chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@amang_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@amang_cmd(
    pattern="restart$",
    fullsudo=False,
)
async def restart(amang):
    ok = await amang.eor(get_string("bot_5"))
    call_back()
    who = "bot" if amang.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{amang.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    if len(sys.argv) > 1:
        os.execl(sys.executable, sys.executable, "main.py")
    else:
        os.execl(sys.executable, sys.executable, "-m", "Amang")


@amang_cmd(
    pattern="shutdown$",
    fullsudo=False,
)
async def shutdownbot(amang):
    await shutdown(amang)


@amang_cmd(
    pattern="logs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"amang{sys.argv[-1]}.log" if len(sys.argv) > 1 else amang.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="amang-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        await event.reply("**Amang Logs.**", file=file)
    elif opt == "open":
        with open("amang.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(amang):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        header, f"{amang_version} [{HOSTED_ON}]", AmangVer, pyver(), uptime, kk
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("◈", _e)
    builder = amang.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                if _pic := resolve_bot_file_id(pic):
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="↻ꝛɪᴢ",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await amang.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await amang.answer(result)


@amang_cmd(pattern="update( (.*)|$)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "Amang")
        # return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            AMANGPIC(),
            caption="• **Pembaruan tersedia** •",
            force_document=False,
            buttons=Button.inline("Changelog", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/Onlymeriz/Amang/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        AMANGPIC(),
        caption="• **Pembaruan tersedia** •",
        force_document=False,
        buttons=Button.inline("Changelog", data="changes"),
    )
