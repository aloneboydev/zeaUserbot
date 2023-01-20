# Amang Userbot
# Copyright (C) 2021-2022 amangtele
#
# This file is a part of < https://github.com/amangtele/AmangUserbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/amangtele/AmangUserbot/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}setname <first name // last name>`
    Ubah nama profil Anda.

• `{i}setbio <bio>`
    Ubah bio profil Anda.

• `{i}setfp <reply to pic>`
    Ubah foto profil Anda.

• `{i}delfp <n>(optional)`
    Hapus satu foto profil, jika tidak ada nilai yang diberikan, hapus n jumlah foto.

• `{i}poto <username>`
    Unggah foto Obrolan/Pengguna jika Tersedia.
"""
import os

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest

from . import eod, eor, get_string, mediainfo, amang_cmd

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

# bio changer


@amang_cmd(pattern="setbio( (.*)|$)", fullsudo=True)
async def _(amang):
    ok = await amang.eor("...")
    set = amang.pattern_match.group(1).strip()
    try:
        await amang.client(UpdateProfileRequest(about=set))
        await eod(ok, f"Bio profil diubah menjadi\n`{set}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# name changer


@amang_cmd(pattern="setname ?((.|//)*)", fullsudo=True)
async def _(amang):
    ok = await amang.eor("...")
    names = amang.pattern_match.group(1).strip()
    first_name = names
    last_name = ""
    if "//" in names:
        first_name, last_name = names.split("//", 1)
    try:
        await amang.client(
            UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
            ),
        )
        await eod(ok, f"Nama diubah menjadi `{names}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# profile pic


@amang_cmd(pattern="setfp$", fullsudo=True)
async def _(amang):
    if not amang.is_reply:
        return await amang.eor("`Balas ke Media..`", time=5)
    reply_message = await amang.get_reply_message()
    ok = await amang.eor(get_string("com_1"))
    replfile = await reply_message.download_media()
    file = await amang.client.upload_file(replfile)
    try:
        if "pic" in mediainfo(reply_message.media):
            await amang.client(UploadProfilePhotoRequest(file))
        else:
            await amang.client(UploadProfilePhotoRequest(video=file))
        await eod(ok, "`Foto Profil Berhasil Diubah !`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")
    os.remove(replfile)


# delete profile pic(s)


@amang_cmd(pattern="delfp( (.*)|$)", fullsudo=True)
async def remove_profilepic(delpfp):
    ok = await eor(delpfp, "`...`")
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client.get_profile_photos("me", limit=lim)
    await delpfp.client(DeletePhotosRequest(pfplist))
    await eod(ok, f"`Berhasil dihapus {len(pfplist)} gambar profil(s).`")


@amang_cmd(pattern="poto( (.*)|$)")
async def gpoto(e):
    amang = e.pattern_match.group(1).strip()
    a = await e.eor(get_string("com_1"))
    just_dl = amang in ["-dl", "--dl"]
    if just_dl:
        amang = None
    if not amang:
        if e.is_reply:
            gs = await e.get_reply_message()
            amang = gs.sender_id
        else:
            amang = e.chat_id
    okla = await e.client.download_profile_photo(amang)
    if not okla:
        return await eor(a, "`Foto Profil Tidak Ditemukan...`")
    if not just_dl:
        await a.delete()
        await e.reply(file=okla)
        return os.remove(okla)
    await a.edit(f"Mengunduh pfp ke [ `{okla}` ].")
