import os
import unittest

from htmltestreport import HTMLTestReport

from config import DIR_PATH

suite = unittest.defaultTestLoader.discover('./script')

file_path = DIR_PATH + os.sep + "report_unittest" + os.sep + "p2p_api_test.html"
HTMLTestReport(file_path,title="p2p接口测试报告").run(suite)