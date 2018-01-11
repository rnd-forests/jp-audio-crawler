import re
import os
import json
from selenium import webdriver
from collections import OrderedDict
from order_dict import DefaultListOrderedDict


def strip_ordinal(text):
    return re.sub(r'^\d{1}', '', text).strip()


def extract_test(url):
    test = OrderedDict()
    questions = []
    solutions = submit_test(url)

    browser = webdriver.Chrome()
    browser.get(url)
    tab = browser.find_element_by_css_selector('li.sub4')
    tab.click()
    tab_content = browser.find_element_by_css_selector('ul.sub4')
    question_nodes = tab_content.find_elements_by_tag_name('li')

    for node in question_nodes:
        if node.get_attribute('class').startswith('4-'):
            question = DefaultListOrderedDict()
            title = strip_ordinal(node.find_element_by_class_name('titlecauhoi').text)
            question['title'] = title
            solution = [s for s in solutions if s[0] == title][0]
            choices = node.find_elements_by_tag_name('span')
            for choice in choices:
                choice_text = strip_ordinal(choice.text)
                if choice_text:
                    question['choices'].append({'choice': choice_text, 'valid': choice_text == solution[1]})
            questions.append(question)

    test['name'] = browser.find_element_by_class_name('title-baihoc').text
    test['questions'] = questions

    browser.close()
    return test


def submit_test(url):
    solution = list()
    browser = webdriver.Chrome()
    browser.get(url)
    tab = browser.find_element_by_css_selector('li.sub4')
    tab.click()
    tab_content = browser.find_element_by_css_selector('ul.sub4')
    question_nodes = tab_content.find_elements_by_tag_name('li')

    submit_button = browser.find_element_by_css_selector('a.bt_nopbai')
    submit_button.click()
    alert = browser.switch_to_alert()
    alert.accept()

    browser.implicitly_wait(0.5)

    for node in question_nodes:
        if node.get_attribute('class').startswith('4-'):
            title = strip_ordinal(node.find_element_by_class_name('titlecauhoi').text)
            answer = strip_ordinal(node.find_element_by_css_selector('span.correct').text)
            solution.append((title, answer))

    browser.close()

    return solution


test = extract_test("http://jlpt4u.info/test/create_test/53")

with open('test.json', 'w') as fp:
    json.dump(test, fp)
