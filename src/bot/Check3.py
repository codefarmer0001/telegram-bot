from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import pytz
from dao.Bills import Bills
from dao.Setting import Setting

class Check3:

    def check3(self, update, context):
        # 获取当前日期和时间
        now = datetime.now()

        # 构造当天凌晨4点的时间
        midnight = datetime(now.year, now.month, now.day, 4, 0, 0)

        # 如果当前时间在凌晨4点之前，日期需要减去一天
        # if now.hour < 4:
        midnight = midnight - timedelta(days=3)

        chat_id = update.message.chat.id

        # print(midnight)

        setting = Setting()
        setData = setting.get_setting_by_group_id(chat_id)
        self.exchange_rate = 1
        self.fee = 0
        self.show_unit = '0'
        self.show_exchange_rate = 0
        print('setData')
        if setData:
            self.exchange_rate = setData[0][3]
            # print(self.exchange_rate)
            self.fee = setData[0][4]
            self.show_unit = setData[0][2]
            self.show_exchange_rate = setData[0][3]
        
        billDao = Bills()
        in_total = billDao.query_in_or_out_total(midnight, chat_id, 1)
        out_total = billDao.query_in_or_out_total(midnight, chat_id, 2)

        in_top5_data = billDao.query_in_or_out_top5_data(midnight, chat_id, 1)
        out_top5_data = billDao.query_in_or_out_top5_data(midnight, chat_id, 2)

        
        reply_text = f"入款（{in_total}笔）：\n"
        show_unit = self.show_unit
        # print(f'显示或者隐藏u：{in_top5_data}')
        # print(f'显示或者隐藏u：{out_top5_data}')
        
        if in_top5_data:
            for item in reversed(in_top5_data):
                # 将字符串转换为 datetime 对象
                datetime_object = datetime.strptime(item[5], "%Y-%m-%d %H:%M:%S")

                # 使用 strftime 方法将日期时间对象格式化为时分秒的字符串
                formatted_time = datetime_object.strftime("%H:%M:%S")
                if item[8] == 1:
                    if show_unit == '1':
                        u_amount = int(item[4]) / float(item[7])
                        u_amount = self.format_float(u_amount)
                        amount = f'{int(item[4])} \t / \t {float(item[7])} = {u_amount}u'
                    else:
                        amount = int(item[4])
                else:
                    if show_unit == '1':
                        u_amount = int(item[4]) / float(item[7])
                        u_amount = self.format_float(u_amount)
                        amount = f'-{int(item[4])} \t / \t {float(item[7])} = {u_amount}u'
                    else:
                        amount = int(item[4])
                        amount = f"-{amount}"
                # print(f'显示或者隐藏u：{show_unit}')
                
                reply_text += f"{formatted_time}  {amount} \n"
                print(reply_text)

        reply_text += f"\n"
        # print(reply_text)

        reply_text += f"下发（{out_total}笔）：\n"

        # print(reply_text)


        if out_top5_data:
            for item in reversed(out_top5_data):
                # 将字符串转换为 datetime 对象
                datetime_object = datetime.strptime(item[5], "%Y-%m-%d %H:%M:%S")

                # 使用 strftime 方法将日期时间对象格式化为时分秒的字符串
                formatted_time = datetime_object.strftime("%H:%M:%S")
                if item[8] == 1:
                    if show_unit == '1':
                        u_amount = int(item[4]) / float(item[7])
                        u_amount = self.format_float(u_amount)
                        amount = f'{self.format_float(item[4])} \t ({u_amount}u)'
                    else:
                        amount = int(item[4])
                else:
                    if show_unit == '1':
                        u_amount = int(item[4]) / float(item[7])
                        u_amount = self.format_float(u_amount)
                        amount = f'-{self.format_float(item[4])} \t ({u_amount}u)'
                    else:
                        amount = int(item[4])
                        amount = f"-{amount}"
                reply_text += f"{formatted_time}  {amount} \n"

        total_in_amount = billDao.query_total_amount(midnight, chat_id, 1)
        plus_total = 0
        # negative_total = 0
        should_be_spent = 0
        if total_in_amount:
            for item in reversed(total_in_amount):
                if item[2] == 1:
                    plus_total += item[0]
                    should_be_spent += item[1]
                if item[2] == 2:
                    plus_total -= item[0]
                    should_be_spent -= item[1]

        total_in_amount = billDao.query_total_amount(midnight, chat_id, 2)
        # print(total_in_amount)
        # print(reply_text)
        has_been_spent = 0
        if total_in_amount:
            for item in reversed(total_in_amount):
                # if item[2] == 1:
                #     plus_total -= item[0]
                #     should_be_spent -= item[1]
                if item[2] == 1:
                    has_been_spent += item[1]

        plus_total = self.format_float(plus_total)
        should_be_spent = self.format_float(should_be_spent)
        has_been_spent = self.format_float(has_been_spent)
        

        # total_amount = int(plus_total - negative_total)
                

        reply_text += f"\n\n"
        reply_text += f"总入款：{plus_total} \n"
        reply_text += f"费率：{self.fee}% \n"
        reply_text += f"USD汇率：{self.show_exchange_rate} \n"

        reply_text += f"\n\n"
        reply_text += f"应下发：{should_be_spent}u\n"
        reply_text += f"总下发：{has_been_spent}u\n"
        reply_text += f"未下发：{self.format_float(should_be_spent - has_been_spent)}u \n"
        print(reply_text)
        print(update.message.chat_id)


        keyboard = [
            [InlineKeyboardButton("历史账单", url=f"http://bills.souho88.com?chat_id={chat_id}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_markup=reply_markup)


    def format_float(self, number):
        if number % 1 == 0:
            return int(number)  # 小数部分为0，返回整数
        else:
            return round(number, 2)  # 小数部分非0，保留两位小数