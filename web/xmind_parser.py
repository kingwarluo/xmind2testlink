"""
Module to parse xmind file into test suite and test case objects.
"""

from web import sharedparser as __
from web.datatype import *


def xmind_to_flat_dict(xmind_file):
    s = xmind_to_suite(xmind_file)
    return __.flat_suite(s)


def xmind_to_suite(xmind_file):
    """Auto detect and parser xmind to test suite object."""
    __.cache.clear()
    __.open_and_cache_xmind(xmind_file)

    if __.is_v2_format(__.cache['root']):
        return xmind_to_suite_v2(xmind_file)
    else:
        return xmind_to_suite_v1(xmind_file)


def xmind_to_suite_v1(xmind_file, custom_dict):
    def parse_suite(suite_dict):
        suite = TestSuite()
        suite.name = suite_dict['title']
        suite.details = suite_dict['note']
        suite.testcase_list = []
        testcase_topics = suite_dict.get('topics', [])
        custom_fields = parse_custom_fields(custom_dict)
        for _ in testcase_topics:
            t = __.parse_testcase(_)
            t.customFields = custom_fields
            suite.testcase_list.append(t)

        return suite


    def parse_custom_fields(custom_fields):
        result = []
        topics = custom_fields['topics']
        for topic in topics:
            custom_field = CustomField();
            custom_field.name = topic['title']
            custom_field.value = topic['topics'][0]['title']
            result.append(custom_field)
        return result

    __.open_and_cache_xmind(xmind_file)
    root = __.cache['root']
    custom = __.cache['custom']

    suite = TestSuite()
    suite.sub_suites = []

    for _ in root['topics']:
        suite.sub_suites.append(parse_suite(_, custom))

    return suite



def xmind_to_suite_v2(xmind_file):
    def parse_testcase_list(cases_dict, parent=None):
        # Judge node of testcase
        if __.is_testcase_topic(cases_dict):
            yield __.parse_testcase(cases_dict, parent)

        else:
            if not parent:
                parent = []

            parent.append(cases_dict)
            topics = cases_dict['topics'] or []

            for child in topics:
                for _ in parse_testcase_list(child, parent):
                    yield _

            parent.pop()

    def parse_suite(suite_dict, custom_dict):
        suite = TestSuite()
        suite.name = suite_dict['title']
        suite.details = suite_dict['note']
        suite.testcase_list = []
        suite.sub_suites = []
        subSuites_list = suite_dict.get('topics', [])
        custom_fields = parse_custom_fields(custom_dict)
        keywords = parse_keywords(custom_dict)

        # Judge floder
        for node in subSuites_list:
            if __.is_testsuite_topic(node):
                suite.sub_suites.append(parse_suite(node, custom_dict))
            else:
                for t in parse_testcase_list(node):
                    t.customFields = custom_fields
                    t.keywords = keywords
                    suite.testcase_list.append(t)
        return suite

    def parse_custom_fields(custom_fields):
        result = []
        topics = custom_fields['topics']
        for topic in topics:
            custom_field = CustomField();
            custom_field.name = topic['title']
            custom_field.value = topic['topics'][0]['title']
            result.append(custom_field)
        return result

    def parse_keywords(custom_fields):
        result = []
        topics = custom_fields['topics']
        for topic in topics:
            if topic['title'] == '关键字':
                result = topic['topics'][0]['title'].split("|")
        return result

    __.open_and_cache_xmind(xmind_file)
    root = __.cache['root']
    custom = __.cache['custom']
    suite = TestSuite()
    suite.sub_suites = []
    for _ in root['topics']:
        suite.sub_suites.append(parse_suite(_, custom))

    return suite
