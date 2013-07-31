#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.utils
    ~~~~~~~~~~~

    :mod:``xmind.utils`` provide a handy way for internal used by
    xmind, and excepted that function defined here will be useful to
    others.

    :copyright:
    :license:
"""

__author__ = "aiqi@xmind.net <Woody Ai>"

import os
import time
import random
import tempfile
import zipfile

from hashlib import md5
from functools import wraps
from xml.dom.minidom import parse, parseString


temp_dir = tempfile.mkdtemp


def extract(path):
    return zipfile.ZipFile(path, "r")


def compress(path):
    return zipfile.ZipFile(path, "w")

########################             Path             #########################

join_path = os.path.join
split_ext = os.path.splitext


def get_abs_path(path):
    """
        Return the absolute path of file

        If path contained start point then use specified start point
        instead of current working dir by default. And part of file
        path allowed begin with a tilde "~" and replaced by user's
        home dir.
    """

    fp, fn = os.path.split(path)
    if not fp:
        fp = os.getcwd()

    fp = os.path.abspath(os.path.expanduser(fp))

    return join_path(fp, fn)


#########################          Time         ###############################

def get_current_time():
    """Get current time in milliseconds
    """
    return long(round(time.time() * 1000))


def readable_time(timestamp):
    """Convert timestamp to human readable time format
    """
    # Timestamp in milliseconds, convert to seconds
    # Cause Python handle time in seconds
    timestampe_in_seconds = float(timestamp) / 1000
    return time.strftime(
        "%m/%d/%Y %H:%M:%S",
        time.gmtime(timestampe_in_seconds))


##########################           DOM            ###########################

parse_dom = parse
parse_dom_string = parseString
# def create_document():
#     return dom.Document()
#
#
# def create_element(tagName, namespaceURI=None, prefix=None, localName=None):
#     return dom.Element(tagName, namespaceURI, prefix, localName)
#
#
# def load_XML(stream):
#     """
#         Create new Document while occure load XML error
#     """
#     try:
#         return dom.parse(stream)
#     except:
#         return create_document()


##########################           Misc             #########################

def generate_id():
    """Generate unique 26-digit random string
    """
    # md5 current time get 32-digit random string
    timestamp = md5(str(get_current_time())).hexdigest()
    lotter = md5(str(random.random())).hexdigest()  # :)

    id = timestamp[19:] + lotter[:13]

    return id.decode("utf8")


############################        Decorator       ###########################

def prevent(func):
    """
        Decarate func with this to prevent to raise Exception while
        occure error
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return

    return wrapper


def check(attr):
    def decorator(method):
        """
            Decatrate method with this to check whether the object
            has an attribute with the given name.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, attr):
                return method(self, *args, **kwargs)

            return None
        return wrapper
    return decorator


def main():
    pass

if __name__ == '__main__':
    main()
