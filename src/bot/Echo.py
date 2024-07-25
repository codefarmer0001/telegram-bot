from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
import re
from datetime import datetime, timedelta
import pytz
from dao.Bills import Bills
from dao.Setting import Setting
from business.OkexPrice import OkexPrice
from dao.Grant import Grant
import re
import ast
import time


class Echo:

    def echo(self, update, context):
        message_text = update.message.text
        # print(111111)
        

        # 获取聊天类型
        chat_type = update.message.chat.type

        # 判断聊天类型
        if chat_type == 'private':
            print("这是单聊")
            return

        bill = self.get_bill_dict(update)    
        print(update.to_dict())

        grantDao = Grant()
        grantData = grantDao.get_grant_by_group_id_and_user_id(bill['group_id'], bill['user_name'], bill['user_id'])
        print(grantData)
        print(grantData)
        if grantData:
            if grantData[0][4] != 1:
                return
        elif not message_text.startswith('添加操作人') and not message_text.startswith('移除操作人'):
            print(not message_text.startswith('添加操作人'))
            print(not message_text.startswith('移除操作人'))
            return

        # print(update.to_dict())

        # 匹配入款 +1000 字符串
        pattern = r'^\+\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        # print(111111)
        if match:
            # print(update.to_dict())
            # print(bill)
            amount = message_text.replace("+", "").replace("u", "").replace("U", "")
            bill['amount'] = amount
            bill['type'] = 1
            bill['operation_symbols'] = 1
            # print(f'入账1: {message_text}')

            self.insert_bill(bill)
            # print("数据插入成功")
            self.get_history_bill(update, context, bill)
            

        # 匹配入款 +1000U 字符串
        pattern = r'^\+\d+(\.\d+)?[uU]$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'入账2: {message_text}')

            print(bill)
            amount = message_text.replace("+", "").replace("u", "").replace("U", "")
            bill['amount'] = float(amount) * float(bill['exchange_rate'])
            bill['type'] = 1
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)


        # 匹配出款 -1000 字符串
        pattern = r'^\-\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'出账1: {message_text}')

            # print(bill)
            amount = message_text.replace("-", "").replace("u", "").replace("U", "")
            bill['amount'] = amount
            bill['type'] = 2
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        # 匹配出款 -1000U 字符串
        pattern = r'^\-\d+(\.\d+)?[uU]$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'出账2: {message_text}')

            # print(bill)
            amount = message_text.replace("-", "").replace("u", "").replace("U", "")
            bill['amount'] = float(amount) * float(bill['exchange_rate'])
            bill['type'] = 2
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)


        # 匹配出款 下发1000 字符串
        pattern = r'^下发\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'下发1: {message_text}')

            # print(bill)
            amount = message_text.replace("下发", "").replace("u", "").replace("U", "")
            bill['amount'] = amount
            bill['type'] = 2
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        # 匹配出款 下发1000U 字符串
        pattern = r'^下发\d+(\.\d+)?[uU]$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'下发2: {message_text}')

            # print(bill)
            amount = message_text.replace("下发", "").replace("u", "").replace("U", "")
            bill['amount'] = float(amount) * float(bill['exchange_rate'])
            bill['type'] = 2
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)


        # 匹配出款 下发1000U 字符串
        pattern = r'^下发-\d+(\.\d+)?[uU]$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'下发2: {message_text}')

            # print(bill)
            amount = message_text.replace("下发-", "").replace("u", "").replace("U", "")
            bill['amount'] = float(amount) * float(bill['exchange_rate'])
            bill['type'] = 2
            bill['operation_symbols'] = 2

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        # 匹配修正下发 下发-1000
        pattern = r'^下发-\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'修正出款: {message_text}')

            # print(bill)
            amount = message_text.replace("下发-", "").replace("u", "").replace("U", "")
            bill['amount'] = amount
            bill['type'] = 2
            bill['operation_symbols'] = 2

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        # 匹配修正入款 入款-1000
        pattern = r'^入款-\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            # print(f'修正入款: {message_text}')

            # print(bill)
            amount = message_text.replace("入款-", "").replace("u", "").replace("U", "")
            bill['amount'] = amount
            bill['type'] = 1
            bill['operation_symbols'] = 2

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        # 匹配带汇率入款 +1000/6.8
        pattern = r'^\+\d+/\d+(\.\d+)?$'
        match = re.fullmatch(pattern, message_text)
        if match:
            # print(f'带汇率入款: {message_text}')

            # print(bill)
            message_text = message_text.replace("+", "").replace("u", "").replace("U", "")
            amountArr = message_text.split('/')
            amount = amountArr[0]
            bill['amount'] = amount
            bill['type'] = 1
            bill['exchange_rate'] = amountArr[1]
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            print('数据保存成功')
            self.get_history_bill(update, context, bill)

        # 匹配带汇率出款 -1000/6.9
        pattern = r'^\-\d+/\d+(\.\d+)?$'
        match = re.fullmatch(pattern, message_text)
        if match:
            # print(f'带汇率出款: {message_text}')

            # print(bill)
            message_text = message_text.replace("-", "").replace("u", "").replace("U", "")
            amountArr = message_text.split('/')
            amount = amountArr[0]
            bill['amount'] = amount
            bill['type'] = 2
            bill['exchange_rate'] = amountArr[1]
            bill['operation_symbols'] = 1

            self.insert_bill(bill)
            self.get_history_bill(update, context, bill)

        if "删除今日数据" == message_text or "删除今天数据" == message_text:
            # print(f'操作: {message_text}')

            billDao = Bills()
            # 获取当前日期和时间
            now = datetime.now()

            # 构造当天凌晨4点的时间
            midnight = datetime(now.year, now.month, now.day, 4, 0, 0)

            # 如果当前时间在凌晨4点之前，日期需要减去一天
            if now.hour < 4:
                midnight = midnight - timedelta(days=1)

            billDao.delete_today_bill(midnight);
            reply_text = f'今日数据删除成功'
            context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

        pattern = r'^设置汇率\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            rate = message_text.replace('设置汇率', "")
            
            setting = Setting()
            setting.insert_or_update_setting_rate(bill['group_id'], rate, bill['group_name'])
            reply_text = f'汇率调整为 {rate}'
            context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

        
        pattern = r'^设置费率\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match:
            fee = message_text.replace('设置费率', "")

            setting = Setting()
            setting.insert_or_update_setting_fee(bill['group_id'], fee, bill['group_name'])
            reply_text = f'费率调整为 {fee}'
            context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)


        if "账单" == message_text:
            self.get_history_bill(update, context, bill)

        if "显示U" == message_text or "显示u" == message_text:
            rate = message_text.replace('设置汇率', "")
            
            setting = Setting()
            setting.insert_or_update_setting_show_unit(bill['group_id'], 1, bill['group_name'])
            print('显示u')
            reply_text = f'调整显示u'
            context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

        if "隐藏U" == message_text or "隐藏u" == message_text:
            rate = message_text.replace('设置汇率', "")
            
            setting = Setting()
            setting.insert_or_update_setting_show_unit(bill['group_id'], 0, bill['group_name'])
            reply_text = f'调整隐藏u'
            context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

        
        if "w0" == message_text:
            okexPrice_instance = OkexPrice()
            okexPrice_instance.weixinPrice(update, context)

        if "z0" == message_text:
            okexPrice_instance = OkexPrice()
            okexPrice_instance.aliPrice(update, context)

        if self.is_valid_expression(message_text):
            result = self.evaluate_expression(message_text)
            if result is not None:
                print(self.format_float(result))
                update.message.reply_text(self.format_float(result), parse_mode='HTML')
            else:
                print("无效的表达式或包含不安全内容")
                
        pattern = r'^z\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match and message_text != 'z0':
            amount = message_text.replace('z', "")
            print(amount)
            okexPrice_instance = OkexPrice()
            okexPrice_instance.aliAmount(update, context, amount)

        
        pattern = r'^w\d+(\.\d+)?$'
        match = re.match(pattern, message_text)
        if match and message_text != 'w0':
            amount = message_text.replace('w', "")
            print(amount)
            okexPrice_instance = OkexPrice()
            okexPrice_instance.weixinAmount(update, context, amount)

        pattern = r'^添加操作人\s+'
        match = re.match(pattern, message_text)
        if match:
            group_id = update.message.chat.id
            user_id = update.message.from_user.id
            # print(update.message.from_user.id)
            # grantData = grant.get_grant_by_type(group_id, user_id)
            grant = Grant()
            print(grantData)
            if len(grantData) != 0 and grantData[0][3] == 1:
                effective_message = update["_effective_message"]
                if effective_message:
                    entities = effective_message['entities']
                    if entities:
                        print(1)
                        for entitie in entities:
                            group_id = update.message.chat.id
                            user_id = ''
                            user_uame = ''
                            user = entitie.user
                            if not user:
                                start = entitie.offset
                                end  = start + entitie.length
                                user_id = message_text[start:end]
                                user_uame = user_id
                            else:
                                user_id = user.id
                                sender_first_name = user.first_name
                                # print(sender_first_name)
                                sender_last_name = user.last_name
                                user_uame = f'{sender_first_name}{sender_last_name}'

                            grant.delete_grant_by_user_id(group_id, user_id)
                             # print(user_uame)
                            grant.insert_grant(group_id, user_id, 2, 1, user_uame, 0)
                            # print(333444)
                list = grant.get_grant_by_group_id(group_id)
                reply_text = '添加操作人成功！当前操作人:'
                if len(list) !=0:
                    for item in list:
                        # print(item)
                        reply_text += f'\n{item["user_name"]}'
                print(reply_text)
                context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)
            else:
                # grant = Grant()
                list = grant.get_grant_by_group_id(group_id)
                reply_text = '该设置权限人可修改:'
                if len(list) !=0:
                    for item in list:
                        # print(item)
                        if item['type'] == 1:
                            reply_text += f'\n机器人由 （{item["user_name"]}) 邀请入群'
                print(reply_text)
                message = context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

                # 模拟5秒后消息被撤回
                time.sleep(10)

                # 撤回消息
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=message.message_id)


        
        pattern = r'^移除操作人\s+'
        match = re.match(pattern, message_text)
        if match:
            group_id = update.message.chat.id
            user_id = update.message.from_user.id
            print(update.message.from_user.id)
            # grantData = grant.get_grant_by_type(group_id, user_id)
            print(not grantData)
            if len(grantData) != 0 and grantData[0][3] == 1:
                effective_message = update["_effective_message"]
                if effective_message:
                    entities = effective_message['entities']
                    grant = Grant()
                    if entities:
                        print(1)
                        for entitie in entities:
                            group_id = update.message.chat.id
                            user_id = ''
                            user = entitie.user
                            if not user:
                                start = entitie.offset
                                end  = start + entitie.length
                                user_id = message_text[start:end]
                                # user_uame = user_id
                            else:
                                user_id = user.id

                            grant.delete_grant_by_user_id(group_id, user_id)

                list = grant.get_grant_by_group_id(group_id)
                reply_text = '添加操作人成功！当前操作人:'
                if len(list) !=0:
                    for item in list:
                        # print(item)
                        reply_text += f'\n{item["user_name"]}'
                print(reply_text)
                context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

            else:
                list = grant.get_grant_by_group_id(group_id)
                reply_text = '该设置权限人可修改:'
                if len(list) !=0:
                    for item in list:
                        # print(item)
                        if item['type'] == 1:
                            reply_text += f'\n机器人由 （{item["user_name"]}) 邀请入群'
                print(reply_text)
                message = context.bot.send_message(chat_id=update.message.chat_id, text=reply_text)

                # 模拟5秒后消息被撤回
                time.sleep(10)

                # 撤回消息
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=message.message_id)


    def send_grant_user_message(self, update, context, group_id):
        print()

        

    def get_bill_dict(self, update):
        billDict = {}
        billDict['group_id'] = update.message.chat.id
        billDict['message_id'] = update.message.message_id
        billDict['user_id'] = update.message.from_user.id
        billDict['user_name'] = f'@{update.message.from_user.username}'
        timestamp = update.message.date
        # 创建UTC+0时区对象
        utc0_timezone = pytz.utc
        # 将UTC+0时间设定时区为UTC+8
        utc8_timezone = pytz.timezone('Asia/Shanghai')
        timestamp = timestamp.replace(tzinfo=utc0_timezone).astimezone(utc8_timezone)
        billDict['date'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print('setData')
        sender_first_name = update.message.from_user.first_name
        sender_last_name = update.message.from_user.last_name
        billDict['username'] = f'{sender_first_name}{sender_last_name}'

        setting = Setting()
        setData = setting.get_setting_by_group_id(billDict['group_id'])
        self.exchange_rate = 1
        self.fee = 0
        self.show_unit = '0'
        self.show_exchange_rate = 0
        print('setData')
        if setData:
            self.exchange_rate = setData[0][3]
            print(self.exchange_rate)
            self.fee = setData[0][4]
            self.show_unit = setData[0][2]
            self.show_exchange_rate = setData[0][3]
        print(f'1{float(self.exchange_rate)}')
        if float(self.exchange_rate) == 0:
            self.exchange_rate = 1
        
        billDict['exchange_rate'] = self.exchange_rate
        billDict['show_exchange_rate'] = self.show_exchange_rate
        billDict['fee'] = self.fee
        billDict['show_unit'] = self.show_unit
        billDict['group_name'] = update.message.chat.title
        print(timestamp)

        
        return billDict
    

    def insert_bill(self, bill):
        # print(bill)
        setting = Setting()
        billDao = Bills()
        result = billDao.get_bill_by_message_id(bill['message_id'])
        print(f'result结果：{result}')
        if not result:
            print(bill)
            # print(f"进入 if 分支 {int(bill['amount'])} {float(bill['exchange_rate'])} {float(bill['fee'])}")
            amount = int(bill['amount'])
            amount = amount / float(bill['exchange_rate'])
            fee = float(bill['fee']) if bill['fee'] else 0
            print(fee)
            should_be_spent = amount - amount *  (fee / 100)
            if bill['type'] == 2:
                should_be_spent = amount
            should_be_spent = self.format_float(should_be_spent)
            print(f'入账1: {should_be_spent}')
            billDao.insert_bill(bill['message_id'], bill['group_id'], bill['user_id'], bill['amount'], bill['date'], bill['type'], bill['exchange_rate'], bill['operation_symbols'], bill['username'], fee, should_be_spent)
            # print(bill)
        else:
            print("进入 else 分支")
            # print(1111111)
        
    def get_history_bill(self, update, context, bill):
        # 获取当前日期和时间
        now = datetime.now()

        # 构造当天凌晨4点的时间
        midnight = datetime(now.year, now.month, now.day, 4, 0, 0)

        # 如果当前时间在凌晨4点之前，日期需要减去一天
        if now.hour < 4:
            midnight = midnight - timedelta(days=1)

        # print(midnight)
        
        billDao = Bills()
        in_total = billDao.query_in_or_out_total(midnight, bill['group_id'], 1)
        out_total = billDao.query_in_or_out_total(midnight, bill['group_id'], 2)

        in_top5_data = billDao.query_in_or_out_top5_data(midnight, bill['group_id'], 1)
        out_top5_data = billDao.query_in_or_out_top5_data(midnight, bill['group_id'], 2)

        
        reply_text = f"入款（{in_total}笔）：\n"
        show_unit = bill['show_unit']
        print(f'显示或者隐藏u：{show_unit}')
        
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
                
                reply_text += f"{formatted_time}  {amount} \n"
                print(reply_text)

        reply_text += f"\n"
        # print(reply_text)

        reply_text += f"下发（{out_total}笔）：\n"


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

        total_in_amount = billDao.query_total_amount(midnight, bill['group_id'], 1)
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

        total_in_amount = billDao.query_total_amount(midnight, bill['group_id'], 2)
        # print(total_in_amount)
        has_been_spent = 0
        if total_in_amount:
            for item in reversed(total_in_amount):
                # print(item)
                if item[2] == 1:
                    # plus_total -= item[0]
                    has_been_spent += item[1]
                    print(item)
                    # should_be_spent -= item[1]
                if item[2] == 2:
                    print(item)
                    has_been_spent -= item[1]

            print(has_been_spent)

        plus_total = self.format_float(plus_total)
        should_be_spent = self.format_float(should_be_spent)
        has_been_spent = self.format_float(has_been_spent)

        # total_amount = int(plus_total - negative_total)
                

        reply_text += f"\n\n"
        reply_text += f"总入款：{plus_total} \n"
        reply_text += f"费率：{bill['fee']}% \n"
        reply_text += f"USD汇率：{bill['show_exchange_rate']} \n"

        reply_text += f"\n\n"
        reply_text += f"应下发：{should_be_spent}u\n"
        reply_text += f"总下发：{has_been_spent}u\n"
        reply_text += f"未下发：{self.format_float(should_be_spent - has_been_spent)}u \n"
        # print(reply_text)
        # print(update.message.chat_id)


        keyboard = [
            [InlineKeyboardButton("历史账单", url=f"http://bills.souho88.com?chat_id={bill['group_id']}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_markup=reply_markup)


    def format_float(self, number):
        if number % 1 == 0:
            return int(number)  # 小数部分为0，返回整数
        else:
            return round(number, 2)  # 小数部分非0，保留两位小数

    def is_valid_expression(self, expression):
        # 使用正则表达式匹配只包含数字和四则运算符的字符串
        pattern = re.compile(r'^-?\d[\d\s]*[\+\-\*/.()]?\d[\d\s\+\-\*/.()]*$')
        return pattern.match(expression) is not None and expression[0].isdigit()

    def starts_with_operator(s):
        # 使用正则表达式判断字符串是否以 +, -, *, / 开头
        pattern = re.compile(r'^[\+\-\*/]')
        return pattern.match(s) is not None


    def evaluate_expression(self, expression):
        try:
            parsed_expr = ast.parse(expression, mode='eval')
            result = eval(compile(parsed_expr, filename='', mode='eval'))
            return result
        except (SyntaxError, TypeError):
            return None  # 表达式无效或包含不安全内容


        # print(reply_text)

        # reply_text = f'成功入账 {amount}'
        
