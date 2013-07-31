#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.workbook
    ~~~~~~~~~~~~~~~~~~~

    :mod:``xmind.core.workbook`` implements the command XMind
    manipulations.

    :copyright:
    :license:
"""

__author__ = "aiqi@xmind.net <Woody Ai>"


from . import Document
from . import const

from .mixin import WorkbookMixinElement
from .sheet import SheetElement
from .topic import TopicElement
from .relationship import RelationshipElement

from .. import utils


class WorkbookElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_WORKBOOK

    def __init__(self, node=None, ownerWorkbook=None):
        super(WorkbookElement, self).__init__(node, ownerWorkbook)

        # Initialize WorkbookElement with default attribute
        namespace = (const.NAMESPACE, const.XMAP)
        attrs = [const.NS_FO, const.NS_XHTML, const.NS_XLINK, const.NS_SVG]

        for attr in attrs:
            self.setAttributeNS(namespace, attr)

        # Initialize WorkbookElement need contains at least one SheetElement
        if not self.getSheets():
            sheet = self.createSheet()
            self.addSheet(sheet)

    def setOwnerWorkbook(self, workbook):
        raise Exception(
            """WorkbookDocument allowed only contains one WorkbookElement
            """)

    def getSheets(self):
        sheets = self.getChildNodesByTagName(const.TAG_SHEET)
        owner_workbook = self.getOwnerWorkbook()
        sheets = [SheetElement(sheet, owner_workbook) for sheet in sheets]

        return sheets

    def getSheetByIndex(self, index):
        sheets = self.getSheets()

        if index < 0 or index >= len(sheets):
            return

        return sheets[index]

    def createSheet(self):
        sheet = SheetElement(None, self.getOwnerWorkbook())
        return sheet

    def addSheet(self, sheet, index=None):
        sheets = self.getSheets()
        if index < 0 or index >= len(sheets):
            self.appendChild(sheet)
        else:
            self.insertBefore(sheet, sheets[index])

        self.updateModifiedTime()

    def removeSheet(self, sheet):
        sheets = self.getSheets()
        if len(sheets) <= 1:
            return

        if sheet.getParentNode() == self.getImplementation():
            self.removeChild(sheet)
            self.updateModifiedTime()

    def moveSheet(self, original_index, target_index):
        if original_index < 0 or original_index == target_index:
            return

        sheets = self.getSheets()
        if original_index >= len(sheets):
            return

        sheet = sheets[original_index]
        if not target_index < 0 and target_index < len(sheets) - 1:
            if original_index < target_index:
                target_index += 1
            else:
                target_index = target_index

            target = sheets[target_index]
            if target != sheet:
                self.removeChild(sheet)
                self.insertBefore(sheet, target)
        else:
            self.removeChild(sheet)
            self.appendChild(sheet)

        self.updateModifiedTime()

    def getVersion(self):
        return self.getAttribution(const.ATTR_VERSION)


class WorkbookDocument(Document):
    """ `WorkbookDocument` as central object correspond XMind workbook.
    """
    def __init__(self, node=None, path=None):
        """  Construct new `WorkbookDocument` object

        :param node:    pass DOM node object and parse as `WorkbookDocument`
                        object. if node not given then created new one.

        :param path:    set workbook will to be placed.

        """
        super(WorkbookDocument, self).__init__(node)
        self._path = path
        # Initialize WorkbookDocument to make sure that contains
        # WorkbookElement as root.
        _workbook_element = self.getFirstChildNodeByTagName(
            const.TAG_WORKBOOK)

        self._workbook_element = WorkbookElement(
            _workbook_element,
            self)

        if not _workbook_element:
            self.appendChild(self._workbook_element)

        self.setVersion(const.VERSION)

    def getWorkbookElement(self):
        return self._workbook_element

    def _create_relationship(self):
        return RelationshipElement(None, self)

    def createRelationship(self, end1, end2):
        """ Create relationship with two topics. Pass two
        `TopicElement` object and retuen `RelationshipElement` object
        """
        sheet1 = end1.getOwnerSheet()
        sheet2 = end2.getOwnerSheet()

        if sheet1 and sheet2:
            if sheet1.getImplementation() == sheet2.getImplementation():

                rel = self._create_relationship()
                rel.setEnd1ID(end1.getID())
                rel.setEnd2ID(end2.getID())

                sheet1.addRelationships(rel)

                return rel

        raise Exception("Topics not on the same sheet!")

    def createTopic(self):
        """ Creat new `TopicElement` object and return. Please notice that
        this topic haven't been add to workbook.
        """
        return TopicElement(None, self)

    def getSheets(self):
        """ List all sheets under workook, if not sheets then return
        empty list
        """
        return self._workbook_element.getSheets()

    def getPrimarySheet(self):
        """ Get the first sheet under workbook.
        """
        return self._workbook_element.getSheetByIndex(0)

    def createSheet(self):
        """ Create new sheet. But please notice the new created sheet
        hasn't been add to workbook. Invoke :method addSheet: to do that.
        """
        return self._workbook_element.createSheet()

    def addSheet(self, sheet, index=None):
        """ Add sheet to workbook.

        :param sheet:   add passed `SheetElement` object to workbook.

        :param index:   insert sheet before another sheet that given by
                        index. If index not given, append sheet to the
                        sheets list.
        """
        self._workbook_element.addSheet(sheet, index)

    def removeSheet(self, sheet):
        """ Remove sheet from workbook

        :param sheet:   remove passed `SheetElement` object
        """
        self._workbook_element.removeSheet(sheet)

    def moveSheet(self, original_index, target_index):
        """ Move sheet from original index to target index

        :param original_index:  index of the sheet will be moved.
                                `original_index` must be positive integer and
                                less than `target_index`.
        :param target_index:    index that sheet want to move to.
                                `target_index` must be positive integer and
                                less than the length of sheets list.
        """
        self._workbook_element.moveSheet(original_index, target_index)

    def getVersion(self):
        return self._workbook_element.getVersion()

    def getModifiedTime(self):
        return self._workbook_element.getModifiedTime()

    def updateModifiedTime(self):
        return self._workbook_element.updateModifiedTime()

    def setModifiedTime(self):
        return self._workbook_element.setModifiedTime()

    def get_path(self):
        if self._path:
            return utils.get_abs_path(self._path)

    def set_path(self, path):
        self._path = utils.get_abs_path(path)


def main():
    pass

if __name__ == '__main__':
    main()
