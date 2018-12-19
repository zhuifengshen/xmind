#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
import os
import sys
from testlink.builder import xmind_to_testlink_json_file, xmind_to_testlink_xml_file


"""
A tool to parse xmind file into testlink xml file, which will help
you generate a testlink recognized xml file, then you can import it
into testlink as test suites.

Usage:
 xmind2testcase [path_to_xmind_file] [-json]

Example:
 xmind2testcase /home/devin/testcase.xmind       => output xml
 xmind2testcase /home/devin/testcase.xmind -json => output json
"""


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(name)s  %(levelname)s  [%(module)s - %(funcName)s]: %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')


def get_absolute_path(path):
    """
        Return the absolute path of a file

        If path contains a start point (eg Unix '/') then use the specified start point
        instead of the current working directory. The starting point of the file path is
        allowed to begin with a tilde "~", which will be replaced with the user's home directory.
    """
    fp, fn = os.path.split(path)
    if not fp:
        fp = os.getcwd()
    fp = os.path.abspath(os.path.expanduser(fp))
    return os.path.join(fp, fn)


def main():
    xmind_file = 'doc/xmind_testcase_template.xmind'
    xmind_file_path = get_absolute_path(xmind_file)
    logging.info('Start to convert XMind file: %s', xmind_file_path)

    testlink_xml_file = xmind_to_testlink_xml_file(xmind_file_path)
    logging.info('Convert XMind file to testlink xml file successfully: %s', testlink_xml_file)

    testlink_json_file = xmind_to_testlink_json_file(xmind_file_path)
    logging.info('Convert XMind file to testlink json file successfully: %s', testlink_json_file)


def cli_main():
    if len(sys.argv) > 1 and sys.argv[1].endswith('.xmind'):
        xmind_file = sys.argv[1]
        xmind_file_path = get_absolute_path(xmind_file)
        logging.info('Start to convert XMind file: %s', xmind_file_path)

        if len(sys.argv) == 3 and sys.argv[2] == '-json':
            testlink_json_file = xmind_to_testlink_json_file(xmind_file_path)
            logging.info('Convert XMind file to testlink json file successfully: %s', testlink_json_file)
        else:
            testlink_xml_file = xmind_to_testlink_xml_file(xmind_file_path)
            logging.info('Convert XMind file to testlink xml files successfully: %s', testlink_xml_file)
    else:
        print(__doc__)
        logging.error('%s', __doc__)


if __name__ == '__main__':
    main()
