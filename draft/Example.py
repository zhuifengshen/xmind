
import xmind
import xmind.core.topic
# 创建XMind文件
def gen_my_xmind_file():  
    # 1、如果指定的XMind文件存在，则加载，否则创建一个新的
    workbook = xmind.load("my.xmind")
    
    # 2、获取第一个画布（Sheet），默认新建一个XMind文件时，自动创建一个空白的画布
    sheet1 = workbook.getPrimarySheet()
    # 对第一个画布进行设计完善，具体参照下一个函数
    design_sheet1(sheet1)
    
    # 3、创建第二个画布
    gen_sheet2(workbook, sheet1)
    
    # 4、保存（如果指定path参数，另存为该文件名）
    xmind.save(workbook, path='test.xmind')

def design_sheet1(sheet1):
    # ***** 第一个画布 *****
    sheet1.setTitle("first sheet")  # 设置画布名称
 
    # 获取画布的中心主题，默认创建画布时会新建一个空白中心主题
    root_topic1 = sheet1.getRootTopic()
    root_topic1.setTitle("root node")  # 设置主题名称
 
    # 创建一个子主题，并设置其名称
    sub_topic1 = root_topic1.addSubTopic()
    sub_topic1.setTitle("first sub topic")
 
    sub_topic2 = root_topic1.addSubTopic()
    sub_topic2.setTitle("second sub topic")
 
    sub_topic3 = root_topic1.addSubTopic()
    sub_topic3.setTitle("third sub topic")
 
    sub_topic4 = root_topic1.addSubTopic()
    sub_topic4.setTitle("fourth sub topic")
 
    # 除了新建子主题，还可以创建自由主题(注意:只有中心主题支持创建自由主题)
    detached_topic1 = root_topic1.addSubTopic(topics_type=TOPIC_DETACHED)
    detached_topic1.setTitle("detached topic")
    detached_topic1.setPosition(0, 30)
 
    # 创建一个子主题的子主题
    sub_topic1_1 = sub_topic1.addSubTopic()
    sub_topic1_1.setTitle("I'm a sub topic too")

def gen_sheet2(workbook, sheet1):
    # ***** 设计第二个画布 *****
    sheet2 = workbook.createSheet()
    sheet2.setTitle("second sheet")
 
    # 获取画布的中心主题
    root_topic2 = sheet2.getRootTopic()
    root_topic2.setTitle("root node")
 
    # 使用另外一种方法创建子主题
    topic1 = TopicElement(ownerWorkbook=workbook)
    # 给子主题添加一个主题间超链接，通过指定目标主题ID即可，这里链接到第一个画布
    topic1.setTopicHyperlink(sheet1.getID())
    topic1.setTitle("redirection to the first sheet")
 
    topic2 = TopicElement(ownerWorkbook=workbook)
    topic2.setTitle("topic with an url hyperlink")
    # 给子主题添加一个URL超链接
    topic2.setURLHyperlink("https://github.com/zhuifengshen/xmind")
 
    topic3 = TopicElement(ownerWorkbook=workbook)
    topic3.setTitle("third node")
    # 给子主题添加一个备注（快捷键F4)
    topic3.setPlainNotes("notes for this topic")
    topic3.setTitle("topic with \n notes")
 
    topic4 = TopicElement(ownerWorkbook=workbook)
    # 给子主题添加一个文件超链接
    topic4.setFileHyperlink("logo.png")
    topic4.setTitle("topic with a file")
 
    topic1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1.setTitle("sub topic")
    # 给子主题添加一个标签（目前XMind软件仅支持添加一个，快捷键）
    topic1_1.addLabel("a label")
 
    topic1_1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1_1.setTitle("topic can add multiple markers")
    # 给子主题添加两个图标
    topic1_1_1.addMarker(MarkerId.starBlue)
    topic1_1_1.addMarker(MarkerId.flagGreen)
 
    topic2_1 = TopicElement(ownerWorkbook=workbook)
    topic2_1.setTitle("topic can add multiple comments")
    # 给子主题添加一个批注（评论）
    topic2_1.addComment("I'm a comment!")
    topic2_1.addComment(content="Hello comment!", author='devin')
 
    # 将创建好的子主题添加到其父主题下
    root_topic2.addSubTopic(topic1)
    root_topic2.addSubTopic(topic2)
    root_topic2.addSubTopic(topic3)
    root_topic2.addSubTopic(topic4)
    topic1.addSubTopic(topic1_1)
    topic2.addSubTopic(topic2_1)
    topic1_1.addSubTopic(topic1_1_1)
 
    # 给中心主题下的每个子主题添加一个优先级图标
    topics = root_topic2.getSubTopics()
    for index, topic in enumerate(topics):
        topic.addMarker("priority-" + str(index + 1))
 
    # 添加一个主题与主题之间的联系
    sheet2.createRelationship(topic1.getID(), topic2.getID(), "relationship test") 

