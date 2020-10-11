import requests
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from os.path import exists

source = requests.get("https://drakensangonline.fandom.com/wiki/Bonus_Codes").text
soup = BeautifulSoup(source,'html.parser')
article = soup.find_all('ul')[16]
article = article.text
USER = "username"
PASSWORD = "password"
if not exists('oldcodes'):
    open('oldcodes','x').close()

if not exists('chromedriver.exe'):
    print('Chromedriver not found')

def clean_codes(codes):
    try:
        open('temp','x')
    except FileExistsError:
        pass
    with open('temp','a') as f:
        f.write(article)
    cleaned = []
    for code in open('temp').readlines():
        code = code[:-2]
        cleaned.append(code)
    open('temp','w').write('')
    
    return cleaned
    
def save_old_codes(code):
    with open('oldcodes','wb') as f:
        pickle.dump(code,f)

def load_olds():
    with open('oldcodes','rb') as f:
        olds = pickle.load(f)
    return olds

def insert_code(codes=[]):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://heredur.drakensang.com/en/login')
    user = driver.find_element_by_xpath("//*[@id='bgcdw_login_form_username']")
    password = driver.find_element_by_xpath("//*[@id='bgcdw_login_form_password']")
    log = driver.find_element_by_xpath("//*[@id='reg']/div[3]/div[1]/div/form/fieldset[2]/button[1]")
    user.send_keys(USER)
    password.send_keys(PASSWORD)
    log.click()
    sleep(5)
    code_input = driver.find_element_by_xpath("//*[@id='content']/ul/li[2]/form/input")
    code_button= driver.find_element_by_xpath("//*[@id='content']/ul/li[2]/form/button")
    check_js = driver.find_element_by_xpath("//*[@id='overlayContainer']/div/a[1]")
    for i in codes:
        code_input.send_keys(codes[i])
        code_button.click()
        sleep(2)
        check_js.click()
    driver.close()
   

page_codes = clean_codes(article)
old_codes = load_olds()
to_insert = []
for code in page_codes:
    if code in old_codes:
        #print(f'This code is old: {code}')
        pass
    else:
        #print(f'this one is new {code}')
        to_insert.append(code)

if to_insert != []:
    insert_code(to_insert)
    old_codes_send = old_codes
    for i in to_insert:
        old_codes_send.append(i)
    with open('oldcodes','wb') as f:
        pickle.dump(old_codes_send,f)
    
else:
    print('sin codigos')

#todo save the old codes in the file

#save_old_codes(page_codes)

