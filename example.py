#-*- coding: utf-8 -*-
import xmind
from xmind.core import workbook,saver
from xmind.core.topic import TopicElement

w = xmind.load("test.xmind") # load an existing file or create a new workbook if nothing is found

s1=w.getPrimarySheet() # get the first sheet
s1.setTitle("first sheet") # set its title
r1=s1.getRootTopic() # get the root topic of this sheet
r1.setTitle("we don't care of this sheet") # set its title

s2=w.createSheet() # create a new sheet
s2.setTitle("second sheet")
r2=s2.getRootTopic()
r2.setTitle("root node")


t1=TopicElement() # create a new element
t1.setTopicHyperlink(s1.getID()) # set a link from this topic to the first sheet given by s1.getID()
t1.setTitle("redirection to the first sheet") # set its title

t2=TopicElement()
t2.setTitle("second node")
t2.setURLHyperlink("https://xmind.net") # set an hyperlink

t3=TopicElement()
t3.setTitle("third node")
t3.setPlainNotes("notes for this topic") # set notes (F4 in XMind)
t3.setTitle("topic with \n notes")

t4=TopicElement()
t4.setFileHyperlink("logo.jpeg") # set a file hyperlink
t4.setTitle("topic with a file")


# then the topics must be added to the root element

r2.addSubTopic(t1)
r2.addSubTopic(t2)
r2.addSubTopic(t3)
r2.addSubTopic(t4)

topics=r2.getSubTopics() # to loop on the subTopics
for topic in topics:
    topic.addMarker("yes")

w.addSheet(s2) # the second sheet is now added to the workbook
rel=s2.createRelationship(t1.getID(),t2.getID(),"test") # create a relationship
s2.addRelationship(rel) # and add to the sheet

xmind.save(w,"test2.xmind") # and we save