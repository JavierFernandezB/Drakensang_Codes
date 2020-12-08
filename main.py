import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from os.path import exists
import datetime

source = requests.get(
    "https://drakensangonline.fandom.com/wiki/Bonus_Codes").text
soup = BeautifulSoup(source, 'html.parser')
article = soup.find_all('ul')[17]
article = article.text
USER = ""
PASSWORD = ""
if not exists(r'C:\Users\javier\Documents\code\python\drakensang_code\\oldcodes'):
    open(r'C:\Users\javier\Documents\code\python\drakensang_code\oldcodes', 'x').close()

if not exists(r'C:\Users\javier\Documents\code\python\drakensang_code\chromedriver.exe'):
    print('Chromedriver not found')


def clean_codes(codes):
    try:
        open(r'C:\Users\javier\Documents\code\python\drakensang_code\temp', 'x')
    except FileExistsError:
        pass
    with open(r'C:\Users\javier\Documents\code\python\drakensang_code\temp', 'a') as f:
        f.write(article)
    cleaned = []
    for code in open(r'C:\Users\javier\Documents\code\python\drakensang_code\temp').readlines():
        if code.endswith("\n"):
            code = code[:-1]
        f=code.split(" ")
        code=f[0]
        cleaned.append(code)
    open(r'C:\Users\javier\Documents\code\python\drakensang_code\temp', 'w').write('')
    
    return cleaned


def save_old_codes(code):
    with open(r'C:\Users\javier\Documents\code\python\drakensang_code\oldcodes', 'wb') as f:
        pickle.dump(code, f)


def load_olds():
    with open(r'C:\Users\javier\Documents\code\python\drakensang_code\oldcodes', 'rb') as f:
        olds = pickle.load(f)
    return olds



def insert_code(codes=[]):
    driver = webdriver.Chrome(r'C:\Users\javier\Documents\code\python\drakensang_code\chromedriver.exe')
    driver.get('https://heredur.drakensang.com/en/login')
    try:
        sleep(2)
        cookie = "//*[@id='qc-cmp2-ui']/div[2]/div/button[2]"
        f=driver.find_element_by_xpath(cookie)
        f.click()
    except:
        pass
    user = driver.find_element_by_xpath("//*[@id='bgcdw_login_form_username']")
    password = driver.find_element_by_xpath(
        "//*[@id='bgcdw_login_form_password']")
    log = driver.find_element_by_xpath(
        "//*[@id='reg']/div[3]/div[1]/div/form/fieldset[2]/button[1]")
    user.send_keys(USER)
    password.send_keys(PASSWORD)
    log.click()
    sleep(5)
    code_input = driver.find_element_by_xpath(
        "//*[@id='content']/ul/li[2]/form/input")
    code_button = driver.find_element_by_xpath(
        "//*[@id='content']/ul/li[2]/form/button")
    check_js = driver.find_element_by_xpath(
        "//*[@id='overlayContainer']/div/a[1]")
    for i in codes:
        code_input.send_keys(i)
        code_button.click()
        sleep(2)
        check_js.click()
        code_input.send_keys([Keys.BACK_SPACE for _ in range(20)])
    driver.close()


page_codes = clean_codes(article)
old_codes = load_olds()
to_insert = []
for code in page_codes:
    if code in old_codes:
        print(f'This code is old: {code}')
    else:
        print(f'this one is new {code}')
        to_insert.append(code)
hay_code = False
if to_insert != []:
    insert_code(to_insert)

    old_codes_send = old_codes
    for i in to_insert:
        old_codes_send.append(i)
    with open(r'C:\Users\javier\Documents\code\python\drakensang_code\oldcodes', 'wb') as f:
        pickle.dump(old_codes_send, f)
    hay_code = True
else:
    hay_code = False

scaned = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if hay_code:
    hay_code = 'Si'
else:
    hay_code = 'No'
with open(r'C:\Users\javier\Documents\code\python\drakensang_code\days.log', 'a') as f:
    f.write(scaned + " " + hay_code + "\n")
