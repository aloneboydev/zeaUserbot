from .. import run_as_module

if not run_as_module:
    from ..exceptions import RunningAsFunctionLibError

    raise RunningAsFunctionLibError(
        "You are running 'Amang' as a functions lib, not as run module. You can't access this folder.."
    )

from .. import *

CMD_HANDLER = os.environ.get("CMD_HANDLER") or "."

DEVLIST = [
    719195224,  # @xditya
    1322549723,  # @danish_00
    1903729401,  # @its_buddhhu
    1054295664,  # @riizzvbss
    1924219811, # @Banned_3
    883761960,  # @SilenceSpe4ks
    910766621, # @thisrama
    1803618640, # @onlymeriz
    874946835,  # @vckyaz
    997461844, # @AyiinXd
    1784606556,  # @greyvbss
    844432220,  # @mrismanaziz
    2059198079, # @thekingofkazu
    951454060, # @riizzvbss
    993270486, # @deakajalah
    2003295492, #
    1191668125, # Rendy
    1488093812, # @ControlErrors
    2073506739, # @amwang
    966484443,  # @bukankenjan
    
]

cmd = CMD_HANDLER
CMD_LIST = {}

DEFAULT = [
    5063062493, # @disinikazu


AMANG_IMAGES = [
    f"https://graph.org/file/{_}.jpg"
    for _ in [
        "4fe47bc238c18b11f8258",
        "4fe47bc238c18b11f8258",
    ]
]

stickers = [

]
