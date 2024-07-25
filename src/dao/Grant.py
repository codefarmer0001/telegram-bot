from db.SQLiteDB import SQLiteDB
import math

class Grant:
    def __init__(self):
        # 创建或连接到数据库
        self.db = SQLiteDB()
        self.table_name = 'grant'
        
        # 检查并应用数据库升级
        # self.db.check_and_apply_upgrade()

        # 创建帐单表
        self.create_grant_table()
        self.add_column_is_template()
        self.add_column_group_name()

    def create_grant_table(self):
        columns = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 帐单表的唯一标识符
            group_id TEXT, -- 频道/群组id
            user_id TEXT, -- 显示/隐藏u
            type INTEGER, -- 权限类型，1机器人拉进群的人，拥有最高权限，2机器人所有者添加的授权的人
            status INTEGER, -- 状态，0为待授权，1为已授权
            user_name TEXT, -- 用户昵称
            is_template INTEGER, -- 权限模板
            group_name TEXT -- 群组名称
        '''
        self.db.create_table(self.table_name, columns)

    def insert_grant(self, group_id, user_id, type1, status, user_name, is_template):
        data = (None, group_id, user_id, type1, status, user_name, is_template, '')
        self.db.insert_data(self.table_name, data)

    def add_column_is_template(self):
        self.db.add_column_if_not_exists(self.table_name, 'is_template', 'INTEGER')

    def add_column_group_name(self):
        self.db.add_column_if_not_exists(self.table_name, 'group_name', 'TEXT')

    def get_all_grant(self):
        return self.db.query_data(self.table_name)

    def update_grant(self, bill_id, description, amount, date, category):
        set_values = f"description = '{description}', amount = {amount}, date = '{date}', category = '{category}'"
        condition = f"id = {bill_id}"
        self.db.update_data(self.table_name, set_values, condition)

    def delete_grant(self, id):
        condition = f"id = {id}"
        self.db.delete_data(self.table_name, condition)

    def get_grant(self, id):
        condition = f"id = {id}"
        return self.db.query_data_json(self.table_name, condition)
    
    def get_template_data(self, user_id):
        condition = f"user_id='{user_id}' and type=1 and is_template = 1"
        print(condition)
        data = self.db.query_data_json(self.table_name, condition)
        return data

    def delete_grant_by_user_id(self, group_id, user_id):
        condition = f"group_id = '{group_id}' and user_id = '{user_id}'"
        self.db.delete_data(self.table_name, condition)

    def delete_grant_by_user(self, group_id, user_id, user_name):
        condition = f"group_id = '{group_id}' and (user_id = '{user_id}' or user_id = '{user_name}')"
        self.db.delete_data(self.table_name, condition)

    def delete_grant_by_group_id(self, group_id):
        condition = f"group_id = {group_id}"
        self.db.delete_data(self.table_name, condition)

    def get_grant_by_group_id_and_user_id(self, group_id, user_name, user_id):
        condition = f"group_id = '{group_id}' and (user_id='{user_id}' or user_id='{user_name}')"
        data = self.db.query_data(self.table_name, condition)
        return data
    
    def get_grant_by_type(self, group_id, user_id):
        condition = f"group_id='{group_id}' and user_id='{user_id}' and type=1"
        print(condition)
        data = self.db.query_data(self.table_name, condition)
        return data
    
    def get_grant_by_group_id(self, group_id):
        condition = f"group_id = '{group_id}' and status = 1"
        data = self.db.query_all_data(self.table_name, 'type', condition)
        return data

    def get_page(self, pageIndex, pageSize, searchKey = None):
        result = {}
        condition = f'(is_template != 1 or is_template is null)'
        print(condition)
        # condition = ''
        if searchKey:
            condition += f" and user_name like '%{searchKey}%'"
        count = self.db.query_data_count(self.table_name, condition)
        result['total'] = count
        result['pageIndex'] = pageIndex
        result['pageSize'] = pageSize
        result['totalPage'] = math.ceil(int(count) / int(pageSize))

        template_data = self.db.query_all_data(table_name=self.table_name, order_by_column = 'id', condition = 'is_template = 1')
        
        if count > 0:
            offset = (int(pageIndex) - 1) * int(pageSize)
            data = self.db.query_data_by_page(table_name = self.table_name, order_by_column = 'id', pageSize = pageSize, offset = offset, condition = condition)
            # print(data)
            template_data.extend(data)
            # print(template_data)
            result['data'] = template_data
            return result
        
        return result

    def update_grant_status(self, id, status):
        set_values = f"status =  {status}"
        condition = f"id = {id}"
        self.db.update_data(self.table_name, set_values, condition)
