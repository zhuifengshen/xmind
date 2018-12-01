# -*- coding: utf-8 -*-
import xmind
from xmind.core.topic import TopicElement

# load an existing file or create a new workbook if nothing is found
workbook_document = xmind.load("test.xmind")

# 新的workbook，默认新建一个空白sheet
sheet1 = workbook_document.getPrimarySheet()  # get the first sheet
sheet1.setTitle("first sheet")  # set its title
# 新的sheet，默认新建一个空白root topic
root_topic1 = sheet1.getRootTopic()  # get the root topic of this sheet
root_topic1.setTitle("we don't care of this sheet")  # set its title
root_topic1.setLabel("I'm a Label")

sheet2 = workbook_document.createSheet()  # create a new sheet
sheet2.setTitle("second sheet")
root_topic2 = sheet2.getRootTopic()
root_topic2.setTitle("root node")


topic1 = TopicElement()  # create a new element
# set a link from this topic to the first sheet given by s1.getID()
topic1.setTopicHyperlink(sheet1.getID())
topic1.setTitle("redirection to the first sheet")  # set its title

topic2 = TopicElement()
topic2.setTitle("second node")
topic2.setURLHyperlink("https://xmind.net")  # set an hyperlink

topic3 = TopicElement()
topic3.setTitle("third node")
topic3.setPlainNotes("notes for this topic")  # set notes (F4 in XMind)
topic3.setTitle("topic with \n notes")

topic4 = TopicElement()
topic4.setFileHyperlink("logo.jpeg")  # set a file hyperlink
topic4.setTitle("topic with a file")


# then the topics must be added to the root element

root_topic2.addSubTopic(topic1)
root_topic2.addSubTopic(topic2)
root_topic2.addSubTopic(topic3)
root_topic2.addSubTopic(topic4)

topics = root_topic2.getSubTopics()  # to loop on the subTopics
# for topic in topics:
#     topic.addMarker("yes")

for index, topic in enumerate(topics):
    topic.addMarker("priority-" + str(index + 1))

workbook_document.addSheet(sheet2)  # the second sheet is now added to the workbook
rel = sheet2.createRelationship(topic1.getID(), topic2.getID(), "test")  # create a relationship
sheet2.addRelationship(rel)  # and add to the sheet

xmind.save(workbook_document)  # and we save
