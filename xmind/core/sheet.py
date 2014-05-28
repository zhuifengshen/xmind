#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.sheet
    ~~~~~~~~~~~~~~~~

    :mod:``xmind.core.sheet` command XMind sheets manipulation

    :copytright:
    :license:
"""

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const

from .mixin import WorkbookMixinElement
from .topic import TopicElement
from .title import TitleElement
from .relationship import RelationshipElement, RelationshipsElement


class SheetElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_SHEET

    def __init__(self, node=None, ownerWorkbook=None):
        super(SheetElement, self).__init__(node, ownerWorkbook)

        self.addIdAttribute(const.ATTR_ID)
        self._root_topic = self._get_root_topic()

    def _get_root_topic(self):
        # This method initialize root topic, if not root topic
        # DOM implementation, then create one
        topics = self.getChildNodesByTagName(const.TAG_TOPIC)
        owner_workbook = self.getOwnerWorkbook()
        if len(topics) >= 1:
            root_topic = topics[0]
            root_topic = TopicElement(root_topic, owner_workbook)
        else:
            root_topic = TopicElement(ownerWorkbook=owner_workbook)
            self.appendChild(root_topic)

        return root_topic

    def createRelationship(self, end1, end2, title=None):
        """
        Create a relationship between two different topics and return the
        created rel. Please notice that the created rel will not be added to
        sheet. Call `addRelationship()` to add rel to sheet.

        :param end1:    topic ID
        :param end2:    topic ID
        :param title:   relationship title, default by None

        """
        rel = RelationshipElement(ownerWorkbook=self.getOwnerWorkbook())
        rel.setEnd1ID(end1)
        rel.setEnd2ID(end2)

        if title is not None:
            rel.setTitle(title)

        return rel

    def _getRelationships(self):
        return self.getFirstChildNodeByTagName(const.TAG_RELATIONSHIPS)

    def addRelationship(self, rel):
        """
        Add relationship to sheet
        """
        _rels = self._getRelationships()
        owner_workbook = self.getOwnerWorkbook()

        rels = RelationshipsElement(_rels, owner_workbook)

        if not _rels:
            self.appendChild(rels)

        rels.appendChild(rel)

    def removeRelationship(self, rel):
        """
        Remove a relationship between two different topics
        """
        rels = self._getRelationships()

        if not rels:
            return

        rel = rel.getImplementation()
        rels.removeChild(rel)
        if not rels.hasChildNodes():
            self.getImplementation().removeChild(rels)

        self.updateModifiedTime()

    def getRootTopic(self):
        return self._root_topic

    def _get_title(self):
        return self.getFirstChildNodeByTagName(const.TAG_TITLE)

    # FIXME: convert to getter/setter
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

        self.updateModifiedTime()

    def getParent(self):
        workbook = self.getOwnerWorkbook()
        if workbook:
            parent = self.getParentNode()

            if (parent == workbook.getWorkbookElement().getImplementation()):
                return workbook

    def updateModifiedTime(self):
        super(SheetElement, self).updateModifiedTime()

        workbook = self.getParent()
        if workbook:
            workbook.updateModifiedTime()


def main():
    pass


if __name__ == '__main__':
    main()
