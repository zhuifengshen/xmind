#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    xmind.core.saver
"""
import codecs
import os

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
        # encoding specifies the encoding which is to be used for the file.
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
            raise Exception("XMind filename require a '%s' extension" % const.XMIND_EXT)

        content = self._get_content()

        f = utils.compress(path)
        f.write(content, const.CONTENT_XML)

    @staticmethod
    def _get_reference(original_path):
        """
        Get all references in xmind zip file except Revisions content.
        """
        reference_dir = utils.temp_dir()

        filename, suffix = utils.split_ext(original_path)
        if suffix != const.XMIND_EXT:
            raise Exception('XMind filename require a "%s" extension' % const.XMIND_EXT)

        original_zip = utils.extract(original_path)
        try:
            with original_zip as input_stream:
                for name in input_stream.namelist():
                    if name == const.CONTENT_XML:
                        continue
                    if const.REVISIONS_DIR in name:
                        continue
                    target_file = utils.get_abs_path(utils.join_path(reference_dir, name))
                    if not os.path.exists(os.path.dirname(target_file)):
                        os.makedirs(os.path.dirname(target_file))
                    with open(target_file, 'xb') as f:
                        f.write(original_zip.read(name))
        except BaseException:
            pass

        return reference_dir

    def save_as(self, path=None):
        """
            After update a xmind file, save it to the given path with all references in the xmind file except
            Revisions content for saving space. If the path is not given, then will save to the path set in workbook.
        """
        original_path = self._workbook.get_path()
        new_path = path or self._workbook.get_path()
        if not new_path:
            raise Exception('Please specify a filename for the XMind file')

        original_path = utils.get_abs_path(original_path)
        original_filename, original_suffix = utils.split_ext(original_path)
        if original_suffix != const.XMIND_EXT:
            raise Exception('XMind filename require a "%s" extension' % const.XMIND_EXT)

        new_path = utils.get_abs_path(new_path)
        new_filename, new_suffix = utils.split_ext(new_path)
        if new_suffix != const.XMIND_EXT:
            raise Exception('XMind filename require a "%s" extension' % const.XMIND_EXT)

        content = self._get_content()
        reference_dir = self._get_reference(original_path)

        f = utils.compress(new_path)
        f.write(content, const.CONTENT_XML)
        length = reference_dir.__len__()
        for dirpath, dirnames, filenames in os.walk(reference_dir):
            for filename in filenames:
                f.write(utils.join_path(dirpath, filename), utils.join_path(dirpath[length+1:]+os.sep, filename))
        f.close()
