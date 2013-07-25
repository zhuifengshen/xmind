#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind
    ~~~~~

    :copyright:
    :license:

"""


__version__ = "0.1a.0"
__author__ = "aiqi@xmind.net <Woody Ai>"

from xmind.core.loader import WorkbookLoader
from xmind.core.saver import WorkbookSaver


def load(path):
    """ Load XMind workbook from given path. If file no
    exist on given path then created new one.

    """
    loader = WorkbookLoader(path)
    return loader.get_workbook()


def save(workbook, path=None):
    """ Save workbook to given path. If path not given, then
    will save to path that set to workbook.

    """
    saver = WorkbookSaver(workbook)
    saver.save(path)


def main():
    pass

if __name__ == '__main__':
    main()
