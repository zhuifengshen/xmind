#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import zipfile


def zip_file_demo():
    """
    zip文件格式是通用的文档压缩标准，在ziplib模块中，使用ZipFile类来操作zip文件
    """
    with zipfile.ZipFile(os.path.join(os.getcwd(), 'demo.zip')) as zipFile:
        for file in zipFile.namelist():
            zipInfo = zipFile.getinfo(file)
            print(zipInfo.filename)
            print(zipInfo.date_time)
            print(zipInfo.file_size)
            print(zipInfo.compress_size)
            # if file == const.CONTENT_XML:
            #     zipFile.extract(file)


if __name__ == '__main__':
    zip_file_demo()