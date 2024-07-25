from flask import Blueprint
from flask import Flask, request
from utils.JwtUtil import JwtUtil
from utils.APIResponse import APIResponse
from dao.Grant import Grant
from passlib.hash import bcrypt

grant_blue = Blueprint('grant', __name__)


@grant_blue.route('/page', methods=['get', 'post'])
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
    grantDao = Grant()
    page = grantDao.get_page(data['pageIndex'], data['pageSize'], searchKey)
    # print(page)
    return APIResponse(status_code=500, data=page).result()


@grant_blue.route('/setGrant', methods=['get', 'post'])
def grant():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    print(data)
    if 'id' not in data:
        return APIResponse(status_code=500, message='用户id为空').result()

    # print(data)
    grantDao = Grant()
    page = grantDao.update_grant_status(data['id'], data['status'])
    print(page)
    return APIResponse(status_code=200, message="授权成功").result()


@grant_blue.route('/setGrantTemplate', methods=['get', 'post'])
def setGrantTemplate():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    # print(data)
    if 'id' not in data:
        return APIResponse(status_code=500, message='用户id为空').result()

    print(data)
    grantDao = Grant()
    data = grantDao.get_grant(data['id'])
    template_data = grantDao.get_template_data(data['user_id'])
    print(data)
    if not template_data:
        grantDao.insert_grant('', data['user_id'], data['type'], data['status'], data['user_name'], 1)
    # print(page)
    return APIResponse(status_code=200, message="授权模板设定成功").result()


@grant_blue.route('/removeGrantTemplate', methods=['get', 'post'])
def removeGrantTemplate():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    # print(data)
    if 'id' not in data:
        return APIResponse(status_code=500, message='用户id为空').result()

    # print(data)
    grantDao = Grant()
    grantDao.delete_grant(data['id'])
    # print(page)
    return APIResponse(status_code=200, message="授权模板移除成功").result()