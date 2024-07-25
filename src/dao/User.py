from db.SQLiteDB import SQLiteDB
import math

class User:
    def __init__(self):
        # 创建或连接到数据库
        self.db = SQLiteDB()
        self.table_name = 'user'
        
        # 检查并应用数据库升级
        # self.db.check_and_apply_upgrade()

        # 创建帐单表
        self.create_user_table()

    def create_user_table(self):
        columns = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 帐单表的唯一标识符
            group_id TEXT, -- 群组id
            account TEXT, -- 登陆账户
            password TEXT, -- 登陆密码
            full_name TEXT, -- 全部账号
            type INTEGER -- 用户类型，1为超级管理，2为普通管理
        '''
        self.db.create_table(self.table_name, columns)

    def insert_user(self, group_id, account, password, full_name, type1):
        data = (None, group_id, account, password, full_name, type1)
        self.db.insert_data(self.table_name, data)

    def get_all_user(self):
        return self.db.query_data(self.table_name)

    def update_user(self, account, password, status):
        set_values = f"description = '{description}', amount = {amount}, date = '{date}', category = '{category}'"
        condition = f"id = {bill_id}"
        self.db.update_data(self.table_name, set_values, condition)

    def delete_user(self, id):
        condition = f"id = {id}"
        self.db.delete_data(self.table_name, condition)

    def delete_user_by_group_id(self, group_id):
        condition = f"group_id = {group_id}"
        self.db.delete_data(self.table_name, condition)

    def get_user_by_account_password(self, account):
        condition = f"account = '{account}'"
        data = self.db.query_data(self.table_name, condition)
        return data

    def get_page(self, pageIndex, pageSize, searchKey = None):
        result = {}
        condition = ''
        if searchKey:
            condition = f"full_name like '%{searchKey}%'"
        count = self.db.query_data_count(self.table_name, condition)
        result['total'] = count
        result['pageIndex'] = pageIndex
        result['pageSize'] = pageSize
        result['totalPage'] = math.ceil(int(count) / int(pageSize))
        if count > 0:
            offset = (int(pageIndex) - 1) * int(pageSize)
            print(offset)
            data = self.db.query_data_by_page(table_name = self.table_name, order_by_column = 'id', pageSize = pageSize, offset = offset, condition = condition)
            result['data'] = data
            return result
        
        return result
        


