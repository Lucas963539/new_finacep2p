import logging

import allure

from api import log
from config import HOST

# log = logging.getLogger(__name__)


class ApiRegisterLogin:

    # 初始化
    def __init__(self, session):
        # 获取session
        self.session = session
        # 获取图片验证码接口 url
        self.__url_get_img_code = HOST + "/common/public/verifycode1/{}"
        # 获取短信验证码接口 url
        self.__url_get_phone_code = HOST + "/member/public/sendSms"
        # 注册接口 url
        self.__url_register = HOST + "/member/public/reg"
        # 登录接口 url
        self.__url_login = HOST + "/member/public/login"
        # 查询登录状态接口 url
        self.__url_login_status = HOST + "/member/public/islogin"

    # 获取图片验证码接口 封装
    def api_get_img_code(self, random):
        log.info(f'正在调用获取图片验证码接口，请求方法："get",请求url是{self.__url_get_img_code.format(random)}')
        return self.session.get(self.__url_get_img_code.format(random))

    # 获取短信验证码接口 封装
    def api_get_phone_code(self, phone, imgVerifyCode):
        data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": "reg"
        }
        log.info(f'正在获取短信验证码接口，请求方法："post",请求url：{self.__url_get_phone_code}，请求参数：{data}')
        return self.session.post(self.__url_get_phone_code,
                             data=data)

    # 注册接口 封装
    def api_register(self, phone, password, verifycode, phone_code):
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": "on",
            "invite_phone": ""
        }
        log.info(f'正在调取注册接口，请求方法："post", 请求url：{self.__url_register},请求参数：{data}')
        return self.session.post(self.__url_register, data=data)

    # 登录接口 封装
    def api_login(self, keywords, password):
        data = {
            "keywords": keywords,
            "password": password
        }
        log.info(f'正在调取登录接口，请求方法："post",请求url：{self.__url_login},请求参数：{data}')
        return self.session.post(self.__url_login, data=data)

    # 查询登录状态接口 封装
    def api_login_status(self):
        log.info(f'正在调取查询登录状态接口，请求方法："post", 请求url：{self.__url_login_status}')
        return self.session.post(self.__url_login_status)


