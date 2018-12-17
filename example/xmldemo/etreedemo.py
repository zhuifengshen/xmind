#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from xml.etree import ElementTree

index_html = """
<html>
    <head>
        <title>Example page</title>
    </head>
    <body>
        <p>Moved to <a href="http://example.org/">example.org</a>
        or <a href="http://example.com/">example.com</a>.</p>
    </body>
</html>
"""

tree = ElementTree.fromstring(index_html)
print(tree)
p = tree.find('body/p')
print(p)
for a in p:  # 遍历子元素 or links = list(p.iter('a'))
    print(a)
