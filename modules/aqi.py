import time
import base64
from telegram.ext import ConversationHandler
import logging
from api import *

logger = logging.getLogger(__name__)

aqi_city = 'chengdu'


def praqi(bot, update):
    user = update.message.from_user
    logger.info(user.username + ":[aqi]")
    tstamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    aqitpl = ' <-----BEGIN TRANSMISSION----->\n' \
             'FROM: @%FROM_USER%\n' \
             'TIME: %FROM_TIME%\n' \
             '     ---------AQI---------\n' \
             'TIME£º%time%\n' \
             'CITY£º%city%  AQI£º%aqi%\n' \
             'LVL£º%level%\n' \
             'PM25£º%pm25%   PM10£º%pm10%\n' \
             '  <-----END TRANSMISSION----->'
    level = ''
    r1j = dict()
    r1 = requests.get("https://api.waqi.info/feed/" + aqi_city + "/?token=--key--")
    r1j = r1.json()
    if r1j['data']['aqi'] >= 300:
        level = 'Hazardous'
    else:
        if r1j['data']['aqi'] >= 200:
            level = 'Very Unhealthy'
        else:
            if r1j['data']['aqi'] >= 150:
                level = 'Unhealthy'
            else:
                if r1j['data']['aqi'] >= 100:
                    level = 'Unhealthy for Sensitive Groups'
                else:
                    if r1j['data']['aqi'] >= 50:
                        level = 'Moderate'
                    else:
                        level = 'Good'
    aqitpl = aqitpl.replace('%city%', aqi_city)
    aqitpl = aqitpl.replace("%FROM_USER%", user.username)
    aqitpl = aqitpl.replace("%FROM_TIME%", tstamp)
    aqitpl = aqitpl.replace('%level%', level)
    aqitpl = aqitpl.replace('%pm25%', str(r1j['data']['iaqi']['pm25']['v']))
    aqitpl = aqitpl.replace('%pm10%', str(r1j['data']['iaqi']['pm10']['v']))
    aqitpl = aqitpl.replace('%aqi%', str(r1j['data']['aqi']))
    aqitpl = aqitpl.replace('%time%', str(r1j['data']['time']['s']))
    outdata = base64.b64encode(aqitpl.encode(encoding='gbk')).decode()
    gu_req('Test', tstamp, 'T:' + outdata)
    update.message.reply_text('Done!')
    return ConversationHandler.END

