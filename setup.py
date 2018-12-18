#!/usr/env/bin python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="xmind",
    version="0.1.0",
    author="devin",
    author_email="1324556701@qq.com",
    description="Xmind思维导图创建和解析的一站式解决方案",
    packages=find_packages(),

    install_requires=["openpyxl", "xlrd", "xlutils"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    license="MIT",
    keywords="xmind, mind mapping, 思维导图",
    url="https://github.com/xmindltd/xmind"
)
