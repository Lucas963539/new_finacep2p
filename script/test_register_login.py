from time import sleep

import allure
import requests
import pytest
import logging


from api.api_register_login import ApiRegisterLogin
from util import read_json, read_yaml, clean_data

# logging.basicConfig(level=logging.INFO,filename="./log/p2p_test.log")
log = logging.getLogger(__name__)


@allure.epic("金融P2P")
@allure.feature("登录注册模块")
class TestRegisterLogin:

    # @classmethod
    # # 在注册登录类开始前执行一次
    # def seup_class(cls):
    #     # 清除测试数据
    #     clean_data()

    # 初始化
    def setup(self):
        with allure.step("1.创建session对象"):
            log.info("正在创建session对象")
            self.seesion = requests.session()
        with allure.step("2.实例化ApiRegisterLogin对象"):
            log.info("正在创建ApiRegisterLogin实例")
            self.reg = ApiRegisterLogin(self.seesion)

    # 结尾清理工作
    def teardown(self):
        with allure.step("关闭session"):
            log.info(f"正在关闭session对象：{self.seesion}")
            self.seesion.close()

    # 1.获取图片验证码接口  测试
    @allure.story("获取图片验证码接口  测试")
    @pytest.mark.parametrize("random,expect_code",read_yaml("register_login.yaml", "img_code"))
    def test_get_img_code(self,random,expect_code):
        try:
            with allure.step("1. 调用获取图片验证码接口"):
                result = self.reg.api_get_img_code(random)
                log.info(f'正在执行图片验证码接口，响应状态码为：{result.status_code}')
            with allure.step("2. 断言响应状态码"):
                assert expect_code == result.status_code
                log.info(f'执行图片验证码接口，断言通过')
        except Exception as e:
            # 打印错误日志
            log.error(f'断言失败，失败原因{e}')
            # 捕获错误信息 有异常需要抛出，不然断言结果会与实际结果不同
            raise

    # 2.获取短信验证码接口  测试
    @allure.story("获取短信验证码接口  测试")
    @pytest.mark.parametrize("phone, imgVerifyCode, expect_text", read_json("register_login_data.json", "phone_code"))
    def test_get_phone_code(self, phone, imgVerifyCode, expect_text):
        try:
            # 先调取获取图片验证码接口，让session记住cookie
            with allure.step("1.调用获取图片验证码接口"):
                self.reg.api_get_img_code(12)
            with allure.step("2.调取获取短信验证码接口"):
                result = self.reg.api_get_phone_code(phone, imgVerifyCode)
                log.info(f'执行结果为：{result.text}')
            with allure.step("3.断言响应文本信息"):
                assert expect_text in result.text
                log.info("执行断言通过")
        except Exception as e:
            # 打印错误日志
            # print(f'接口有误，错误内容{e}')
            log.error(f'断言失败，失败原因{e}')
            # 捕获错误信息
            raise

    # 3.注册接口  测试
    @allure.story("注册接口  测试")
    @pytest.mark.parametrize("phone, password, imgVerifyCode, phone_code,expect_text", read_json("register_login_data.json", "register"))
    def test_register(self, phone, password, imgVerifyCode, phone_code,expect_text):
        try:
            with allure.step("1.调用获取图片验证码接口"):
                self.reg.api_get_img_code(12)
            with allure.step("2.调取获取短信验证码接口"):
                self.reg.api_get_phone_code(phone=phone, imgVerifyCode=imgVerifyCode)
            with allure.step("3.调取注册接口"):
                result = self.reg.api_register(
                    phone=phone,
                    password=password,
                    verifycode=imgVerifyCode,
                    phone_code=phone_code,
                )
                log.info(f'执行结果为：{result.text}')
            with allure.step("3.断言响应文本信息"):
                assert expect_text in result.text
                log.info("执行断言通过")
        except Exception as e:
            # 打印错误日志
            log.error(f'断言失败，失败原因{e}')
            # 捕获错误信息
            raise

    # 4.登录接口 测试
    @allure.story("登录接口  测试")
    @pytest.mark.parametrize("keywords, password, expect_text", read_json("register_login_data.json", "login"))
    def test_login(self, keywords, password, expect_text):
        try:
            i = 1
            result = None
            if "error" in password:
                while i <= 3:
                    with allure.step("测试锁定"):
                        result = self.reg.api_login(keywords, password)
                        log.info(f'执行结果为：{result.text}')
                    i += 1
                print("断言：", result.text)
                with allure.step("断言锁定"):
                    assert "锁定" in result.text
                    log.info("执行断言通过")
                # 暂停60秒
                sleep(61)
                with allure.step("测试登录成功"):
                    result = self.reg.api_login(keywords="15815800001", password="test123")
                    log.info(f'执行结果为：{result.text}')

                with allure.step("断言登录成功"):
                    assert expect_text in result.text
                    log.info("执行断言通过")
            else:
                with allure.step("测试登录成功"):
                    result = self.reg.api_login(keywords=keywords, password=password)
                    log.info(f'执行结果为：{result.text}')
                with allure.step("断言登录成功"):
                    assert expect_text in result.text
                    log.info("执行断言通过")
        except Exception as e:
            # 打印错误日志
            log.error(f'断言失败，失败原因{e}')
            # 捕获错误信息
            raise

    # 5.登录状态查询接口  测试
    @allure.story("登录状态查询接口  测试")
    @pytest.mark.parametrize("status, expect_text",read_json("register_login_data.json", "login_status"))
    def test_login_status(self, status, expect_text):
        try:
            if "已登录" == status:
                with allure.step("调取登录结果"):
                    self.reg.api_login(keywords="15815800001", password="test123")
                with allure.step("登录状态查询接口测试"):
                    result = self.reg.api_login_status()
                    log.info(f'执行结果为：{result.text}')
                with allure.step("断言已登录"):
                    assert expect_text in result.text
                    log.info("执行断言通过")
        except Exception as e:
            # 打印错误日志
            log.error(f'断言失败，失败原因{e}')
            # 捕获错误信息
            raise
