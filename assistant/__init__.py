# Amang Userbot
# Copyright (C) 2021-2022 amangtele
#
# This file is a part of < https://github.com/amangtele/AmangUserbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/amangtele/AmangUserbot/blob/main/LICENSE/>.

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from Amang import *
from Amang import _amang_cache
from Amang._misc import owner_and_sudos
from Amang._misc._assistant import asst_cmd, callback, in_pattern
from Amang.fns.helper import *
from Amang.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = amang_bot.full_name
OWNER_ID = amang_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException:
        return await event.edit("`Ada yang salah`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
