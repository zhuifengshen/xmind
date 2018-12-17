#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
from io import BytesIO
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, ElementTree, Comment
from xml.sax.saxutils import escape
from testlink import const
from testlink.parser import config


def xmind_to_testlink_json_file(testsuites, xmind_file_path):
    """Convert XMind file to a testlink json file"""
    testcases = []

    for testsuite in testsuites:
        product = testsuite.name
        for suite in testsuite.sub_suites:
            for case in suite.testcase_list:
                case_data = case.to_dict()
                case_data['product'] = product
                case_data['testsuite'] = suite.name
                testcases.append(case_data)

    testlink_json_file = xmind_file_path[:-6] + '.json'

    if os.path.exists(testlink_json_file):
        os.remove(testlink_json_file)

    with open(testlink_json_file, 'w', encoding='utf8') as f:
        f.write(json.dumps(testcases, indent=4, separators=(',', ': ')))

    return testlink_json_file


def testsuite_to_testlink_xml_file(testsuite, xmind_file_path):
    """Convert a XMind sheet to a testlink xml file"""
    xml_content = testsuite_to_xml_content(testsuite)

    suite_name = '_'.join(testsuite.name.split())
    testsuite_xml_file = xmind_file_path[:-6] + '_' + suite_name + '.xml'

    if os.path.exists(testsuite_xml_file):
        os.remove(testsuite_xml_file)

    with open(testsuite_xml_file, 'w', encoding='utf-8') as f:
        pretty_content = minidom.parseString(
            xml_content).toprettyxml(indent='\t')
        f.write(pretty_content)

    return testsuite_xml_file


def testsuite_to_xml_content(testsuite):
    root_element = Element(const.TAG_TESTSUITE)

    # setting the root suite's name attribute, that will generate a new testsuite folder on testlink
    # root_element.set(const.ATTR_NMAE, testsuite.name)

    for sub_suite in testsuite.sub_suites:

        if is_should_skip(sub_suite.name):
            continue

        sub_suite_element = SubElement(root_element, const.TAG_TESTSUITE)
        sub_suite_element.set(const.ATTR_NMAE, sub_suite.name)
        gen_text_element(
            sub_suite_element,
            const.TAG_DETAILS,
            sub_suite.details)
        gen_testcase_element(sub_suite_element, sub_suite)

    testlink = ElementTree(root_element)
    content_stream = BytesIO()
    testlink.write(content_stream, encoding='utf-8', xml_declaration=True)
    return content_stream.getvalue()


def is_should_skip(content):
    """A testsuite/testcase/teststep should be skip: 1、content is empty; 2、starts with config.ignore_char"""
    return content is None or \
        not isinstance(content, str) or \
        content.strip() == '' or \
        content[1] in config['ignore_char']


def gen_text_element(parent_element, tag_name, content):
    """generate an element's text conent: <![CDATA[text]]>"""
    if is_should_parse(content):
        child_element = SubElement(parent_element, tag_name)
        element_set_text(child_element, content)


def gen_testcase_element(suite_element, suite):
    for testcase in suite.testcase_list:

        if is_should_skip(testcase.name):
            continue

        testcase_elment = SubElement(suite_element, const.TAG_TESTCASE)
        testcase_elment.set(const.ATTR_NMAE, testcase.name)

        gen_text_element(
            testcase_elment, const.TAG_VERSION, str(
                testcase.version))
        gen_text_element(testcase_elment, const.TAG_SUMMARY, testcase.summary)
        gen_text_element(
            testcase_elment,
            const.TAG_PRECONDITIONS,
            testcase.preconditions)
        gen_text_element(
            testcase_elment,
            const.TAG_EXECUTION_TYPE,
            _convert_execution_type(
                testcase.execution_type))
        gen_text_element(
            testcase_elment,
            const.TAG_IMPORTANCE,
            _convert_importance(
                testcase.importance))

        estimated_exec_duration_element = SubElement(
            testcase_elment, const.TAG_ESTIMATED_EXEC_DURATION)
        estimated_exec_duration_element.text = str(
            testcase.estimated_exec_duration)

        status = SubElement(testcase_elment, const.TAG_STATUS)
        status.text = str(
            testcase.status) if testcase.status in (
            1, 2, 3, 4, 5, 6, 7) else '7'

        gen_steps_element(testcase_elment, testcase)


def gen_steps_element(testcase_element, testcase):
    if testcase.steps:
        steps_element = SubElement(testcase_element, const.TAG_STEPS)

        for step in testcase.steps:

            if is_should_skip(step.actions):
                continue

            step_element = SubElement(steps_element, const.TAG_STEP)
            gen_text_element(
                step_element, const.TAG_STEP_NUMBER, str(
                    step.step_number))
            gen_text_element(step_element, const.TAG_ACTIONS, step.actions)
            gen_text_element(
                step_element,
                const.TAG_EXPECTEDRESULTS,
                step.expectedresults)
            gen_text_element(
                step_element,
                const.TAG_EXECUTION_TYPE,
                _convert_execution_type(
                    step.execution_type))


def is_should_parse(content):
    """An element that has a string content and doesn't start with exclamation mark should be parsing"""
    return isinstance(content, str) and not content[1] in config['ignore_char']


def element_set_text(element, content):
    # retain html tags in content
    content = escape(content, entities={'\r\n': '<br />'})
    # replace new line for *nix system
    content = content.replace('\n', '<br />')
    # add the line break in source to make it readable
    content = content.replace('<br />', '<br />\n')

    # add CDATA for a element  TODO(devin): fix format
    element.append(Comment(' --><![CDATA[' + content.replace(']]>', ']]]]><![CDATA[>') + ']]><!--'))


def _convert_execution_type(value):
    if value in (1, '手动', '手工', 'manual', 'Manual'):
        return '1'
    elif value in (2, '自动', '自动化', '自动的', 'Automate', 'Automated', 'Automation', 'automate', 'automated', 'automation'):
        return '2'
    else:
        return '1'


def _convert_importance(value):
    mapping = {1: '3', 2: '2', 3: '1'}
    if value in mapping.keys():
        return mapping[value]
    else:
        return '2'
