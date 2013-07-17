#!/usr/bin/env python

"""
    xmind.core.topic
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "woody@xmind.net <Woody Ai>"

from . import const
# from . import Element

from .mixin import WorkbookMixinElement, TopicMixinElement
from .title import TitleElement
from .position import PositionElement

from .. import utils


class TopicElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TOPIC

    def __init__(self, node=None, ownerWorkbook=None):
        super(TopicElement, self).__init__(node, ownerWorkbook)

        self.addIdAttribute(const.ATTR_ID)

    def _get_title(self):
        return self.getFirstChildNodeByTagName(const.TAG_TITLE)

    def _get_position(self):
        return self.getFirstChildNodeByTagName(const.TAG_POSITION)

    def _get_children(self):
        return self.getFirstChildNodeByTagName(const.TAG_CHILDREN)

    def _set_hyperlink(self, hyperlink):
        self.setAttribute(const.ATTR_HREF, hyperlink)
        #self.updateModifiedTime()

    def getID(self):
        return self.getAttribute(const.ATTR_ID)

    def getTitle(self):
        title = self._get_title()
        if title:
            title = TitleElement(title, self.getOwnerWorkbook())
            return title.getTextContent()

    def setTitle(self, text):
        _title = self._get_title()
        title = TitleElement(_title, self.getOwnerWorkbook())
        title.setTextContent(text)

        if _title is None:
            self.appendChild(title)

        # self.updateModifiedTime()

    def setFolded(self):
        self.setAttribute(const.ATTR_BRANCH, const.VAL_FOLDED)

        # self.updateModifiedTime()

    def getPosition(self):
        """ Get a pair of integer located topic position.

        return (x, y) indicate x and y
        """
        position = self._get_position()
        if position is None:
            return

        position = PositionElement(position, self.getOwnerWorkbook())

        x = position.getX()
        y = position.getY()

        if x is None and y is None:
            return

        x = x or 0
        y = y or 0

        return (int(x), int(y))

    def setPosition(self, x, y):
        ownerWorkbook = self.getOwnerWorkbook()
        position = self._get_position()

        if not position:
            position = PositionElement(ownerWorkbook=ownerWorkbook)
            self.appendChild(position)
        else:
            position = PositionElement(position, ownerWorkbook)

        position.setX(x)
        position.setY(y)

        # self.updateModifiedTime()

    def removePosition(self):
        position = self._get_position()
        if position is not None:
            self.getImplementation().removeChild(position)

        # self.updateModifiedTime()

    def getType(self):
        parent = self.getParentNode()
        if not parent:
            return

        if parent.tagName == const.TAG_SHEET:
            return const.TOPIC_ROOT

        if parent.tagName == const.TAG_TOPICS:
            topics = TopicsElement(parent, self.getOwnerWorkbook())
            return topics.getType()

    def getTopics(self, topics_type=const.TOPIC_ATTACHED):
        topic_children = self._get_children()

        if topic_children:
            topic_children = ChildrenElement(
                topic_children,
                self.getOwnerWorkbook())

            return topic_children.getTopics(topics_type)

    def getSubTopics(self, topics_type=const.TOPIC_ATTACHED):
        """ List all sub topics under current topic, If not sub topics,
        return None.
        """
        topics = self.getTopics(topics_type)
        if not topics:
            return

        return topics.getSubTopics()

    def getSubTopicByIndex(self, index, topics_type=const.TOPIC_ATTACHED):
        """ Get sub topic by speicifeid index
        """
        sub_topics = self.getSubTopics(topics_type)
        if sub_topics is None:
            return

        if index < 0 or index >= len(sub_topics):
            return sub_topics

        return sub_topics[index]

    def addSubTopic(self, topic, index=-1,
                    topics_type=const.TOPIC_ATTACHED):
        """ Add sub topic to current topic.

        :param topic:   passed `TopicElement` object.
        :param index:   if index not given then passed topic will append to
                        sub topics list. Otherwise, index must be less than
                        length of sub topics list and insert passed topic
                        before given index.
        """
        ownerWorkbook = self.getOwnerWorkbook()
        topic = topic or self.__class__(ownerWorkbook=ownerWorkbook)

        topic_children = self._get_children()
        if not topic_children:
            topic_children = ChildrenElement(ownerWorkbook=ownerWorkbook)
            self.appendChild(topic_children)
        else:
            topic_children = ChildrenElement(topic_children, ownerWorkbook)

        topics = topic_children.getTopics(topics_type)
        if not topics:
            topics = TopicsElement(ownerWorkbook=ownerWorkbook)
            topics.setAttribute(const.ATTR_TYPE, topics_type)
            topic_children.appendChild(topics)

        topic_list = []
        for i in topics.getChildNodesByTagName(const.TAG_TOPIC):
            topic_list.append(TopicElement(i, ownerWorkbook))

        if index < 0 or len(topic_list) >= index:
            topics.appendChild(topic)
        else:
            topics.insertBefore(topic, topic_list[index])

    def getIndex(self):
        parent = self.getParentNode()
        if parent and parent.tagName == const.TAG_TOPICS:
            index = 0
            for child in parent.childNodes:
                if self.getImplementation() == child:
                    return index
                index += 1
        return -1

    def getHyperlink(self):
        return self.getAttribute(const.ATTR_HREF)

    def setFileHyperlink(self, path):
        """ Set file as topic hyperlink

        :param path: path of specified file

        """
        protocol, content = split_hyperlink(path)
        if not protocol:
            path = const.FILE_PROTOCOL + utils.get_abs_path(path)

        self._set_hyperlink(path)

    def setTopicHyperlink(self, tid):
        """ Set topic as topic hyperlink

        :param id: given topic's id

        """
        protocol, content = split_hyperlink(tid)
        if not protocol:
            if tid.startswith("#"):
                tid = tid[1:]

            tid = const.TOPIC_PROTOCOL + tid
        self._set_hyperlink(tid)

    def setURLHyperlink(self, url):
        """ Set URL as topic hyperlink

        :param url: HTTP URL to specified website

        """
        protocol, content = split_hyperlink(url)
        if not protocol:
            url = const.HTTP_PROTOCOL + content

        self._set_hyperlink(url)

    def getNotes(self):
        notes = self.getFirstChildNodeByTagName(const.TAG_NOTES)
        if notes:
            return NotesElement(notes, self)

    def setNotes(self, content):
        """ Set notes to topic. Please notice that only support plain txt
        format right now.

        :param content: sub-object of `NotesContent`. Only support palin txt
                        format and accept pass `PlainNotesContent` object

            from xmind.core.topic.import PlainNotesContent, TopicElement

            topic = TopicElement()
            plain_content = PlainNotesContent()
            plain_content.setContent("Test plain note")

            topic.setNotes(plain_content)
        """
        notes = self.getNotes()
        if notes is None:
            notes = NotesElement(None, self)
            notes.setContent(content)
            self.appendChild(notes)
        else:
            notes.setContent(content)


class ChildrenElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_CHILDREN

    def __init__(self, node=None, ownerWorkbook=None):
        super(ChildrenElement, self).__init__(node, ownerWorkbook)

    def getTopics(self, topics_type):
        topics = self.iterChildNodesByTagName(const.TAG_TOPICS)
        for i in topics:
            t = TopicsElement(i, self.getOwnerWorkbook())
            if topics_type == t.getType():
                return t


class TopicsElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TOPICS

    def __init__(self, node=None, ownerWorkbook=None):
        super(TopicsElement, self).__init__(node, ownerWorkbook)

    def getType(self):
        return self.getAttribute(const.ATTR_TYPE)

    def getSubTopics(self):
        """List all sub topics on current topic
        """
        topics = []
        ownerWorkbook = self.getOwnerWorkbook()
        for t in self.getChildNodesByTagName(const.TAG_TOPIC):
            topics.append(TopicElement(t, ownerWorkbook))

        return topics

    def getSubTopicByIndex(self, index):
        """Get specified sub topic by index
        """
        sub_topics = self.getSubTopics()
        if index < 0 or index >= len(sub_topics):
            return sub_topics

        return sub_topics[index]


class NotesElement(TopicMixinElement):
    TAG_NAME = const.TAG_NOTES

    def __init__(self, node, owner_topic):
        super(NotesElement, self).__init__(node, owner_topic)

    def getParent(self):
        return self.getOwnerTopic()

    def getContent(self, format=const.PLAIN_FORMAT_NOTE):
        """Get note content in specified format, plain text in default
        """
        content = self.getFirstChildNodeByTagName(format)
        if content is None:
            return

        ownerWorkbook = self.getOwnerWorkbook()
        return NotesContentElement(content, ownerWorkbook)

    def setContent(self, content):
        """ Set note content in specified format
        """
        content_format = content.getFormat()
        if not content_format:
            return

        default_format = (const.HTML_FORMAT_NOTE, const.PLAIN_FORMAT_NOTE)
        if content_format not in default_format:
            return

        for format in default_format:
            old_content = self.getContent(format)
            if old_content is not None:
                self.removeChild(old_content)

        self.appendChild(content)
        # self.updateModifiedTime()


class NotesContentElement(WorkbookMixinElement):
    def __init__(self, node=None, ownerWorkbook=None):
        super(NotesContentElement, self).__init__(node, ownerWorkbook)

    def getFormat(self):
        return self.getImplementation().tagName


class PlainNotesContent(NotesContentElement):
    TAG_NAME = const.PLAIN_FORMAT_NOTE

    def __init__(self, content=None, node=None, ownerWorkbook=None):
        super(PlainNotesContent, self).__init__(node, ownerWorkbook)
        if content is not None:
            self.setTextContent(content)

    def setContent(self, content):
        self.setTextContent(content)


def split_hyperlink(hyperlink):
    colon = hyperlink.find(":")
    if colon < 0:
        protocol = None
    else:
        protocol = hyperlink[:colon]

    hyperlink = hyperlink[colon + 1:]
    while hyperlink.startswith("/"):
        hyperlink = hyperlink[1:]

    return (protocol, hyperlink)


def main():
    pass

if __name__ == '__main__':
    main()
