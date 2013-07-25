#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.const
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:
"""

__author__ = "aiqi@xmind.net <Woody Ai>"

XMIND_EXT = ".xmind"

VERSION = "2.0"
NAMESPACE = "xmlns"
XMAP = "urn:xmind:xmap:xmlns:content:2.0"

ATTACHMENTS_DIR = "attachments/"
MARKERS_DIR = "markers/"
META_INF_DIR = "META-INF/"
REVISIONS_DIR = "Revisions/"

CONTENT_XML = "content.xml"
STYLES_XML = "styles.xml"
META_XML = "meta.xml"
MANIFEST_XML = "META-INF/manifest.xml"
MARKER_SHEET_XML = "markerSheet.xml"
MARKER_SHEET = MARKERS_DIR + MARKER_SHEET_XML
REVISIONS_XML = "revisions.xml"

TAG_WORKBOOK = "xmap-content"
TAG_TOPIC = "topic"
TAG_TOPICS = "topics"
TAG_SHEET = "sheet"
TAG_TITLE = "title"
TAG_POSITION = "position"
TAG_CHILDREN = "children"
TAG_NOTES = "notes"
TAG_RELATIONSHIP = "relationship"
TAG_RELATIONSHIPS = "relationships"

ATTR_VERSION = "version"
ATTR_ID = "id"
ATTR_STYLE_ID = "style-id"
ATTR_TIMESTAMP = "timestamp"
ATTR_THEME = "theme"
ATTR_X = "svg:x"
ATTR_Y = "svg:y"
ATTR_HREF = "xlink:href"
ATTR_BRANCH = "branch"
ATTR_TYPE = "type"
ATTR_END1 = "end1"
ATTR_END2 = "end2"

NS_URI = "http://www.w3.org/1999/xhtml"

NS_XHTML = (NS_URI, "xhtml", "http://www.w3.org/1999/xhtml")
NS_XLINK = (NS_URI, "xlink", "http://www.w3.org/1999/xlink")
NS_SVG = (NS_URI, "svg", "http://www.w3.org/2000/svg")
NS_FO = (NS_URI, "fo", "http://www.w3.org/1999/XSL/Format")

VAL_FOLDED = "folded"

TOPIC_ROOT = "root"
TOPIC_ATTACHED = "attached"

FILE_PROTOCOL = "file://"
TOPIC_PROTOCOL = "xmind:#"
HTTP_PROTOCOL = "http://"
HTTPS_PROTOCOL = "https://"

HTML_FORMAT_NOTE = "html"
PLAIN_FORMAT_NOTE = "plain"
