
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import XmindCopilot
from XmindCopilot.search import topic_search
from XmindCopilot.file_shrink import xmind_shrink
from XmindCopilot.fmt_cvt.latex_render import latex2img
from XmindCopilot.fmt_cvt.md2xmind import MarkDown2Xmind

TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")
TEST_TEMPLATE_XMIND = os.path.join(
    os.path.dirname(__file__), "TestTemplate.xmind")
TEST_TEMPLATE_MD = os.path.join(os.path.dirname(__file__), "TestTemplate.md")
TEST_TEMPLATE_MDList = os.path.join(os.path.dirname(__file__), "TestIndentList.md")


class TestXmindCopilot(unittest.TestCase):
    def testXmindLoad(self):
        xmind_path = TEST_TEMPLATE_XMIND
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
        xmind_path = TEST_TEMPLATE_XMIND
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
        xmind_path = TEST_TEMPLATE_XMIND
        xmind_shrink(xmind_path,
                     PNG_Quality=10, JPEG_Quality=20, use_pngquant=True,
                     replace=False,
                     output_path=os.path.join(TMP_DIR, "TestShrink.xmind"))
        self.assertTrue(True)


class TestXmindFmtConvert(unittest.TestCase):
    def testMarkdown2Xmind(self):
        file_path = TEST_TEMPLATE_MD
        xmind_path = os.path.join(TMP_DIR, "TestMd2Xmind.xmind")
        if os.path.isfile(xmind_path):
            os.remove(xmind_path)
        workbook = XmindCopilot.load(xmind_path)
        rootTopic = workbook.getPrimarySheet().getRootTopic()
        markdowntext = open(file_path, 'r', encoding='utf-8').read()
        rootTopic.addSubTopicbyMarkDown(markdowntext)
        # MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
        XmindCopilot.save(workbook)
        self.assertTrue(True)

    def testMarkdownList2Xmind(self):
        file_path = TEST_TEMPLATE_MDList
        xmind_path = os.path.join(TMP_DIR, "TestMdList2Xmind.xmind")
        if os.path.isfile(xmind_path):
            os.remove(xmind_path)
        workbook = XmindCopilot.load(xmind_path)
        rootTopic = workbook.getPrimarySheet().getRootTopic()
        markdowntext = open(file_path, 'r', encoding='utf-8').read()
        rootTopic.addSubTopicbyMarkDown(markdowntext)
        # MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
        XmindCopilot.save(workbook)
        self.assertTrue(True)

    def testLatexRenderer(self):
        text = r'$\sum_{i=0}^\infty x_i$'
        latex2img(text, size=48, color=(0.1, 0.8, 0.8),
                  out=os.path.join(TMP_DIR, "TestLatex.png"))

        text = r'$\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$'
        im = latex2img(text, size=48, color=(0.9, 0.1, 0.1))
        # im.show()


if __name__ == '__main__':
    unittest.main()
