import allure
import pytest
import requests

from api import log
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util import parser_html, read_json


@allure.epic("金融P2P")
@allure.feature("投资模块")
class TestTender:
    # 初始化
    def setup(self):
        with allure.step("创建session对象"):
        # 创建session对象
            self.session = requests.session()
            log.info(f'session对象已创建，sessio: {self.session}')
        with allure.step("实例化ApiTender对象"):
        # 实例化ApiTender对象
            self.tender = ApiTender(self.session)
            log.info("ApiTender对象已创建")
        # 调取登录成功
        with allure.step("调取登录成功象"):
            ApiRegisterLogin(self.session).api_login("15815800001", "test123")

    # 收尾
    def teardown(self):
        # 关闭session
        with allure.step("关闭session"):
            self.session.close()
            log.info("session对象已关闭")

    # 投资接口 测试
    @allure.story("投资接口测试")
    @pytest.mark.parametrize('amount, expect_text', read_json("tender_data.json", "tender"))
    def test_tender(self,amount, expect_text):
        try:
            with allure.step("调取投资接口"):

                result = self.tender.api_tender(amount)
                log.info(f"正在执行投资接口，响应结果为：{result.json()}")
                if amount == 100:
                    with allure.step("断言响应结果"):
                        assert "form" in result.text
                        log.info(f"断言响应成功")

                    # 三方投资

                    with allure.step("使用HTML数据提取工具提取数据"):
                        bs_result = parser_html(result)
                        log.info(f"正在使用工具提取HTML页面数据，返回结果为：{bs_result}")
                    with allure.step("调取三方投资接口"):
                        r = self.session.post(url=bs_result[0], data=bs_result[1])
                        log.info(f'正在调取三方投资接口，请求方法："post"，请求url：{bs_result[0]},请求参数：{bs_result[1]}')

                        assert expect_text in r.text
                        log.info("断言投资成功")

                else:
                    with allure.step("断言投资失败"):
                        assert expect_text in result.text
                        log.info("断言结果成功，金额不能为空")
        except Exception as e:
            log.info(f"断言失败，错误信息是:{e}")
            raise

