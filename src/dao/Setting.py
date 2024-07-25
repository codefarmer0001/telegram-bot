from db.SQLiteDB import SQLiteDB
from utils.BotUtil import BotUtil

class Setting:
    def __init__(self):
        # 创建或连接到数据库
        self.db = SQLiteDB()
        self.table_name = 'setting'
        
        # 检查并应用数据库升级
        # self.db.check_and_apply_upgrade()

        # 创建帐单表
        self.create_setting_table()

    def create_setting_table(self):
        columns = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 帐单表的唯一标识符
            group_id TEXT, -- 频道/群组id
            show_unit TEXT, -- 显示/隐藏u
            exchange_rate TEXT, -- 账单金额
            fee TEXT, -- 手续费
            group_owner TEXT, -- 群主id
            group_name TEXT --群组名称
        '''
        self.db.create_table(self.table_name, columns)

    def insert_setting(self, group_id, show_unit, exchange_rate, fee, group_owner, group_name):
        data = (None, group_id, show_unit, exchange_rate, fee, group_owner, group_name)
        self.db.insert_data(self.table_name, data)

    def get_all_setting(self):
        return self.db.query_data(self.table_name)

    # def update_setting(self, bill_id, description, amount, date, category):
    #     set_values = f"description = '{description}', amount = {amount}, date = '{date}', category = '{category}'"
    #     condition = f"id = {bill_id}"
    #     self.db.update_data(self.table_name, set_values, condition)

    def delete_setting(self, bill_id):
        condition = f"id = {bill_id}"
        self.db.delete_data(self.table_name, condition)

    def get_setting_by_group_id(self, group_id):
        condition = f"group_id = '{group_id}'"
        data = self.db.query_data(self.table_name, condition)
        return data

    def insert_or_update_setting_rate(self, group_id, exchange_rate, group_name):
        data = self.get_setting_by_group_id(group_id)
        print(data)
        if not data:
            print(1)
            self.insert_setting(group_id, 0, exchange_rate, 0, '', group_name)
        else:
            print(2)
            set_values = f"exchange_rate={exchange_rate}"
            condition = f"group_id = {group_id}"
            self.db.update_data(self.table_name, set_values, condition)



    def insert_or_update_setting_fee(self, group_id, fee, group_name):
        data = self.get_setting_by_group_id(group_id)
        print(data)
        if not data:
            self.insert_setting(group_id, 0, 1, fee, '', group_name)
        else:
            set_values = f"fee={fee}"
            condition = f"group_id = {group_id}"
            self.db.update_data(self.table_name, set_values, condition)

    def insert_or_update_setting_show_unit(self, group_id, unit, group_name):
        data = self.get_setting_by_group_id(group_id)
        if not data:
            # print(1)
            self.insert_setting(group_id, unit, 1, '', '', group_name)
        else:
            # print(2)
            set_values = f"show_unit={unit}"
            condition = f"group_id = {group_id}"
            self.db.update_data(self.table_name, set_values, condition)

    # def get_group_owner(self, group_id):
    #     print(group_id)
    #     condition = f"group_id = '{group_id}'"
    #     print(condition)
    #     data = self.db.query_data(self.table_name, condition)
    #     if data:
    #         print(data)
    #         return data.group_owner
    #     else:
    #         print(data)
    #         botUtil = BotUtil()
    #         group_owner = botUtil.get_group_owner(group_id)
    #         print(group_owner)
    #         self.insert_setting(group_id, 0, None, None, group_owner)
    #         return group_owner


