#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import logging
import sys
import xmind
from testlink.builder import xmind_to_testlink_json_file, testsuite_to_testlink_xml_file
from testlink.parser import xmind_to_suite

"""
A tool to parse xmind file into testlink xml file, which will help
you generate a testlink recognized xml file, then you can import it
into testlink as test suites.

Usage:
 xmind2testlink [path_to_xmind_file] [-json]

Example:
 xmind2testlink /home/devin/testcase.xmind       => output xml
 xmind2testlink /home/devin/testcase.xmind -json => output json
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(name)s  %(levelname)s  [%(module)s - %(funcName)s]: %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')


def main():
    xmind_file = 'doc/xmind_testcase_template.xmind'
    workbook = xmind.load(xmind_file)
    xmind_data = workbook.getData()
    logging.debug('xmind data: %s', xmind_data)

    if xmind_data:
        testsuites = xmind_to_suite(xmind_data)

        logging.info('this xmind file contains %d sheet(s) and will generate %d testlink file(s) as follow:',
                     len(testsuites), len(testsuites))
        for testsuite in testsuites:
            logging.debug(json.dumps(testsuite.to_dict(), indent=4, separators=(',', ': ')))
            testlink_xml_file = testsuite_to_testlink_xml_file(testsuite, xmind_file)
            logging.info('Convert testsuite file to testlink xml file successfully: %s', testlink_xml_file)

        testlink_json_file = xmind_to_testlink_json_file(testsuites, xmind_file)
        logging.info('Convert XMind file to testlink json file successfully: %s', testlink_json_file)

    else:
        logging.error('Invalid xmind file: it is empty!')


def cli_main():
    if len(sys.argv) > 1 and sys.argv[1].endswith('.xmind'):
        xmind_file = sys.argv[1]
        workbook = xmind.load(xmind_file)
        xmind_data = workbook.getData()

        if xmind_data:
            testsuites = xmind_to_suite(xmind_data)

            if len(sys.argv) == 3 and sys.argv[2] == '-json':
                testlink_json_file = xmind_to_testlink_json_file(testsuites, xmind_file)
                logging.info('Convert XMind file to testlink json file successfully: %s', testlink_json_file)
            else:
                logging.info('this xmind file contains %d sheet(s) and will generate %d testlink file(s) as follow:',
                             len(testsuites), len(testsuites))
                for testsuite in testsuites:
                    testlink_xml_file = testsuite_to_testlink_xml_file(testsuite, xmind_file)
                    logging.info('Convert testsuite file to testlink xml file successfully: %s', testlink_xml_file)
        else:
            logging.error('Invalid xmind file: it is empty!')
    else:
        print(__doc__)
        logging.error('%s', __doc__)


def gui_main():
    pass


if __name__ == '__main__':
    main()
