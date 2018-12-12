#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    xmind
"""
__version__ = "0.1.0"
from xmind.core.loader import WorkbookLoader
from xmind.core.saver import WorkbookSaver


def load(path):
    """ Load XMind workbook from given path. If file no exist on given path then created new one. """
    loader = WorkbookLoader(path)
    return loader.get_workbook()


def save(workbook, path=None):
    """ Save workbook to given path. If path not given, then will save to path that set to workbook. """
    saver = WorkbookSaver(workbook)
    saver.save(path)


def save_as(workbook, path=None):
    """
        After update a xmind file, save it to the given path with all references in the xmind file except
        Revisions content for saving space. If the path is not given, then will save to the path set in workbook.
    """
    saver = WorkbookSaver(workbook)
    saver.save_as(path)
