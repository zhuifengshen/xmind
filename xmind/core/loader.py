#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
xmind.core.loader
"""
from xmind.core.comments import CommentsBookDocument
from xmind.core.styles import StylesBookDocument
from xmind.core.manifest import ManifestBookDocument
from . import const
from .workbook import WorkbookDocument
from .. import utils
import os


class WorkbookLoader(object):
    def __init__(self, path):
        """ Load XMind workbook from given path

        :param path: path to XMind file. If not an existing file, will not raise an exception.

        """
        super(WorkbookLoader, self).__init__()
        self._input_source = utils.get_abs_path(path)

        file_name, ext = utils.split_ext(self._input_source)

        if ext != const.XMIND_EXT:
            raise Exception("The XMind filename is missing the '%s' extension!" % const.XMIND_EXT)

        # Input Stream
        self._content_stream = None
        self._styles_stream = None
        self._comments_stream = None
        self._manifest_stream = None
        
        try:
            with utils.extract(self._input_source) as input_stream:
                for stream in input_stream.namelist():
                    if stream == const.CONTENT_XML:
                        self._content_stream = utils.parse_dom_string(input_stream.read(stream))
                    elif stream == const.STYLES_XML:
                        self._styles_stream = utils.parse_dom_string(input_stream.read(stream))
                    elif stream == const.COMMENTS_XML:
                        self._comments_stream = utils.parse_dom_string(input_stream.read(stream))
                    elif stream == const.MANIFEST_XML:
                        self._manifest_stream = utils.parse_dom_string(input_stream.read(stream))

        except BaseException:
            # FIXME: illegal char in xmind & illegal file name should be distinguished
            pass

    def get_workbook(self, get_refs=True):
        """ Parse XMind file to `WorkbookDocument` object and return
        """
        path = self._input_source
        content = self._content_stream
        styles = self._styles_stream
        comments = self._comments_stream
        manifest = self._manifest_stream
        stylesbook = StylesBookDocument(node=styles, path=path)
        commentsbook = CommentsBookDocument(node=comments, path=path)
        manifestbook = ManifestBookDocument(node=manifest, path=path)
        reference_dir = None
        if get_refs:
            reference_dir = self.get_reference()
        workbook = WorkbookDocument(node=content, path=path,
                                    stylesbook=stylesbook, commentsbook=commentsbook,
                                    manifestbook=manifestbook, reference_dir=reference_dir)

        return workbook

    def get_stylesbook(self):
        """ Parse Xmind styles.xml to `StylesBookDocument` object and return
        """
        content = self._styles_stream
        path = self._input_source

        stylesbook = StylesBookDocument(node=content, path=path)
        return stylesbook

    def get_commentsbook(self):
        content = self._comments_stream
        path = self._input_source

        commentsbook = CommentsBookDocument(node=content, path=path)
        return commentsbook

    def get_manifestbook(self):
        content = self._manifest_stream
        path = self._input_source

        manifestbook = ManifestBookDocument(node=content, path=path)
        return manifestbook

    def get_reference(self, except_revisions=False):
        """
        Get all references in xmind zip file.

        :param except_revisions: whether or not to save `Revisions` content in order ot save space.
        :return: the temp reference directory path
        """
        original_xmind_file = self._input_source
        reference_dir = utils.temp_dir()
        if os.path.isfile(original_xmind_file):
            filename, suffix = utils.split_ext(original_xmind_file)
            if suffix != const.XMIND_EXT:
                raise Exception('XMind filename require a "%s" extension' % const.XMIND_EXT)

            original_zip = utils.extract(original_xmind_file)
            try:
                with original_zip as input_stream:
                    for name in input_stream.namelist():
                        if name in [const.CONTENT_XML, const.STYLES_XML, const.COMMENTS_XML, const.MANIFEST_XML]:
                            continue
                        if const.REVISIONS_DIR in name and except_revisions:
                            continue
                        target_file = utils.get_abs_path(utils.join_path(reference_dir, name))
                        if not os.path.exists(os.path.dirname(target_file)):
                            os.makedirs(os.path.dirname(target_file))
                        with open(target_file, 'xb') as f:
                            f.write(original_zip.read(name))
            except BaseException:
                pass
        return reference_dir
