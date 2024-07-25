from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import requests
import time
from decimal import Decimal, ROUND_HALF_UP

class OkexPrice:

    def __init__(self):
        self.base_url = "https://www.okx.com/v3/c2c/tradingOrders/books"
    
    def aliPrice(self, update, context):

        t = time.time() * 1000
        params = {
            't': t,
            'quoteCurrency': 'CNY',
            'baseCurrency': 'USDT',
            'side': 'sell',
            'paymentMethod': "aliPay",
            'userType': "all",
            'receivingAds': "false",
            'urlId': 6
        }

        data = self.get_api_data(self.base_url, params)
        reply_text = f'\[ 欧易(okx)支付宝实时汇率 ] \n\n'
        if data:
            array = data["data"]["sell"]
            for item in array[:10]:
                price = item["price"]
                nickName = item['nickName']
                # print(price)
                reply_text += f'{price} \t {nickName} \n'
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)
        # context.bot.send_message(group_id=update.message.group_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)

    def weixinPrice(self, update, context):
        t = time.time() * 1000
        params = {
            't': t,
            'quoteCurrency': 'CNY',
            'baseCurrency': 'USDT',
            'side': 'sell',
            'paymentMethod': "wxPay",
            'userType': "all",
            'receivingAds': "false",
            'urlId': 6
        }

        data = self.get_api_data(self.base_url, params)
        reply_text = f'\[ 欧易(okx)微信实时汇率 ] \n\n'
        if data:
            array = data["data"]["sell"]
            for item in array[:10]:
                price = item["price"]
                nickName = item['nickName']
                # print(price)
                reply_text += f'{price} \t {nickName} \n'
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)
        # context.bot.send_message(group_id=update.message.group_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)

    def get_api_data(self, base_url, params):
        try:
            # print(base_url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/'
            }

            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()  # 检查响应状态码
            data = response.json()  # 解析JSON数据
            # print(data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None


    def aliAmount(self, update, context, amount):

        t = time.time() * 1000
        params = {
            't': t,
            'quoteCurrency': 'CNY',
            'baseCurrency': 'USDT',
            'side': 'sell',
            'paymentMethod': "aliPay",
            'userType': "all",
            'receivingAds': "false",
            'urlId': 6
        }

        data = self.get_api_data(self.base_url, params)
        reply_text = f'\[ 欧易(okx)支付宝实时汇率 ] \n\n'
        total_price = 0
        if data:
            array = data["data"]["sell"]
            for item in array[:10]:
                price = item["price"]
                total_price += Decimal(price)
                print(total_price)
                nickName = item['nickName']
                reply_text += f'{price} \t {nickName} \n'
            price = round(total_price / 10, 2)
            reply_text += f'\n实时价格 (三档) :\n\n'
            result_amount = Decimal(amount) / price
            reply_text += f'{amount} / {price} = {round(result_amount, 2)}U'
            print(reply_text)
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)

    
    def weixinAmount(self, update, context, amount):
        t = time.time() * 1000
        params = {
            't': t,
            'quoteCurrency': 'CNY',
            'baseCurrency': 'USDT',
            'side': 'sell',
            'paymentMethod': "wxPay",
            'userType': "all",
            'receivingAds': "false",
            'urlId': 6
        }

        data = self.get_api_data(self.base_url, params)
        reply_text = f'\[ 欧易(okx)微信实时汇率 ] \n\n'
        total_price = 0
        print(amount)
        if data:
            array = data["data"]["sell"]
            for item in array[:10]:
                price = item["price"]
                total_price += Decimal(price)
                print(total_price)
                nickName = item['nickName']
                reply_text += f'{price} \t {nickName} \n'
            price = total_price / 10

            reply_text += f'\n实时价格 (三档) :\n\n'
            result_amount = Decimal(amount) / price
            reply_text += f'{amount} / {price} = {round(result_amount, 2)}U'
        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, parse_mode=ParseMode.MARKDOWN)
    