# 1.导包
from bs4 import BeautifulSoup

html = """
    <html>
        <head>
            <title>BeautifulSoup库使用示例</title>
        </head>
        <body>
            <p id="test01">软件测试01</p>
            <p id="test02">2023年</p>
            <a name="api" href="./api.html">接口测试</a>
            <a name="web" href="./web.html">web测试</a>
            <a name="app" href="./app.html">app测试</a>
        </body>
    </html>
"""
# 2.实例化BeautifulSoup对象 html.parser 表示告诉Python解释器你要解析的是html格式
beautiful_soup = BeautifulSoup(html,"html.parser")
# 3.调用方法，
"""重要：
        1.获取所有标签，
            beautiful_soup.find_all("标签名")--->[元素1，元素2.....]--->[<a href="./api.html">接口测试</a>, <a href="./web.html">web测试</a>]
        2.查找属性 元素.get(属性名）
        
"""
ele_list = beautiful_soup.find_all("a")

for a_big in ele_list:
    data = {}
    data[a_big.get('name')] = a_big.get('href')
    herf = a_big.get('href')
    print(f'结果是：{(herf,data)}')



# 4.拓展其他用法
# 获取单个元素 ----> beautiful_soup.标签名
print(f'获取单个元素 :{beautiful_soup.a}')
# 获取文本
print(f'获取标签文本：{beautiful_soup.a.string}')
# 获取属性
print(f'获取标签属性：{beautiful_soup.a.get("href")}')