from flask import Blueprint
from flask import Flask, request
from utils.JwtUtil import JwtUtil
from utils.APIResponse import APIResponse
from dao.Bills import Bills
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import pytz

bills_blue = Blueprint('bills', __name__)


@bills_blue.route('/page', methods=['get', 'post'])
def page():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    print(data)
    if 'pageIndex' not in data or 'pageSize' not in data:
        return APIResponse(status_code=500, message='分页信息为空').result()

    searchKey = None
    if 'searchKey' in data:
        searchKey = data['searchKey']

    # print(data)
    billDao = Bills()
    page = billDao.get_page(data['pageIndex'], data['pageSize'], searchKey)
    print(page)
    return APIResponse(status_code=500, data=page).result()


@bills_blue.route('/getAlldate', methods=['get', 'post'])
def get_all_date():
    # 获取通过 POST 请求的 JSON 数据
    print(1111)
    chat_id = request.args.get('chat_id')
    print(chat_id)
    billDao = Bills()
    dateList = billDao.get_all_date(chat_id)
    return APIResponse(status_code=200, data=dateList).result()


@bills_blue.route('/data', methods=['get', 'post'])
def data():
    # 获取通过 POST 请求的 JSON 数据
    chat_id = request.args.get('chat_id')
    date = request.args.get('date')
    print(date)
    if not date:
        return APIResponse(status_code=500, message="时间参数为空").result()

    # 将字符串转换为 datetime 对象并设置时区为 UTC
    datetime_object = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=pytz.utc)

    # 设置目标时区
    target_timezone = pytz.timezone("Asia/Shanghai")

    # 转换时区
    datetime_object = datetime_object.astimezone(target_timezone)

    # 计算凌晨4点
    start_time = datetime_object.replace(hour=4, minute=0, second=0, microsecond=0)

    # 计算次日凌晨4点
    end_time = start_time + timedelta(days=1)

        # print(midnight)
        
    billDao = Bills()

    in_data = billDao.query_in_or_out_data(start_time, end_time, chat_id, 1)
    out_data = billDao.query_in_or_out_data(start_time, end_time, chat_id, 2)


    total_in_amount = billDao.query_sum_amount(start_time, end_time, chat_id, 1)
    plus_total = 0
    should_be_spent = 0
    if total_in_amount:
        for item in reversed(total_in_amount):
            if item[2] == 1:
                plus_total += item[0]
                should_be_spent += item[1]
            if item[2] == 2:
                plus_total -= item[0]
                should_be_spent -= item[1]

    total_in_amount = billDao.query_sum_amount(start_time, end_time, chat_id, 2)
    has_been_spent = 0
    if total_in_amount:
        for item in reversed(total_in_amount):
            if item[2] == 1:
                has_been_spent += item[1]

    data = {
        "inData": in_data,
        "outData": out_data,
        "plusTotal": plus_total,
        "shouldBeSpent": should_be_spent,
        "hasBeenSpent": has_been_spent
    }

    print(data)

    # print(data)
    # billDao = Bills()
    # dateList = billDao.get_all_date(date)
    return APIResponse(status_code=200, data=data).result()