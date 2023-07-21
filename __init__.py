#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    XmindCopilot
"""
import sys
import os

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except Warning:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()
    
#注意环境变量 本地路径要排在前边（用修改过的xmind）
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
