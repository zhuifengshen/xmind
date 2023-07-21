import json
from zipfile import ZipFile


class XmindFileParser:
    content_json = "content.json"
    xmindFileContent = [content_json]
    markdown_file_content = ""

    @classmethod
    def parse(self, file_path):
        file_content = self.__unzip(self, file_path)
        file_json_content = self.__parse_json(file_content)
        self.__parse_children(self, file_json_content)
        self.__generat_file(self)

    def __unzip(self, file_path):
        with ZipFile(file_path) as xmind_file:
            for f in xmind_file.namelist():
                for key in self.xmindFileContent:
                    if f == key:
                        with xmind_file.open(f) as contentJsonFile:
                            return contentJsonFile.read().decode('utf-8')

    def __parse_json(file_content):
        return json.loads(file_content)

    def __parse_children(self, json_content):
        root_topic = json_content[0]["rootTopic"]
        cur_node = root_topic
        self.__parse_node(self, cur_node, "#")

    '''
    递归解析 children 节点
    '''

    def __parse_node(self, node, level):
        self.markdown_file_content = self.markdown_file_content + "\n" + level + " " + node["title"] + "\n"
        if "notes" in node:
            # TODO 内容 "\n" 需要替换为 "  \n"
            content = node["notes"]["plain"]["content"]
            self.markdown_file_content = self.markdown_file_content + "\n" + node["notes"]["plain"]["content"] + "\n"
        if "children" in node:
            for cur_node in node["children"]["attached"]:
                self.__parse_node(self, cur_node, level + "#")

    def __generat_file(self):
        file = open('个人学习.md', 'w', encoding="utf-8")
        file.write("[TOC]\n\n" + self.markdown_file_content)
        file.close()
