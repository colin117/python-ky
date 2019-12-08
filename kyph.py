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


# @dp.message_handler(regexp='(^cat[s]?$|puss)')
# async def cats(message: types.Message):
#     with open('data/cats.jpg', 'rb') as photo:
#         '''
#         # Old fashioned way:
#         await bot.send_photo(
#             message.chat.id,
#             photo,
#             caption='Cats are here 😺',
#             reply_to_message_id=message.message_id,
#         )
#         '''
#
#         await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands={'cx'})
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)￿
    print(message)

    order_no = message.text.replace("/cx", "").strip()
    order_no= order_no.replace("8888","7777")

    print(order_no)
    resp = get_delivery_info(order_no)
    print(resp)
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
