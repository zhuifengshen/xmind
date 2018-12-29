#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xmind
from xmind.core.markerref import MarkerId


def update_xmind():
    workbook = xmind.load('demo.xmind')
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    root_topic.addMarker(MarkerId.starRed)

    # 1、save all content and save as xmind_update_demo.xmind(recommended)
    xmind.save(workbook=workbook, path='xmind_update_demo.xmind')

    # 2、only save the content.xml
    xmind.save(workbook=workbook, path='xmind_update_demo1.xmind', only_content=True)

    # 3、only save content.xml、comments.xml、styles.xml
    xmind.save(workbook=workbook, path='xmind_update_demo2.xmind', except_attachments=True)

    # 4、save everything except `Revisions` content to save space(also recommended)
    xmind.save(workbook=workbook, path='xmind_update_demo3.xmind', except_revisions=True)

    # 5、update and overwrite the original file directly.
    xmind.save(workbook)


if __name__ == '__main__':
    update_xmind()
