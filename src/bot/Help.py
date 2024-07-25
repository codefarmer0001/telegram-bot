from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

class Help:

    def help(self, update, context):
        message = (
            "群组记账机器人 使用说明\n"
            "\n"
            "1.『基础设置』\n"
            "① 添加机器人进群\n"
            "② 添加操作人\n"
            "③ 设置汇率发送 ” 设置汇率6.5 ” \n"
            "设置费率/点位发送 ” 设置费率0 “ \n"
            "\n"
            "2.『操作指令』\n"
            "+1000  入款1000\n"
            "+1000u  入款1000 USDT\n"
            "下发1000  出款1000  \n"
            "下发1000u  出款1000 USDT\n"
            "+1000/6.8  用6.8汇率入款1000\n"
            "-1000/7.2  用7.2汇率出款1000\n"
            "\n"
            "账单 查看账单\n"
            "清空今日账单 删除当前账单\n"
            "设置汇率6.8 表示设置u汇率6.8\n"
            "设置汇率0  表示切换单币种记账\n"
            "显示U 打开U显示\n"
            "隐藏U 关闭U显示\n"
            "\n"
            "3.『错账修正』 \n"
            "入款-1000 入款减1000\n"
            "下发-1000 出款减1000\n"
            "\n"
            "4.『快捷指令』\n"
            "z0   欧易支付宝实时价格\n"
            "w0   欧易微信实时价格\n"
            "z1000  计算1000元换算USDT\n"
            "添加操作人 添加操作人+空格+选中操作人\n"
            "移除操作人 移除操作人+空格+选中操作人\n"
            "/help 查看操作帮助\n"
        )
        # 获取消息文本
        # message_text = update.message.text
        # print(update.to_dict())
        # 获取消息所在的群组或频道的 ID
        # group_id = update.message.group_id

        # print(f"Received message '{message_text}' from chat ID {group_id}")

        print(update.to_dict())

        context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
