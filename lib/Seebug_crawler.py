# coding=utf-8
import configparser
import time
from lib.CaptchaHandler import CaptchaHandler
from PIL import Image


from selenium import webdriver

cf = configparser.ConfigParser()
cf.read('../seebug.cfg')

browser = webdriver.Chrome(executable_path="/Users/tianwen/Downloads/chromedriver")

while True:
    browser.get(
        'https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.seebug.org%2Faccounts%2Flogin%2F%3Fnext%3D%252F')
    # 登录界面网页源代码
    con = browser.page_source
    email_input = browser.find_elements_by_name('email')[0].send_keys(cf.get('seebug', 'user'))
    passwd_input = browser.find_elements_by_name('password')[0].send_keys(cf.get('seebug', 'passwd'))

    captchaHandler = CaptchaHandler()
    code = captchaHandler.get_vcode(browser).replace(' ', '')
    print(code)
    if len(code) != 4:
        continue
    else:
        vcode_input = browser.find_elements_by_name('captcha')[0].send_keys(code)
        login_btn = browser.find_element_by_class_name('btn-lg').click()
        try:
            browser.find_element_by_class_name('form-error')
        except Exception:
            break
        else:
            continue
    break

print('登录成功')