#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
from xml.dom import minidom


def gen_xml_demo1():
    xml = minidom.Document()
    root = xml.createElement('root')
    xml.appendChild(root)

    child = xml.createElement('child')
    child.setAttribute('attr', '0')
    root.appendChild(child)

    text = xml.createTextNode('text')
    child.appendChild(text)

    print(xml.toxml())
    print(xml.toprettyxml())

    hello = minidom.parseString('<hello>world</hello>')
    root.appendChild(hello.firstChild)
    xml.writexml(sys.stdout, '', ' '*4, '\n', 'UTF-8')


def gen_xml_demo2():
    impl = minidom.getDOMImplementation()
    xml = impl.createDocument(None, 'employees', None)

    root = xml.documentElement

    employee = xml.createElement('employee')
    root.appendChild(employee)

    name = xml.createElement('name')
    text = xml.createTextNode('devin')
    name.appendChild(text)
    employee.appendChild(name)

    age = xml.createElement('age')
    num = xml.createTextNode('18')
    age.appendChild(num)
    employee.appendChild(age)
    # encoding = 'utf-8' 表示生成的xml的编码格式（ < ?xml version = "1.0" encoding = "utf-8"? > ）
    # xml.writexml(sys.stdout, addindent=' '*4, newl='\n', encoding='utf-8')

    return xml.toxml()


def parse_xml_demo1():
    employees_xml = gen_xml_demo2()
    doc = minidom.parseString(employees_xml)
    root = doc.documentElement
    employees = root.getElementsByTagName('employee')

    for employee in employees:
        print(employee.nodeName)
        print(employee.toxml())
        print(employee.childNodes)

        nameNode = employee.getElementsByTagName("name")[0]
        print(nameNode.childNodes)
        print(nameNode.nodeName + ':' + nameNode.childNodes[0].nodeValue)  # nodeValue是结点的值，只对textNode有效

        ageNode = employee.getElementsByTagName('age')[0]
        print(ageNode.childNodes)
        print(ageNode.nodeName + ':' + ageNode.childNodes[0].data)  # 对应textNode也可以通过.data属性获取其文本内容


def parse_xml_demo2():
    """
    文件对象模型（Document Object Model，简称DOM），是W3C组织推荐的处理可扩展置标语言的标准编程接口。
    一个 DOM 的解析器在解析一个 XML 文档时，一次性读取整个文档，把文档中所有元素保存在内存中的一个树结构里，
    之后你可以利用DOM 提供的不同的函数来读取或修改文档的内容和结构，也可以把修改过的内容写入xml文件。
    """
    domtree = minidom.parse("movies.xml")
    collection = domtree.documentElement
    if collection.hasAttribute("shelf"):
        print("Root element: %s" % collection.getAttribute("shelf"))
    movies = collection.getElementsByTagName("movie")
    for movie in movies:
        print("*****Movie*****")
        if movie.hasAttribute("title"):
            print("Title: %s" % movie.getAttribute("title"))
        type = movie.getElementsByTagName('type')[0]
        print("Type: %s" % type.childNodes[0].data)
        format = movie.getElementsByTagName('format')[0]
        print("Format: %s" % format.childNodes[0].data)
        rating = movie.getElementsByTagName('rating')[0]
        print("Rating: %s" % rating.childNodes[0].data)
        description = movie.getElementsByTagName('description')[0]
        print("Description: %s" % description.childNodes[0].data)


if __name__ == '__main__':
    gen_xml_demo1()
    parse_xml_demo1()
    parse_xml_demo2()
