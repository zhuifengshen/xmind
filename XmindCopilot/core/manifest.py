#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
XmindCopilot.core.manifest implements encapsulation of the XMind META-INF/manifest.xml.
"""
import random

from .. import utils
from . import Document, const, Element


class ManifestBookDocument(Document):
    """ `ManifestBookDocument` as central object correspond XMind manifest file.

    such as:
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0" password-hint="">
        <file-entry full-path="attachments/" media-type=""/>
        <file-entry full-path="attachments/3iaqp5lrttp46abkh5a9dh4bhq.jpeg" media-type="image/jpeg"/>
        <file-entry full-path="content.xml" media-type="text/xml"/>
        <file-entry full-path="META-INF/" media-type=""/>
        <file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>
        <file-entry full-path="meta.xml" media-type="text/xml"/>
        <file-entry full-path="styles.xml" media-type="text/xml"/>
        <file-entry full-path="Thumbnails/" media-type=""/>
        <file-entry full-path="Thumbnails/thumbnail.png" media-type="image/png"/>
    </manifest>
    """

    def __init__(self, node=None, path=None):
        """Construct new `ManifestBookDocument` object

        :param node: pass DOM node object and parse as `ManifestBookDocument` object.
                     if node not given then created new one.
        :param path: set workbook will to be placed.
        """
        super(ManifestBookDocument, self).__init__(node)
        self._path = path

        _manifestbook_element = self.getFirstChildNodeByTagName(const.TAG_MANIFESTBOOK)
        self._manifestbook_element = ManifestBookElement(_manifestbook_element, self)

        if not _manifestbook_element:
            self.appendChild(self._manifestbook_element)

        self.setVersion(const.VERSION)

    def getManifestBookElement(self):
        return self._manifestbook_element

    def getManifest(self):
        return self._manifestbook_element.getManifest()

    def addManifest(self, path, media_type):
        return self._manifestbook_element.addManifest(path, media_type)


class ManifestBookElement(Element):
    """`ManifestBookElement` as the one and only root element of the manifest book document"""
    TAG_NAME = const.TAG_MANIFESTBOOK

    def __init__(self, node=None, ownerManifestBook=None):
        super(ManifestBookElement, self).__init__(node)
        self._owner_manifestbook = ownerManifestBook
        self.registerOwnerManifestBook()
        self.setAttribute(const.NAMESPACE, const.XMLNS_MANIFEST)
        # TODO: password-hint?

    def registerOwnerManifestBook(self):
        if self._owner_manifestbook:
            self.setOwnerDocument(self._owner_manifestbook.getOwnerDocument())

    def getOwnerManifestBook(self):
        return self._owner_manifestbook

    def getManifest(self):
        manifest = self.getChildNodesByTagName(const.TAG_FILE_ENTRY)
        owner_manifestbook = self.getOwnerManifestBook()
        manifest = [ManifestElement(node=manifest, ownerManifestBook=owner_manifestbook) for manifest in manifest]
        return manifest

    def addManifest(self, path, media_type):
        manifest = ManifestElement(node=None, ownerManifestBook=self.getOwnerManifestBook())
        manifest.setPath(path)
        manifest.setMediaType(media_type)
        self.appendChild(manifest)
        return manifest


class ManifestElement(Element):
    """`ManifestElement` as element of the manifest book document"""
    TAG_NAME = const.TAG_FILE_ENTRY

    def __init__(self, node=None, ownerManifestBook=None):
        super(ManifestElement, self).__init__(node)
        self._owner_manifestbook = ownerManifestBook
        self.registerOwnerManifestbook()

    def registerOwnerManifestbook(self):
        if self._owner_manifestbook:
            self.setOwnerDocument(self._owner_manifestbook.getOwnerDocument())

    def setPath(self, path):
        self.setAttribute(const.ATTR_FULL_PATH, path)
    
    def setMediaType(self, media_type):
        self.setAttribute(const.ATTR_MEDIA_TYPE, media_type)
    