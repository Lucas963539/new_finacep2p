import os

import pytest

if __name__ == '__main__':
    # 生成测试结果数据
    pytest.main()

    # 运行测试数据，生成到测试报告
    os.system("allure generate ./temp -o ./result --clean")