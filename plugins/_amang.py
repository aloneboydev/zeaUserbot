# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, ayra_cmd, eor, get_string

REPOMSG = """
◈ **Amang ꭙ ᴜꜱᴇʀʙᴏᴛ​** ◈\n
◈ Repo - [Click Here](https://github.com/amangtele/AmangUserbot)
◈ Addons - [Click Here](https://github.com/amangtele/addons)
◈ Support - @amangsupportgrup
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/amangtele/AmangUserbot"),
        Button.url("Addons", "https://github.com/amangtele/addons"),
    ],
    [Button.url("Support Group", "t.me/amangsupportgrup")],
]

AYSTRING = """🎇 **Thanks for Deploying ᴀʏʀᴀ ꭙ ᴜꜱᴇʀʙᴏᴛ!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@amang_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@amang_cmd(pattern="amang$")
async def useAyra(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        AYSTRING,
        file="https://graph.org/file/a51b51ca8a7cc5327fd42.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")