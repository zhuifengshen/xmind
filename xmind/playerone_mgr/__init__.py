#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmind
from xmind.core.topic import TopicElement
from xmind.core.markerref import MarkerId
from search import topic_search
from urllib.parse import unquote
import re
import os
import copy
def topic_info_transfer(topic):
    topics = topic.getSubTopics()
    for t in topics:
        topic_info_transfer(t)
    href = topic.getHyperlink() if topic.getHyperlink() else ""
    match = re.match("file://(.*\.xmind)", href)
    if match and topics:
        f_url = unquote(match.group(1))
        # Convert the url to utf-8
        print("Loading: ", f_url)
        workbook = xmind.load(f_url)
        sheets = workbook.getSheets()
        if not sheets[0].getTitle():
            if os.path.isfile(f_url):
                print("File doesn't exist:"+workbook.get_path())
            else:
                print("Failed to open:"+workbook.get_path())
        else:
            wb_root_topic = sheets[0].getRootTopic()
            if not topic_search(wb_root_topic, "Draft", 1):
                wb_root_topic.addSubTopicbyTitle("Draft")
            Draft_topic = topic_search(wb_root_topic, "Draft", 1)
            for t in topics:
                # IMPORTANT When you add topic to another topic,
                # the topic will be removed from the original topic automatically.
                # You DO NOT have to remove it manually.
                # (Because the topic instance can only have one parent topic)
                Draft_topic.addSubTopic(t)
            for t in Draft_topic.getSubTopics():
                print(t.getTitle())
        xmind.save(workbook)
        
    
