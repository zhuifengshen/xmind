#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.notes
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const

from .mixin import TopicMixinElement


class NotesElement(TopicMixinElement):
    TAG_NAME = const.TAG_NOTES

    def __init__(self, node=None, ownerTopic=None):
        super(NotesElement, self).__init__(node, ownerTopic)

    def getContent(self, format=const.PLAIN_FORMAT_NOTE):
        """ Get notes content

        :parma format:  specified returned content format, plain text
                        by default.
        """

        content = self.getFirstChildNodeByTagName(format)

        if not content:
            return

        if format is const.PLAIN_FORMAT_NOTE:
            content = PlainNotes(node=content, ownerTopic=self.getOwnerTopic())
        else:
            raise Exception("Only support plain text notes right now")

        return content.getTextContent()


class _NoteContentElement(TopicMixinElement):
    def __init__(self, node=None, ownerTopic=None):
        super(_NoteContentElement, self).__init__(node, ownerTopic)

    def getFormat(self):
        return self.getImplementation().tagName


class PlainNotes(_NoteContentElement):
    """ Plain text notes

    :param content: utf8 plain text.
    :param node:    `xml.dom.Element` object`
    :param ownerTopic:  `xmind.core.topic.TopicElement` object

    """

    TAG_NAME = const.PLAIN_FORMAT_NOTE

    def __init__(self, content=None, node=None, ownerTopic=None):
        super(PlainNotes, self).__init__(node, ownerTopic)
        if content is not None:
            self.setTextContent(content)

    def setContent(self, content):
        self.setTextContent(content)


def main():
    pass

if __name__ == '__main__':
    main()
