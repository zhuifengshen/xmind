
import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


import XmindCopilot
from XmindCopilot.fmt_cvt.md2xmind import MarkDown2Xmind
from XmindCopilot.file_shrink import xmind_shrink
from XmindCopilot.search import topic_search


class TestXmindCopilot(unittest.TestCase):
    def testXmindLoad(self):
        xmind_path = os.path.join(os.path.dirname(__file__), "TestTemplate.xmind")
        workbook = XmindCopilot.load(xmind_path)
        sheets = workbook.getSheets()
        first_sheet = sheets[0]
        root_topic = first_sheet.getRootTopic()
        print(root_topic.getTitle())
        subtopics = root_topic.getSubTopics()
        for topic in subtopics:
            print('  ', topic.getTitle())
        self.assertTrue(True)

class TestSearch(unittest.TestCase):
    def testSearch(self):
        xmind_path = os.path.join(os.path.dirname(__file__), "TestTemplate.xmind")
        workbook = XmindCopilot.load(xmind_path)
        sheets = workbook.getSheets()
        first_sheet = sheets[0]
        root_topic = first_sheet.getRootTopic()
        search_topic = topic_search(root_topic, '常用标记')
        print("\n")
        print(search_topic.getTitle())
        for subtopic in search_topic.getSubTopics():
            print('  ', subtopic.getTitle())
        self.assertTrue(True)

class TestXmindShrink(unittest.TestCase):
    def testXmindShrink(self):
        xmind_path = os.path.join(os.path.dirname(__file__), "TestTemplate.xmind")
        xmind_shrink(xmind_path,
                     PNG_Quality=10, JPEG_Quality=20, use_pngquant=True,
                     replace=False,
                     output_path=os.path.join(os.path.dirname(__file__), "tmp", "TestShrink.xmind"))
        self.assertTrue(True)


class TestXmindFmtConvert(unittest.TestCase):
    def testMarkdown2Xmind(self):
        file_path = os.path.join(os.path.dirname(__file__), "TestTemplate.md")
        xmind_path = os.path.join(os.path.dirname(__file__), "tmp", "TestMd2Xmind.xmind")
        if os.path.isfile(xmind_path):
            os.remove(xmind_path)
        workbook = XmindCopilot.load(xmind_path)
        rootTopic = workbook.getPrimarySheet().getRootTopic()
        markdowntext = open(file_path, 'r', encoding='utf-8').read()
        MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
        XmindCopilot.save(workbook)
        self.assertTrue(True)
    
    def testMarkdownList2Xmind(self):
        file_path = os.path.join(os.path.dirname(__file__), "TestIndentList.md")
        xmind_path = os.path.join(os.path.dirname(__file__), "tmp", "TestMdList2Xmind.xmind")
        if os.path.isfile(xmind_path):
            os.remove(xmind_path)
        workbook = XmindCopilot.load(xmind_path)
        rootTopic = workbook.getPrimarySheet().getRootTopic()
        markdowntext = open(file_path, 'r', encoding='utf-8').read()
        MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
        XmindCopilot.save(workbook)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
    
