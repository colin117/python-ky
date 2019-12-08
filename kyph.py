import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'BOT TOKEN HERE'

"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
import urllib.parse
import time

API_TOKEN = '1028075615:AAHXFHb0ytJIocw3JTJ-s4KfKw-mW-fQ684'
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# params = url.Values{"waybill_number": {"777700032006"}, "mr": {"0.7425856138710181"}}
url = "http://www.flb56.com/api/waybill.php"

#查询订单
@dp.message_handler(commands={'cx'})
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)￿
    order_no = message.text.replace("/cx", "").strip()
    order_no= order_no.replace("8888","7777")


    resp = get_delivery_info(order_no)

    await message.reply(resp, reply=False)


# 获取物流信息`
def get_delivery_info(waybill_number):
    data = {"waybill_number": waybill_number, "mr": time.time()}
    resp = requests.post(url, data)
    msg = resp.text
    msg = msg.encode("utf-8").decode("unicode_escape")
    json_info = json.loads(msg)
    if json_info["code"] != 0:
        return json_info["msg"]
    print(json_info)
    items = json_info["data"][0]['fast7_desc']
    text = ""
    for i in range(len(items)):
        text += str("↓") + ":  " + items[i]["scantime"] + "\n" + items[i]["scantype"] + "" + items[i]["desc"] + "\n\n"
    return text


@dp.message_handler(commands={'kf'})
async def echo(message: types.Message):

    resp = "如需人工帮助请联系客服 telegram：+63 919 907 9011"

    await message.reply(resp, reply=False)


@dp.message_handler()
async def echo(message: types.Message):
    resp = "1.查询订单输入 '/cx 单号' "+"\n"+"2.客服联系方式,输入 '/kf'"

    await message.reply(resp, reply=False)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
