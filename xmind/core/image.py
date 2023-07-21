#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    xmind.core.image

"""
from . import const
from .mixin import WorkbookMixinElement
from . import utils
import os
import shutil


class ImageElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_IMAGE

    def __init__(self, node=None, ownerWorkbook=None):
        super(ImageElement, self).__init__(node, ownerWorkbook)

    def _getImgAbsPath(self):
        src = self.getAttribute(const.ATTR_IMG_SRC)
        refdir = self.getOwnerWorkbook().reference_dir
        if src and refdir:
            return os.path.join(refdir, src.split(":")[1])

    def _getImgAttribute(self):
        """
        Get image attributes

        :return: (src, align, height, width)
        """
        align = self.getAttribute(const.ATTR_IMG_ALIGN)
        height = self.getAttribute(const.ATTR_IMG_HEIGHT)
        width = self.getAttribute(const.ATTR_IMG_WIDTH)
        src = self.getAttribute(const.ATTR_IMG_SRC)
        return (src, align, height, width)

    def _setImgAttribute(self, src=None, align=None, height=None, width=None):
        """
        Set image attributes.
        
        :param src: image source (xap:attachments/<img_name>). If src is not None, it WON'T be changed.
        :param align: image align (["top", "bottom", "left", "right"]). if it is None, it will be removed(Defaults to aligning top).
        :param height: image svg:height. If it is None, it will be removed.
        :param width: image svg:width. If it is None, it will be removed.
        """
        if src is not None:
            self.setAttribute(const.ATTR_IMG_SRC, src)
        if align in ["top", "bottom", "left", "right", None]:
            self.setAttribute(const.ATTR_IMG_ALIGN, align)
        self.setAttribute(const.ATTR_IMG_HEIGHT, height)
        self.setAttribute(const.ATTR_IMG_WIDTH, width)

    def _setImageFile(self, img_path: str):
        """
        Set image file

        :param img_path: file path of image to be set
        """
        # Delete origin image file
        if self._getImgAbsPath() and os.path.isfile(self._getImgAbsPath()):
            os.remove(self._getImgAbsPath())

        # Set image file
        attach_dir = self.getOwnerWorkbook().get_attachments_path()
        ext_name = os.path.splitext(img_path)[1]
        media_type = "image/"+ext_name[1:]
        img_name = utils.generate_id()+ext_name
        save_path = os.path.join(attach_dir, img_name)
        # Set xhtml:src Attr
        attr_src = "xap:attachments/"+img_name
        self.setAttribute(const.ATTR_IMG_SRC, attr_src)
        self.getOwnerWorkbook().manifestbook.addManifest("attachments/"+img_name, media_type)
        # Copy image file
        shutil.copy(img_path, save_path)

    def setImage(self, img_path=None, align=None, height=None, width=None):
        """
        Set the image and its attr

        :param img_path: file path of image to be set. If src is not None, it WON'T be changed.
        :param align: image align (["top", "bottom", "left", "right"]). if it is None, it will be removed(Defaults to aligning top).
        :param height: image svg:height. If it is None, it will be removed.
        :param width: image svg:width. If it is None, it will be removed.
        """
        if img_path:
            self._setImageFile(img_path)
        self._setImgAttribute(align=align, height=height, width=width)
