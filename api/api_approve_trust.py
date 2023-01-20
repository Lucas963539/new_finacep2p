# 认证和注册接口封装
import requests

from api import log
from config import HOST

"""
    本期难点：
        请求接口的参数类型为：multipart/form-data 多消息类型，如何实现请求？？？？
        解决方法：
            请求使用data+files两种参数格式，消息头会自动切换multipart即可
        示例：
            return self.session.post(url=self.__url_approve, data=data, files={"x":"y"})
"""
class ApiApproveTrust:

    # 初始化
    def __init__(self,session):
        # 获取session对象
        self.session = session
        # 登录接口
        self.__url_login = HOST + "/member/public/login"
        # 认证接口 url
        self.__url_approve = HOST + "/member/realname/approverealname"
        # 查询认真状态 url
        self.__url_approve_status = HOST + "/member/member/getapprove"
        # 后台开户接口 url
        self.__url_trust = HOST + "/trust/trust/register"
        # 获取图片验证码接口 url
        self.__url_img_code = HOST + "/common/public/verifycode/{}"
        # 充值接口 url
        self.__url_recharge = HOST + "/trust/trust/recharge"


    # 1.认证接口 封装
    def api_approve(self,card_id="350102199003072237"):
        # 请求参数
        data = {
            "realname":"华仔",
            "card_id":card_id
        }
        # 调用认证请求方法
        # # 难题：multipart/form-data 需要添加参数 files={"x":"y"} 其中x是需要用到的参数名，y是open('./xxx'),这里只做占位用就写作{"x":"y"}
        log.info(f'正在调取认证接口，请求方法："post", 请求url：{self.__url_approve},请求参数：{data}')

        return self.session.post(url=self.__url_approve, data=data, files={"x":"y"})

    # 2.查询认证状态接口 封装
    def api_approve_status(self):
        log.info(f'正在调取认证状态接口，请求方法："post", 请求url：{self.__url_approve_status}')
        return self.session.post(url=self.__url_approve_status)

    # 3.后台开户接口 封装
    def api_trust(self):
        log.info(f'正在调取后台开户接口，请求方法："post", 请求url：{self.__url_trust}')
        return self.session.post(url=self.__url_trust)

    # 4.获取图片验证码接口 封装
    def api_img_code(self, random):
        log.info(f'正在调取获取图片验证码接口，请求方法："get", 请求url：{self.__url_img_code.format(random)}')
        return self.session.get(url=self.__url_img_code.format(random))

    # 5.后台充值接口 封装
    def api_recharge(self, valicode):
        # 请求参数
        data = {
            "paymentType": "chinapnrTrust",
            "amount": "1000",
            "formStr": "reForm",
            "valicode": valicode
        }
        headers = {"X-Requested-With":"XMLHttpRequest"}  # 请求头需要加上不然测试该接口时会有问题
        # 调用认证请求方法
        log.info(f'正在调取后台充值接口，请求方法："post", 请求url：{self.__url_recharge},请求参数data:{data},请求头headers：{headers}')
        return self.session.post(url=self.__url_recharge, data=data,headers=headers)

if __name__ == '__main__':
    session = requests.session()
    approve = ApiApproveTrust(session)
    approve.api_img_code(123)
    result = approve.api_recharge("8888")
    print("请求后台充值结果为：{}".format(result.json()))
    re_html = result.json()
    print(re_html)