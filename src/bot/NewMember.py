from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from dao.Grant import Grant
import config
from telegram import ParseMode

class NewMember:
    def handler(self, update, context):
        print(update)
        # 获取添加机器人进群的用户 ID
        for member in update.message.new_chat_members:
            print(f"获取添加机器人进群的用户 ID:{member.id},{config.TOKEN}")
            if config.TOKEN.find(str(member.id)) != -1:
                print(f"获取添加机器人进群的用户 ID:{member.id}")
                group_id = update.message.chat.id
                sender_first_name = update.message.from_user.first_name
                sender_last_name = update.message.from_user.last_name
                user_uame = f'{sender_first_name}{sender_last_name}'
                group_id = update.message.chat.id
                user_id = update.effective_user.id
                grant = Grant()
                grant.delete_grant_by_user(group_id, user_id, user_uame)
                data = grant.get_template_data(user_id)
                if data:
                    grant.insert_grant(group_id, user_id, 1, 1, user_uame, 0)
                    print(f'群组id：{group_id}, 用户id：{user_id}')
                else:
                    grant.insert_grant(group_id, user_id, 1, 2, user_uame, 0)
                #     print(f'群组id：{group_id}, 用户id：{user_id}')
                    # 做一些事情，例如向用户发送一条欢迎消息
                    # update.message.send_message(user_id, "欢迎加入群聊！")
                # context.bot.send_message(chat_id=group_id, text='欢迎使用本助手，请点击 /help 查看操作帮助1', parse_mode=ParseMode.MARKDOWN)
                

    def new_group_grant(self, bot, group_id, user_id, user_uame):
        grant = Grant()
        grant.delete_grant_by_user(group_id, user_id, user_uame)
        data = grant.get_template_data(user_id)
        if data:
            grant.insert_grant(group_id, user_id, 1, 1, user_uame, 0)
        else:
            grant.insert_grant(group_id, user_id, 1, 0, user_uame, 0)
        
        bot.send_message(chat_id=group_id, text='欢迎使用本助手，请点击 /help 查看操作帮助', parse_mode=ParseMode.MARKDOWN)

        