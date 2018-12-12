#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xmind
from xmind.core.markerref import MarkerId


def update_xmind_correctly():
    workbook = xmind.load('demo.xmind')
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    root_topic.addMarker(MarkerId.smileyLaugh)
    # save_as() save all references in the xmind file（except Revisions content for saving space）
    xmind.save_as(workbook, path='update_demo.xmind')


def update_xmind_by_mistake():
    workbook = xmind.load('demo.xmind')
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    root_topic.addMarker(MarkerId.smileyLaugh)
    # save() only save content.xml（styles and attachments will lost)
    xmind.save(workbook, path='update_demo_by_mistake.xmind')


if __name__ == '__main__':
    # update_xmind_correctly()
    # update_xmind_by_mistake()
    pass
