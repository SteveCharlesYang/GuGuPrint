import base64
import time
import logging
from msgtpl import *
from api import *
from telegram.ext import ConversationHandler
import lang

logger = logging.getLogger(__name__)


def guguprtxt(pruser, prtext, forward=False):
    tstamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outdata = outtpl.replace("%FROM_USER%", pruser)
    outdata = outdata.replace("%FROM_TIME%", tstamp)
    outdata = outdata.replace("%CONTENT%", prtext)
    if forward:
        outdata = outdata.replace("%TEXT%", 'FORWARD')
    else:
        outdata = outdata.replace("%TEXT%", '-TEXT-')
    outdata = outdata.replace(u'\xa0 ', u' ')
    outdata = base64.b64encode(outdata.encode(encoding='gbk', errors='ignore')).decode()
    gu_req(pruser, tstamp, 'T:' + outdata)


def prtxt(bot, update):
    user = update.message.from_user
    logger.info(user.username + ":[Text]")
    pr_usrname = user.username
    if update.message.forward_from is not None:
        pr_usrname = pr_usrname + "\nFORWARD: @" + update.message.forward_from.username
    guguprtxt(pr_usrname, update.message.text)
    update.message.reply_text(lang.print_success)
    return ConversationHandler.END
