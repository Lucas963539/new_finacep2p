import requests

from config import HOST


class ApiTender:
    pass
    # 初始化
    def __init__(self,session):
        # 获取session对象
        self.session = session
        # 投资接口url
        self.__tender = HOST + "/trust/trust/tender"

    # 投资接口封装
    def api_tender(self,amount):
        data = {
            "id": 642,
            "depositCertificate": -1,
            "amount": amount
        }
        return self.session.post(url=self.__tender, data=data)
if __name__ == '__main__':
        session = requests.session()
        tender = ApiTender(session)
        print(tender.api_tender(100).text)