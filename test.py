from XmindCopilot import xmind
from XmindCopilot.fmt_cvt.md2xmind import MarkDown2Xmind

# md格式的源文件路径
file_path = "E:\\CodeTestFile\\Github-opensource-repo\\XmindCopilotPrj\\XmindCopilot\\test\\SLIP.md"
xmind_path = "E:\\CodeTestFile\\Github-opensource-repo\\XmindCopilotPrj\\XmindCopilot\\test\\md2xmind_SLIP.xmind"
workbook = xmind.load(xmind_path)
rootTopic = workbook.getPrimarySheet().getRootTopic()
markdowntext = open(file_path, 'r', encoding='utf-8').read()

MarkDown2Xmind(rootTopic).convert2xmind(markdowntext)
xmind.save(workbook)