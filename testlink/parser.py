#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
from testlink.metadata import TestSuite, TestCase, TestStep

config = {'sep': ' ',
          'valid_sep': '&>+/-',
          'precondition_sep': '\n----\n',
          'summary_sep': '\n----\n',
          'ignore_char': '#!！'
          }


def xmind_to_suite(xmind_data):
    suites = []

    for sheet in xmind_data:
        logging.debug('start to parse a sheet: %s', sheet['title'])
        root_topic = sheet['topic']
        sub_topics = root_topic.get('topics', [])

        if sub_topics:
            root_topic['topics'] = filter_ignore_or_blank_testcase(sub_topics)
        else:
            logging.error('Invalid XMind file, should have at least 1 sub topic(test suite)')
            exit(1)
        root_suite = sheet_to_suite(root_topic)
        # root_suite.sheet_name = sheet['title']  # root testsuite has a sheet_name attribute
        logging.debug('sheet(%s) parsing complete: %s', sheet['title'], root_suite.to_dict())
        suites.append(root_suite)

    return suites


def filter_ignore_or_blank_testcase(topics):
    """filter blank topic or start with config.ignore_char"""
    result = [topic for topic in topics if not(
            topic['title'] is None or
            topic['title'].strip() == '') or
            topic['title'][0] in config['ignore_char']]

    for topic in result:
        sub_topics = topic.get('topics', [])
        topic['topics'] = filter_ignore_or_blank_testcase(sub_topics)

    return result


def sheet_to_suite(root_topic):
    root_suite = TestSuite()
    root_title = root_topic['title']
    separator = root_title[-1]

    if separator in config['valid_sep']:
        logging.debug('find a valid separator for connecting testcase title: %s', separator)
        config['sep'] = separator  # set the separator for the testcase's title
        root_title = root_title[:-1]
    else:
        config['sep'] = ' '

    root_suite.name = root_title
    root_suite.details = root_topic['note']
    root_suite.sub_suites = []  # TODO(devin): infinite recursive reference problem

    for suite_dict in root_topic['topics']:
        root_suite.sub_suites.append(parse_testsuite(suite_dict))

    return root_suite


def parse_testsuite(suite_dict):
    testsuite = TestSuite()
    testsuite.name = suite_dict['title']
    testsuite.details = suite_dict['note']
    testsuite.testcase_list = []  # TODO(devin): infinite recursive reference problem
    logging.debug('start to parse a testsuite: %s', testsuite.name)

    for cases_dict in suite_dict.get('topics', []):
        for case in recurse_parse_testcase(cases_dict):
            testsuite.testcase_list.append(case)

    logging.debug('testsuite(%s) parsing complete: %s', testsuite.name, testsuite.to_dict())
    return testsuite


def recurse_parse_testcase(case_dict, parent=None):
    if is_testcase_topic(case_dict):
        case = parse_a_testcase(case_dict, parent)
        yield case
    else:
        if not parent:
            parent = []

        parent.append(case_dict)

        for child_dict in case_dict.get('topics', []):
            for case in recurse_parse_testcase(child_dict, parent):
                yield case

        parent.pop()


def is_testcase_topic(case_dict):
    """A topic with a priority marker, or no subtopic, indicates that it is a testcase"""
    priority = get_priority(case_dict)
    if priority:
        return True

    children = case_dict.get('topics', [])
    if children:
        return False

    return True


def parse_a_testcase(case_dict, parent):
    testcase = TestCase()
    topics = parent + [case_dict] if parent else [case_dict]

    testcase.name = gen_testcase_title(topics)
    testcase.preconditions = gen_testcase_preconditions(topics)
    testcase.summary = gen_testcase_summary(topics)
    testcase.importance = get_priority(case_dict) or 2

    step_dict_list = case_dict.get('topics', [])
    if step_dict_list:
        testcase.steps = parse_test_steps(step_dict_list)

    logging.debug('finds a testcase: %s', testcase.to_dict())
    return testcase


def get_priority(case_dict):
    """Get the topic's priority（equivalent to the importance of the testcase)"""
    if isinstance(case_dict['markers'], list):
        for marker in case_dict['markers']:
            if marker.startswith('priority'):
                return int(marker[-1])


def filter_empty_string(values):
    result = []
    for value in values:
        if isinstance(value, str):
            if value.strip():
                result.append(value.strip())
        # else:
        #     logging.error('Expected string but not: %s', value)
    return result


def gen_testcase_title(topics):
    """Link all topic's title as testcase title"""
    titles = [topic['title'] for topic in topics]
    titles = filter_empty_string(titles)

    # when separator is not blank, will add space around separator, e.g. '/' will be changed to ' / '
    separator = config['sep']
    if separator != ' ':
        separator = ' {} '.format(separator)

    return separator.join(titles)


def gen_testcase_preconditions(topics):
    notes = [topic['note'] for topic in topics]
    notes = filter_empty_string(notes)
    return config['precondition_sep'].join(notes)


def gen_testcase_summary(topics):
    comments = [topic['comment'] for topic in topics]
    comments = filter_empty_string(comments)
    return config['summary_sep'].join(comments)


def parse_test_steps(step_dict_list):
    steps = []

    for step_num, step_dict in enumerate(step_dict_list, 1):
        test_step = parse_a_test_step(step_dict)
        test_step.step_number = step_num
        steps.append(test_step)

    return steps


def parse_a_test_step(step_dict):
    test_step = TestStep()
    test_step.actions = step_dict['title']

    expected_topics = step_dict.get('topics', [])
    if expected_topics:
        test_step.expectedresults = expected_topics[0]['title']  # one test step action, one test expected result

    logging.debug('finds a teststep: %s', test_step.to_dict())
    return test_step









