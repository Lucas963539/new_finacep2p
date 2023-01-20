import allure
import pytest
import requests

from script import log
from api.api_approve_trust import ApiApproveTrust
from api.api_register_login import ApiRegisterLogin
from util import parser_html, read_yaml


@allure.epic("金融P2P")
@allure.feature("认证开户模块")
class TestApproveTrust:

    # 初始化
    def setup(self):
        # 1.获取session对象
        self.session = requests.session()
        # 2.实例化ApiApproveTrust类
        self.approve = ApiApproveTrust(self.session)
        # 3.调取登录成功
        ApiRegisterLogin(self.session).api_login("15815800001","test123")

    # 结束
    def teardown(self):
        # 关闭session
        self.session.close()

    # 1.认证接口 测试
    @allure.story("认证接口 测试")
    def test_approve(self):
        try:
            with allure.step("调取认证接口"):
                result = self.approve.api_approve()
                log.info(f"正在执行认证接口，执行结果为{result.text}")

            with allure.step("断言结果成功"):
                assert "成功" in result.text
                log.info("执行断言通过")
        except Exception as e:
            log.error(f"断言错误！！！原因：{e}")
            raise

    # 2.查询认证状态接口 测试
    def test_approve_status(self):
        try:
            with allure.step("调取查询认证状态接口"):
                result = self.approve.api_approve_status()
                log.info(f"正在执行查询认证状态接口，执行结果为{result.text}")
            with allure.step("断言成功"):
                assert "华" in result.text
                log.info("执行断言通过")
        except Exception as e:
            log.error(f"断言错误！！！原因：{e}")
            raise

    # 3.后台开户接口 测试
    def test_trust(self):
        try:
            with allure.step("调取后台开户接口测试"):
                result = self.approve.api_trust()
                log.info(f"正在执行查询认证状态接口，执行结果为{result.json()}")
                print(f'请求后台结果：{result.json()}')
            with allure.step("断言"):
                assert "form" in result.text
                log.info("执行断言1111通过")

            # 三方开户
            with allure.step("调取parser_html工具获取html数据"):
                bs_result = parser_html(result)
                log.info(f"正在调取parser_html工具提取html数据，提取结果是：{bs_result}")
            with allure.step("发送三方开户请求"):
                r = self.session.post(url=bs_result[0], data=bs_result[1])
                log.info(f"正在发送三方开户请求，请求方法：'post, 请求url:{bs_result[0]},请求数据：{bs_result[1]}")
            with allure.step("断言三方开户结果"):
                assert "OK" in r.text
                log.info("执行断言2222通过")
        except Exception as e:
            log.error(f"断言错误！！！原因：{e}")
            raise

    # 4.获取图片验证码接口 测试
    @pytest.mark.parametrize('random, expect_code', read_yaml("approve_trust.yaml", "img_code"))
    def test_img_code(self, random, expect_code):
        try:
            with allure.step("调取获取图片验证码接口测试"):
                result = self.approve.api_img_code(random)
                log.info(f"正在执行查询认证状态接口，执行结果为{result.status_code}")
            with allure.step("断言"):
                assert expect_code == result.status_code
                log.info("执行断言通过")
        except Exception as e:
            log.error(f"断言错误！！！原因：{e}")
            raise

    # 5.后台充值接口 测试
    @pytest.mark.parametrize("valicode, expect_text", read_yaml("approve_trust.yaml", "recharge"))
    def test_recharge(self, valicode, expect_text):
        try:
            with allure.step("调用图片验证码"):
            # 调用图片验证码
                self.approve.api_img_code(1231123)

            with allure.step("调用后台充值接口"):
            # 调用接口
                result = self.approve.api_recharge(valicode)
                log.info("接口执行结果为：{}".format(result.json()))
                if valicode == 8888:
                    with allure.step("断言"):
                    # 断言
                        assert "form" in result.text
                        log.info("断言通过！")

                    # 三方充值
                    with allure.step("调取parser_html工具获取html数据"):
                        bs_result = parser_html(result)
                        log.info(f"正在调取parser_html工具提取html数据，提取结果是：{result}")
                    with allure.step("发送三方充值请求"):
                        r = self.session.post(url=bs_result[0], data=bs_result[1])
                        print(f'三方充值结果为:{r.text}')
                        log.info(f"正在发送三方开户请求，请求方法：'post, 请求url:{bs_result[0]},请求数据：{bs_result[1]},请求结果为：{r.text}")
                    with allure.step("断言三方开户结果"):
                        assert expect_text in r.text
                        log.info("执行断言通过")
                else:
                    assert "100" in result.text
                    log.info(f"验证码错误，断言通过！")
        except Exception as e:
            log.error(f"断言错误！！！原因：{e}")
            raise
