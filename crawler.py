import re
import json
from selenium import webdriver
from order_dict import DefaultListOrderedDict


def strip_ordinal(text):
    return re.sub(r'^\d{1}', '', text).strip()


def extract_test(url):
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

    test_name = browser.find_element_by_class_name('title-baihoc').text

    browser.close()

    with open('text/' + test_name + '.json', 'w') as fp:
        json.dump(questions, fp)


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


urls = [
    'http://jlpt4u.info/test/create_test/11',
    'http://jlpt4u.info/test/create_test/18',
    'http://jlpt4u.info/test/create_test/19',
    'http://jlpt4u.info/test/create_test/20',
    'http://jlpt4u.info/test/create_test/52',
    'http://jlpt4u.info/test/create_test/53',
    'http://jlpt4u.info/test/create_test/54',
    'http://jlpt4u.info/test/create_test/55',
    'http://jlpt4u.info/test/create_test/56',
    'http://jlpt4u.info/test/create_test/23',
    'http://jlpt4u.info/test/create_test/24',
    'http://jlpt4u.info/test/create_test/25',
    'http://jlpt4u.info/test/create_test/26',
    'http://jlpt4u.info/test/create_test/27',
    'http://jlpt4u.info/test/create_test/28',
    'http://jlpt4u.info/test/create_test/29',
    'http://jlpt4u.info/test/create_test/57',
    'http://jlpt4u.info/test/create_test/58',
    'http://jlpt4u.info/test/create_test/63',
    'http://jlpt4u.info/test/create_test/31',
    'http://jlpt4u.info/test/create_test/32',
    'http://jlpt4u.info/test/create_test/33',
    'http://jlpt4u.info/test/create_test/34',
    'http://jlpt4u.info/test/create_test/36',
    'http://jlpt4u.info/test/create_test/37',
    'http://jlpt4u.info/test/create_test/61',
    'http://jlpt4u.info/test/create_test/62',
    'http://jlpt4u.info/test/create_test/59',
    'http://jlpt4u.info/test/create_test/60'
]

for url in urls:
    extract_test(url)
