#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
import sys
from testcase.testlink import xmind_to_testlink_json_file, xmind_to_testlink_xml_file
from testcase.utils import get_absolute_path
from testcase.zentao import xmind_to_zentao_csv_file

"""
A tool to parse xmind file into testcase file, which will help you 
generate a testlink recognized xml file or a zentao recognized cvs file, 
then you can import it into testlink as test suites or zentao as testcases.

Usage:
 xmind2testcase [path_to_xmind_file] [-csv] [-xml] 

Example:
 xmind2testcase /path/to/testcase.xmind       => output testcase.csv、testcase.xml
 xmind2testcase /path/to/testcase.xmind -csv  => output testcase.csv
 xmind2testcase /path/to/testcase.xmind -xml  => output testcase.xml 
"""


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(name)s  %(levelname)s  [%(module)s - %(funcName)s]: %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')


def main():
    xmind_file = 'doc/xmind_testcase_template.xmind'
    xmind_file_path = get_absolute_path(xmind_file)
    logging.info('Start to convert XMind file: %s', xmind_file_path)

    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    logging.info('Convert XMind file to zentao csv file successfully: %s', zentao_csv_file)

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
        elif len(sys.argv) == 3 and sys.argv[2] == '-xml':
            testlink_xml_file = xmind_to_testlink_xml_file(xmind_file_path)
            logging.info('Convert XMind file to testlink xml files successfully: %s', testlink_xml_file)
        elif len(sys.argv) == 3 and sys.argv[2] == '-csv':
            zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
            logging.info('Convert XMind file to zentao csv file successfully: %s', zentao_csv_file)
        else:
            testlink_json_file = xmind_to_testlink_json_file(xmind_file_path)
            testlink_xml_file = xmind_to_testlink_xml_file(xmind_file_path)
            zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
            logging.info('Convert XMind file successfully: \n'
                         '1、 testlink json file(%s)\n'
                         '2、 testlink xml file(%s)\n'
                         '3、 zentao csv file(%s)',
                         testlink_json_file,
                         testlink_xml_file,
                         zentao_csv_file)
    else:
        print(__doc__)
        logging.error('%s', __doc__)


if __name__ == '__main__':
    main()
