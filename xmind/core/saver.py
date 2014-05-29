#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.saver
    ~~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "aiqi@xmind.net <Woody Ai>"

import codecs

from . import const
from .. import utils


class WorkbookSaver(object):
    def __init__(self, workbook):
        """ Save `WorkbookDocument` as XMind file.

        :param workbook: `WorkbookDocument` object

        """
        self._workbook = workbook

    def _get_content(self):
        content_path = utils.join_path(utils.temp_dir(), const.CONTENT_XML)

        with codecs.open(content_path, "w", encoding="utf-8") as f:
            self._workbook.output(f)

        return content_path

    def save(self, path=None):
        """
        Save the workbook to the given path. If the path is not given, then
        will save to the path set in workbook.
        """
        path = path or self._workbook.get_path()

        if not path:
            raise Exception("Please specify a filename for the XMind file")

        path = utils.get_abs_path(path)

        file_name, ext = utils.split_ext(path)

        if ext != const.XMIND_EXT:
            raise Exception("XMind filenames require a '%s' extension" % const.XMIND_EXT)

        content = self._get_content()

        f=utils.compress(path)
        f.write(content, const.CONTENT_XML)


def main():
    pass

if __name__ == "__main__":
    main()
