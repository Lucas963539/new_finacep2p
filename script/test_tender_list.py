import allure
import requests

from api import log
from api.api_approve_trust import ApiApproveTrust
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util import parser_html


@allure.epic("金融P2P")
@allure.feature("投资业务模块")
class TestTenderList:

    # 初始化
    def setup(self):
        with allure.step("创建session对象"):
        # 创建session对象
            self.session = requests.session()
            log.info(f"正在创建session对象，session：{self.session}")
        with allure.step("实例化ApiTender对象"):
        # 实例化ApiTender对象
            self.tender = ApiTender(self.session)
        with allure.step("实例化ApiApproveTrust对象"):
        # 实例化ApiApproveTrust对象
            self.approve = ApiApproveTrust(self.session)
        with allure.step("实例化ApiRegisterLogin对象"):
        # 实例化ApiRegisterLogin对象
            self.rg = ApiRegisterLogin(self.session)

    # 收尾
    def teardown(self):
        with allure.step("关闭session对象"):
            self.session.close()
            log.info("session对象已关闭")

    @allure.story("投资业务")
    def test_tender_list(self,
                         random=123,
                         phone="18800000001",
                         imgVerifyCode="8888",
                         password="test123",
                         verifycode="8888",
                         phone_code="666666",
                         card_id="431102198906079778",
                         valicode = "8888",
                         amount=100,
                         expect_text="OK"):

        # 1.调取获取图片验证码接口  测试
        with allure.step("1.调取获取图片验证码接口"):
            self.rg.api_get_img_code(random)
            log.info(f'正在调取获取图片验证码接口')

        # 2.调取短信验证码接口 测试
        with allure.step("2.调取短信验证码接口"):
            self.rg.api_get_phone_code(phone,imgVerifyCode)
            log.info(f'正在调取短信验证码接口')

        # 3.调取注册接口 测试
        with allure.step("3.调取注册接口"):
            self.rg.api_register(phone, password, verifycode, phone_code)

        # 4.调取登录接口 测试
        with allure.step("4.调取登录接口"):
            self.rg.api_login(keywords="15815800001",password="test123")

        # 5.调取认证接口
        with allure.step("5.调取认证接口"):
            self.approve.api_approve(card_id)

        # 6.请求后台开户
        with allure.step("6.请求后台开户"):
            trust_result = self.approve.api_trust()

        # 7.三方开户
        with allure.step("调取parser_html工具获取html数据"):
            bs_result = parser_html(trust_result)

            log.info(f"正在调取parser_html工具提取html数据，提取结果是：{bs_result}")
        with allure.step("发送三方开户请求"):
            r = self.session.post(url=bs_result[0], data=bs_result[1])
            print(f"三方开户请求结果为{r.text}")
            log.info(f"正在发送三方开户请求，请求方法：'post, 请求url:{bs_result[0]},请求数据：{bs_result[1]}")
        with allure.step("断言三方开户结果"):
            assert "OK" in r.text
            log.info("执行断言2222通过")

        # 8.获取图片验证码
        with allure.step("8.获取图片验证码"):
            self.approve.api_img_code(random)

        # 9.后台充值成功
        with allure.step("9.后台充值成功"):
            recharge_result = self.approve.api_recharge(valicode)
        # 10.三方充值
        if valicode == 8888:
            with allure.step("断言"):
                # 断言
                assert "form" in recharge_result.text
                log.info("断言通过！")

            # 三方充值
            with allure.step("调取parser_html工具获取html数据"):
                bs_result = parser_html(recharge_result)
                log.info(f"正在调取parser_html工具提取html数据，提取结果是：{recharge_result}")
            with allure.step("10.发送三方充值请求"):
                r = self.session.post(url=bs_result[0], data=bs_result[1])
                log.info(f"正在发送三方开户请求，请求方法：'post, 请求url:{bs_result[0]},请求数据：{bs_result[1]},请求结果为：{r.text}")
            with allure.step("断言三方开户结果"):
                assert "OK" in r.text
                log.info("执行断言通过")
        else:
            assert "100" in recharge_result.text
            log.info(f"验证码错误，断言通过！")
        # 11.请求后台投资接口
        with allure.step("11.请求后台投资接口"):
            tender_result = self.tender.api_tender(amount)
        # 12.三方投资
        if amount == 100:
            with allure.step("断言响应结果"):
                assert "form" in tender_result.text
                log.info(f"断言响应成功")

            # 三方投资
            with allure.step("使用HTML数据提取工具提取数据"):
                bs_result = parser_html(tender_result)
                log.info(f"正在使用工具提取HTML页面数据，返回结果为：{bs_result}")
            with allure.step("调取三方投资接口"):
                r = self.session.post(url=bs_result[0], data=bs_result[1])
                log.info(f'12.正在调取三方投资接口，请求方法："post"，请求url：{bs_result[0]},请求参数：{bs_result[1]}')

                assert expect_text in r.text
                log.info("断言投资成功")
        else:
            with allure.step("断言投资失败"):
                assert "金额不能为空" in tender_result.text
                log.info("断言结果成功，金额不能为空")
