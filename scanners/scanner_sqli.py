from dataclasses import dataclass, field, asdict
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

s = requests.Session()

@dataclass
class InputField:
    type: str= ""
    name: str= ""
    value: str = ""

@dataclass
class FormField:
    action: str=""
    method: str=""
    input_fields: List[InputField] = field(default_factory=list)

@dataclass
class JudgmentString:
    strings: list[str] = field(default_factory=list)

@dataclass
class InjectionString:
    strings: list[str] = field(default_factory=list)


def get_judgment_strings():
    judgment_strings = JudgmentString()
    judgment_strings.strings += {"pyodbc.programmingerror"}
    return judgment_strings

def get_injection_strings():
    injection_strings = InjectionString()
    injection_strings.strings += {"'", "tom", "tom'"}
    return injection_strings

def get_form_area(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    form_area = soup.find("form")
    return form_area

def get_form_info(form_area):
    form_field = FormField()
    form_field.action = form_area.attrs.get("action").lower()
    form_field.method = form_area.attrs.get("method", "get").lower()

    for input_tag in form_area.find_all("input"):
        input_field = InputField()
        input_field.type = input_tag.attrs.get("type", "text")
        input_field.name = input_tag.attrs.get("name")
        input_field.value = input_tag.attrs.get("value", "")

        form_field.input_fields.append(input_field)
    
    return form_field

def check_vulnerability(response, url, payload):
    judgment_strings = get_judgment_strings()

    for judgment_string in judgment_strings.strings:
        if judgment_string in response.content.decode().lower():
            print("Injection detected: ", url, "\nTesting data: ", str(payload), "\n Detection string: ", judgment_string, "\n", "-"*10)

def make_payload(form_info, injection_string):
    payload = {}

    for input_field in form_info.input_fields:
        if input_field.type != "submit":
            payload.update({input_field.name: injection_string})
    
    return payload

def send_injection(url, form_info, payload):
    if form_info.method == "post":
        response = s.post(url, data=payload)
    elif form_info.method == "get":
        response = s.get(url, params=payload)
    return response

def page_scan(start_url):
    form_area = get_form_area(start_url)
    form_info = get_form_info(form_area)
    injection_strings = get_injection_strings()

    for injection_string in injection_strings.strings:
        payload = make_payload(form_info, injection_string)
        url = urljoin(start_url, form_info.action)

        response = send_injection(url, form_info, payload)
        check_vulnerability(response, url, payload)

if __name__ == "__main__":
    page_url = "http://127.0.0.1:5000/item_search"
    page_scan(page_url)