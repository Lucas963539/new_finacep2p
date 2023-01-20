from flask import Flask,request

app = Flask(__name__)

"""
需求：用户名为admin，密码为123456，返回登录成功，否则返回用户名密码错误，请求参数格式：form
"""
# 定义接口，模拟返回结果
@app.route('/login', methods=['post'])
def login():
    # 提取数据
    username = request.form.get('username')
    pwd = request.form.get('password')

    # 判断
    if username == 'admin' and pwd == '123456':
        return {"status": 200, "msg": "登录成功！", "token": "XXXXXX123123123"}
    else:
        return {"status": 100, "msg": "用户名密码错误！"}
    # 如果需要指定返回状态码是333
    # return "custom_status_code", 305, {"status": 200, "msg": "success", "token": "XXXXXX123123123"}


# # 定义接口，模拟异常响应状态码
@app.route('/login/error', methods=['post', 'get'])
def error():

     # 如果需要指定返回状态码是305有以下两种方式：
     # 1. 响应体、状态码、响应头，但注意，有响应头，必须要有状态码
     #return "custom_status_code", 305, [("Itcast","python123"),("city","shenzhen")]

     # 2."状态码+空格+描述信息"
    return "custom_status_code", "305 test"

if __name__ == '__main__':
    app.run()
