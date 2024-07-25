from flask import Blueprint
from flask import Flask, request
from utils.JwtUtil import JwtUtil
from utils.APIResponse import APIResponse
from dao.User import User
from passlib.hash import bcrypt

auth_blue = Blueprint('auth', __name__)

# 定义蓝图路径及请求方法和请求返回逻辑
@auth_blue.route('/login', methods=['post'])
def login():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    # print(data)
    if 'account' in data and 'password' in data:
        account = data['account']
        password = data['password']
        # password = hashed_password = bcrypt.using(salt_size=22).hash(password)
        # print(password)
        userDao = User()
        result = userDao.get_user_by_account_password(account)
        if result:
            userItem = result[0]
            print(userItem)
            if bcrypt.verify(password, userItem[3]):
                print("密码匹配")
                loginResult = {}
                loginResult['id'] = userItem[0]
                loginResult['account'] = userItem[1]
                loginResult['fullName'] = userItem[3]
                loginResult['role'] = 'admin'
                loginResult['username'] = userItem[1]
                jwtToken = JwtUtil()
                accessToken = jwtToken.generate_jwt(loginResult)
                
                userAbilitie = {}
                userAbilitie['action'] = 'manage'
                userAbilitie['subject'] = 'all'
                userAbilities = [userAbilitie]
                # userAbilities.append(userAbilitie)

                loginData = {
                    "accessToken": accessToken,
                    "userAbilities": userAbilities,
                    "userData": loginResult
                }
                return APIResponse(status_code=500, data=loginData).result()

            else:
                return APIResponse(status_code=500, message='登陆错误，密码不匹配').result()
            # print(result)
            # return APIResponse(status_code=500, message='登陆错误，账号不存在').result()
        else:
            return APIResponse(status_code=500, message='登陆错误，账号不存在').result()

        print(account)
        return account
    return APIResponse(status_code=500, message='账号或者密码为空').result()

@auth_blue.route('/page', methods=['get', 'post'])
def searchproduct():
    # 获取通过 POST 请求的 JSON 数据
    data = request.get_json()
    print(data)
    if 'pageIndex' not in data or 'pageSize' not in data:
        return APIResponse(status_code=500, message='分页信息为空').result()

    searchKey = None
    if 'searchKey' in data:
        searchKey = data['searchKey']

    print(data)
    userDao = User()
    page = userDao.get_page(data['pageIndex'], data['pageSize'], searchKey)
    print(page)
    return APIResponse(status_code=500, data=page).result()