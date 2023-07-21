import unittest

from XmindFileParser import XmindFileParser


class TestXmindFileParser(unittest.TestCase):

    def test_unzip(self):
        XmindFileParser.parse("测试文件.xmind")

if __name__ == '__main__':
    unittest.main()