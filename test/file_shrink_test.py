
import unittest
import os
from XmindCopilot.file_shrink import xmind_shrink


class TestXmindShrink(unittest.TestCase):
    def test_xmind_shrink(self):
        xmind_path = os.path.join(os.path.dirname(__file__), "TestTemplate.xmind")
        xmind_shrink(xmind_path,
                     PNG_Quality=10, JPEG_Quality=20, use_pngquant=True,
                     replace=False,
                     output_path=os.path.join(os.path.dirname(__file__), "tmp", "ShrinkTest.xmind"))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
    
# from XmindCopilot import xmind
# from XmindCopilot.fmt_cvt.md2xmind import MarkDown2Xmind

# # md格式的源文件路径
# file_path = "E:\\CodeTestFile\\Github-opensource-repo\\XmindCopilotPrj\\XmindCopilot\\test\\SLIP.md"
# xmind_path = "E:\\CodeTestFile\\Github-opensource-repo\\XmindCopilotPrj\\XmindCopilot\\test\\md2xmind_SLIP.xmind"
# workbook = xmind.load(xmind_path)
# rootTopic = workbook.getPrimarySheet().getRootTopic()
# markdowntext = open(file_path, 'r', encoding='utf-8').read()

# MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
# xmind.save(workbook)