from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from dataclasses import dataclass, field, asdict
from typing import List
from urllib.parse import urljoin

@dataclass
class InputField:
    type: str = ""
    name: str = ""
    value: str = ""


@dataclass
class FormField:
    action: str = ""
    method: str = ""
    input_fields: List[InputField] = field(default_factory=list)


@dataclass
class JudgmentString:
    strings: list[str] = field(default_factory=list)


@dataclass
class InjectionString:
    strings: list[str] = field(default_factory=list)


def get_judgment_strings():
    get_judgment_strings = JudgmentString()
    get_judgment_strings.strings += {"pyodbc.programmingerror"}
    
    return get_judgment_strings

def get_injection_strings():
    injection_strings = InjectionString()
    injection_strings.strings += {"'", "tom", "tom'"}

    return injection_strings

def get_form_area(url):
    browser.get(url)
    try:
        element = WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.TAG_NAME, "form")))
    except TimeoutException:
        print("Not found")
        return ""
    
    return element

def get_form_info(form_area):
    form_field = FormField()

    form_field.action = form_area.get_attribute("action").lower()
    form_field.method = form_area.get_attribute("method").lower()

    input_tags = form_area.find_elements_by_tag_name("input")

    for input_tag in input_tags:
        if input_tag.get_attribute("type").lower() != "text":
            continue
        
        input_field = InputField()
        input_field.type = input_tag.get_attribute("type")
        input_field.name = input_tag.get_attribute("name")
        input_field.value = input_tag.get_attribute("value")
        form_field.input_fields.append(input_field)

    return form_field

def check_vulnerability(response, url, injection_string):
    judgment_strings = get_judgment_strings()

    for judgment_string in judgment_strings.strings:
        if judgment_string in response.lower():
            print("Injection detected: ", url, "\n Test data: ", str(injection_string), "\nResult: ", judgment_string, "\n", "-"*10)
    
def send_injection(url, form_info, injection_string):
    browser.get(url)

    for input_field in form_info.input_fields:
        input_element = browser.find_element_by_name(input_field.name)
        input_element.send_keys(injection_string)

    form_element = browser.find_element_by_tag_name("form")
    form_element.submit()

    try:
        element = WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.CLASS_NAME, "errormsg")))
    except TimeoutException:
        return ""
    
    return element.text

def page_scan(start_url):
    form_area = get_form_area(start_url)
    form_info = get_form_info(form_area)
    injection_strings = get_injection_strings()

    for injection_string in injection_strings.strings:
        url = urljoin(start_url, form_info.action)
        response = send_injection(url, form_info, injection_string)
        check_vulnerability(response, url, injection_string)


if __name__ == "__main__":
    browser = webdriver.Chrome()

    page_url = "http://127.0.0.1:5000/item_search"
    page_scan(page_url)