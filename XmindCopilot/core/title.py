#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    XmindCopilot.core.title

"""
from . import const
from .mixin import WorkbookMixinElement


class TitleElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TITLE

    def __init__(self, node=None, ownerWorkbook=None):
        super(TitleElement, self).__init__(node, ownerWorkbook)
    
    def setSvgWidth(self, width):
        self.setAttribute(const.ATTR_TITLE_SVGWIDTH, width)
