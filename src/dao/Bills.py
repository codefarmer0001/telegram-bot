from db.SQLiteDB import SQLiteDB
import math

class Bills:
    def __init__(self):
        # 创建或连接到数据库
        self.db = SQLiteDB()
        self.table_name = 'bills'
        
        # 检查并应用数据库升级
        # self.db.check_and_apply_upgrade()

        # 创建帐单表
        self.create_bill_table()
        self.add_column_group_name()

    def create_bill_table(self):
        table_name = 'bills'
        columns = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 帐单表的唯一标识符
            message_id TEXT, -- 消息id，防止重复
            group_id TEXT, -- 频道/群组id
            user_id TEXT, -- 来自谁的
            amount REAL, -- 账单金额
            date TEXT, -- 出/入账时间
            type INTEGER, -- 出/入帐，1为入账，2为出账
            exchange_rate TEXT, -- 汇率
            operation_symbols INTEGER, -- 运算符号，1为加，2为减
            username TEXT, -- 操作人
            fee TEXT, -- 当前这笔费率
            should_be_spent TEXT, -- 应支出
            group_name TEXT -- 群组名称
        '''
        self.db.create_table(self.table_name, columns)

    def add_column_group_name(self):
        self.db.add_column_if_not_exists(self.table_name, 'group_name', 'TEXT')

    def get_bill_by_message_id(self, message_id):
        condition = f'message_id="{message_id}"'
        return self.db.query_data(self.table_name, condition)

    def insert_bill(self, message_id, group_id, user_id, amount, date, type1, exchange_rate, operation_symbols, username, fee, should_be_spent):
        data = (None, message_id, group_id, user_id, amount, date, type1, exchange_rate, operation_symbols, username, fee, should_be_spent, '')
        print(message_id)
        self.db.insert_data(self.table_name, data)

    def get_all_bills(self):
        return self.db.query_data(self.table_name)

    def update_bill(self, bill_id, description, amount, date, category):
        set_values = f"description = '{description}', amount = {amount}, date = '{date}', category = '{category}'"
        condition = f"id = {bill_id}"
        self.db.update_data(self.table_name, set_values, condition)

    def delete_bill(self, bill_id):
        condition = f"id = {bill_id}"
        self.db.delete_data(self.table_name, condition)

    def delete_today_bill(self, start_time):
        condition = f"date >= '{start_time}'"
        # print(condition)
        self.db.delete_data(self.table_name, condition)

    def query_in_or_out_total(self, date, group_id, type1):
        condition = f"date >= '{date}' and group_id = '{group_id}' and type = {type1}"
        # print(condition)
        return self.db.query_data_count(self.table_name, condition)

    def query_in_or_out_top5_data(self, date, group_id, type1):
        condition = f"date >= '{date}' and group_id = '{group_id}' and type = {type1}"
        # print(condition)
        return self.db.query_top5_data(self.table_name, 'date', condition)

    def query_total_amount(self, date, group_id, type1):
        select_colum = f"sum(amount) as total_amount, sum(should_be_spent) as should_be_spent, operation_symbols "
        condition = f"date >= '{date}' and group_id = '{group_id}' and type = {type1}"
        print(condition)
        return self.db.query_aggregation_data(self.table_name, select_colum, 'operation_symbols', condition)

    
    def get_page(self, pageIndex, pageSize, searchKey = None):
        result = {}
        condition = ''
        if searchKey:
            condition = f"group_id = '{searchKey}'"
        count = self.db.query_data_count(self.table_name, condition)
        result['total'] = count
        result['pageIndex'] = pageIndex
        result['pageSize'] = pageSize
        result['totalPage'] = math.ceil(int(count) / int(pageSize))
        if count > 0:
            offset = (int(pageIndex) - 1) * int(pageSize)
            print(offset)
            data = self.db.query_data_by_page(table_name = self.table_name, order_by_column = 'date', pageSize = pageSize, offset = offset, condition = condition)
            result['data'] = data
            return result
        
        return result

    def get_all_date(self, chat_id):
        select_colum = f"distinct strftime('%Y-%m-%d', `date`) AS key, strftime('%Y-%m-%d', `date`) AS value "
        condition = f"`date` >= date('now', '-16 days') and group_id='{chat_id}'"
        print(condition)
        return self.db.query_colum_data(self.table_name, select_colum, 'date', condition)


    def query_in_or_out_top5_data(self, date, group_id, type1):
        condition = f"date >= '{date}' and group_id = '{group_id}' and type = {type1}"
        # print(condition)
        return self.db.query_top5_data(self.table_name, 'date', condition)


    def query_in_or_out_data(self, start_date, end_time, group_id, type1):
        condition = f"date >= '{start_date}' and date < '{end_time}' and group_id = '{group_id}' and type = {type1}"
        # print(condition)
        return self.db.query_all_data(self.table_name, 'date', condition)


    def query_sum_amount(self, start_date, end_time, group_id, type1):
        select_colum = f"sum(amount) as total_amount, sum(should_be_spent) as should_be_spent, operation_symbols "
        condition = f"date >= '{start_date}' and date < '{end_time}' and group_id = '{group_id}' and type = {type1}"
        print(condition)
        return self.db.query_aggregation_data(self.table_name, select_colum, 'operation_symbols', condition)


# # 创建帐单表和插入一些示例数据
# bill_table = BillTable()
# bill_table.insert_bill("Groceries", 50.0, "2023-01-01", "Food")
# bill_table.insert_bill("Internet", 30.0, "2023-01-05", "Utilities")

# # 查询并打印所有帐单
# all_bills = bill_table.get_all_bills()
# print("All Bills:")
# for bill in all_bills:
#     print(bill)