## 解析XMind文件
# 将XMind文件转换为Dict数据 / JSON数据
def XmindDocPrintJson():
    workbook = xmind.load('XmlTest.xmind')
    print(workbook.getData());
    print(workbook.to_prettify_json())

# 将画布转换为Dict数据
def XmindDocPrintDict():
    workbook = xmind.load('demo.xmind')
    sheet = workbook.getPrimarySheet()
    print(sheet.getData())

# 将主题转换为Dict数据
def XmindTopic2Dict():
    workbook = xmind.load('demo.xmind')
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    print(root_topic.getData())
# 自定义解析
def custom_parse_example():
    workbook = xmind.load('demo.xmind')
    custom_parse_xmind(workbook)

def custom_parse_xmind(workbook):
    elements = {}
 
    def _echo(tag, element, indent=0):
        title = element.getTitle()
        elements[element.getID()] = title
        print('\t' * indent, tag, ':', pipes.quote(title))
 
    def dump_sheet(sheet):
        root_topic = sheet.getRootTopic()
        _echo('RootTopic', root_topic, 1)
 
        for topic in root_topic.getSubTopics() or []:
            _echo('AttachedSubTopic', topic, 2)
 
        for topic in root_topic.getSubTopics(xmind.core.const.TOPIC_DETACHED) or []:
            _echo('DetachedSubtopic', topic, 2)
 
        for rel in sheet.getRelationships():
            id1, id2 = rel.getEnd1ID(), rel.getEnd2ID()
            print('Relationship: [%s] --> [%s]' % (elements.get(id1), elements.get(id2)))
 
    for sheet in workbook.getSheets():
        _echo('Sheet', sheet)

# 更新保存XMind文件
def save_example():
    # 加载XMind文件demo.xmind
    workbook = xmind.load('demo.xmind')  
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    # 给中心主题添加一个星星图标
    root_topic.addMarker(MarkerId.starRed)
    
    # 第1种：默认保存所有的内容，这里保存时另存为xmind_update_demo.xmind（推荐）
    xmind.save(workbook=workbook, path='xmind_update_demo.xmind')
    
    # 第2种：只保存思维导图内容content.xml核心文件，适用于没有添加评论、自定义样式和附件的情况
    xmind.save(workbook=workbook, path='xmind_update_demo1.xmind', only_content=True)
    
    # 第3种：只保存content.xml、comments.xml、styles.xml三个核心文件，适用于没有附件的情况
    xmind.save(workbook=workbook, path='xmind_update_demo2.xmind', except_attachments=True)
    
    # 4、除了修改记录，其他内容都保存，因为XMind文件的修改记录文件夹比较大，以便节约内存（推荐）
    xmind.save(workbook=workbook, path='xmind_update_demo3.xmind', except_revisions=True)
    
    # 5、不指定保存路径，直接更新原文件
    xmind.save(workbook)


if __name__ == "__main__":
    # custom_parse_example()
    pass
