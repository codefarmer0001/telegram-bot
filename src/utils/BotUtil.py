from telegram import Bot
import config

class BotUtil:

    def __init__(self):
        self.bot = Bot(config.TOKEN)


    # def get_group_owner(self, group_id):
    #     # 获取群组的详细信息
    #     chat = self.bot.get_chat(group_id=group_id)
    #     print(chat)
    #     # 提取群组创建者的用户ID
    #     creator_id = chat['pinned_message']['from']['id']

    #     return creator_id

    def get_chat_administrators(self, group_id):
        # 获取群组的管理员
        administrators = self.bot.get_chat_administrators(group_id=group_id)

        # 提取管理员的用户 ID
        admin_ids = [admin.user.id for admin in administrators]
        return admin_ids