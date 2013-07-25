#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.loader
    ~~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const
from .workbook import WorkbookDocument

from .. import utils


class WorkbookLoader(object):
    def __init__(self, path):
        """ Load XMind workbook from given path

        :param path:    path of XMind, if path is not a exists file,
                        will not occured error.

        """
        super(WorkbookLoader, self).__init__()
        self._input_source = utils.get_abs_path(path)

        file_name, ext = utils.split_ext(self._input_source)

        if ext != const.XMIND_EXT:
            raise Exception("Illegal XMind file")

        # Input Stream
        self._content_stream = None

        try:
            with utils.extract(self._input_source) as input_stream:
                for stream in input_stream.namelist():
                    if stream == const.CONTENT_XML:
                        self._content_stream = utils.parse_dom_string(
                            input_stream.read(stream))
        except:
            pass

    def get_workbook(self):
        """ Parse XMind file to `WorkbookDocument` object and return
        """
        content = self._content_stream
        path = self._input_source

        workbook = WorkbookDocument(content, path)
        return workbook


def main():
    pass

if __name__ == "__main__":
    main()
