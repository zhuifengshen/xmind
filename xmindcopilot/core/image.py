#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    xmind.core.image

"""
from . import const
from .mixin import WorkbookMixinElement
from . import utils
import os
import re
import shutil
from PIL.Image import Image
from typing import Optional, Union

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

    def _setImageFile(self, img: Union[Image, str]):
        """
        Set image file

        :param img: image path or Image obj to set.
        """
        
        # Delete origin image file
        if self._getImgAbsPath() and os.path.isfile(self._getImgAbsPath()):
            os.remove(self._getImgAbsPath())

        # Handle Web img
        if re.match("^http[s]{0,1}://.*$", img):
            self.setAttribute(const.ATTR_IMG_SRC, img)
            return
        
        # Set image file
        attach_dir = self.getOwnerWorkbook().get_attachments_path()
        if type(img) == str:
            ext_name = os.path.splitext(img)[1]
        else:
            ext_name = ".png"
        media_type = "image/"+ext_name[1:]
        img_name = utils.generate_id()+ext_name
        save_path = os.path.join(attach_dir, img_name)
        # Copy image file
        if type(img) == str:
            shutil.copy(img, save_path)
        else:
            img.save(save_path, format='png')
        
        # Set xhtml:src Attr
        attr_src = "xap:attachments/"+img_name
        self.setAttribute(const.ATTR_IMG_SRC, attr_src)
        self.getOwnerWorkbook().manifestbook.addManifest("attachments/"+img_name, media_type)
        
        
            
        

    def setImage(self, img: Optional[Union[Image, str]] = None,
                 align=None, height=None, width=None):
        """
        Set the image and its attr

        :param img: image path or Image obj to set. If img is None, original img will be reserved.
        :param align: image align (["top", "bottom", "left", "right"]). if it is None, it will be removed(Defaults to aligning top).
        :param height: image svg:height. If it is None, it will be removed.
        :param width: image svg:width. If it is None, it will be removed.
        """
        if img:
            self._setImageFile(img)
        self._setImgAttribute(align=align, height=height, width=width)
