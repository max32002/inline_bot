#!/usr/bin/env python3
#encoding=utf-8
import os
import sys
import platform
import json
import random

# seleniumwire not support python 2.x.
# if you want running under python 2.x, you need to assign driver_type = 'stealth'
driver_type = 'selenium'
driver_type = 'undetected_chromedriver'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# for close tab.
from selenium.common.exceptions import NoSuchWindowException
# for alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
# for alert 2
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# for ["pageLoadStrategy"] = "eager"
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# for selenium 4
from selenium.webdriver.chrome.service import Service

# for wait #1
import time

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# for error output
import logging
logging.basicConfig()
logger = logging.getLogger('logger')


app_version = "MaxinlineBot (2022.09.22)"

homepage_default = u"https://inline.app/"

# initial webdriver
# 說明：初始化 webdriver
driver = None

homepage = ""
browser = "chrome"

adult_picker = ""
book_now_time = ""
book_now_time_alt = ""

user_name = ""
user_gender = ""
user_phone = ""
user_email = ""

cardholder_name=""
cardholder_email = ""
cc_number = ""
cc_exp = ""
cc_ccv = ""

cc_auto_submit = False

debugMode = False

def get_app_root():
    # 讀取檔案裡的參數值
    basis = ""
    if hasattr(sys, 'frozen'):
        basis = sys.executable
    else:
        basis = sys.argv[0]
    app_root = os.path.dirname(basis)
    return app_root

def get_config_dict():
    config_json_filename = 'settings.json'
    app_root = get_app_root()
    config_filepath = os.path.join(app_root, config_json_filename)
    config_dict = None
    if os.path.isfile(config_filepath):
        with open(config_filepath) as json_data:
            config_dict = json.load(json_data)
    return config_dict

def load_config_from_local(driver):
    config_dict = get_config_dict()

    global homepage
    global homepage_default
    global browser

    global adult_picker 
    global book_now_time 
    global book_now_time_alt 
    global user_name 
    global user_gender 
    global user_phone 
    global user_email 
    global cardholder_name
    global cardholder_email 
    global cc_number 
    global cc_exp 
    global cc_ccv

    global cc_auto_submit

    global debugMode

    if config_dict is None:
        print("Config is empty!")
        config_dict = {}


    if not config_dict is None:
        # output config:
        print("homepage", config_dict["homepage"])
        print("adult_picker", config_dict["adult_picker"])
        print("book_now_time", config_dict["book_now_time"])
        print("book_now_time_alt", config_dict["book_now_time_alt"])
        
        print("user_name", config_dict["user_name"])
        print("user_gender", config_dict["user_gender"])
        print("user_phone", config_dict["user_phone"])
        print("user_email", config_dict["user_email"])

        print("cardholder_name", config_dict["cardholder_name"])
        print("cardholder_email", config_dict["cardholder_email"])
        print("cc_number", config_dict["cc_number"])
        print("cc_exp", config_dict["cc_exp"])
        print("cc_ccv", config_dict["cc_ccv"])
        
        if 'cc_auto_submit' in config_dict:
            print("cc_auto_submit", config_dict["cc_auto_submit"])

        homepage = config_dict["homepage"]
        adult_picker = config_dict["adult_picker"]
        book_now_time = config_dict["book_now_time"]
        book_now_time_alt = config_dict["book_now_time_alt"]
        
        user_name = config_dict["user_name"]
        user_gender = config_dict["user_gender"]
        user_phone = config_dict["user_phone"]
        user_email = config_dict["user_email"]

        cardholder_name = config_dict["cardholder_name"]
        cardholder_email = config_dict["cardholder_email"]
        cc_number = config_dict["cc_number"]
        cc_exp = config_dict["cc_exp"]
        cc_ccv = config_dict["cc_ccv"]

        if 'cc_auto_submit' in config_dict:
            cc_auto_submit = config_dict["cc_auto_submit"]

        # entry point
        # 說明：自動開啟第一個的網頁
        if homepage is None:
            homepage = ""
        if len(homepage) == 0:
            homepage = homepage_default

        Root_Dir = ""
        if browser == "chrome":

            DEFAULT_ARGS = [
                '--disable-audio-output',
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-breakpad',
                '--disable-browser-side-navigation',
                '--disable-checker-imaging', 
                '--disable-client-side-phishing-detection',
                '--disable-default-apps',
                '--disable-demo-mode', 
                '--disable-dev-shm-usage',
                #'--disable-extensions',
                '--disable-features=site-per-process',
                '--disable-hang-monitor',
                '--disable-in-process-stack-traces', 
                '--disable-javascript-harmony-shipping', 
                '--disable-logging', 
                '--disable-notifications', 
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--disable-perfetto',
                '--disable-permissions-api', 
                '--disable-plugins',
                '--disable-presentation-api',
                '--disable-reading-from-canvas', 
                '--disable-renderer-accessibility', 
                '--disable-renderer-backgrounding', 
                '--disable-shader-name-hashing', 
                '--disable-smooth-scrolling',
                '--disable-speech-api',
                '--disable-speech-synthesis-api',
                '--disable-sync',
                '--disable-translate',

                '--ignore-certificate-errors',

                '--metrics-recording-only',
                '--no-first-run',
                '--no-experiments',
                '--safebrowsing-disable-auto-update',
                #'--enable-automation',
                '--password-store=basic',
                '--use-mock-keychain',
                '--lang=zh-TW',
                '--stable-release-mode',
                '--use-mobile-user-agent', 
                '--webview-disable-safebrowsing-support',
                #'--no-sandbox',
                #'--incognito',
            ]

            chrome_options = webdriver.ChromeOptions()

            # for navigator.webdriver
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False,'profile.default_content_setting_values':{'notifications':2}})

            # default os is linux/mac
            chromedriver_path =Root_Dir+ "webdriver/chromedriver"
            if platform.system()=="windows":
                chromedriver_path =Root_Dir+ "webdriver/chromedriver.exe"

            #caps = DesiredCapabilities().CHROME
            caps = chrome_options.to_capabilities()

            #caps["pageLoadStrategy"] = u"normal"  #  complete
            caps["pageLoadStrategy"] = u"eager"  #  interactive
            #caps["pageLoadStrategy"] = u"none"
            
            #caps["unhandledPromptBehavior"] = u"dismiss and notify"  #  default
            caps["unhandledPromptBehavior"] = u"ignore"
            #caps["unhandledPromptBehavior"] = u"dismiss"

            driver = None

            # method 5: uc
            if driver_type=="undetected_chromedriver":
                import undetected_chromedriver as uc
                #import seleniumwire.undetected_chromedriver as uc
                # multiprocessing not work bug.
                if platform.system().lower()=="windows":
                    if hasattr(sys, 'frozen'):
                        from multiprocessing import freeze_support
                        freeze_support()

                options = uc.ChromeOptions()
                options.add_argument("--password-store=basic")
                options.page_load_strategy="eager"
                #print("strategy", options.page_load_strategy)

                if os.path.exists(chromedriver_path):
                    print("Use user driver path:", chromedriver_path)
                    #driver = uc.Chrome(service=chrome_service, options=options, suppress_welcome=False)
                    driver = uc.Chrome(executable_path=chromedriver_path, options=options, suppress_welcome=False)
                else:
                    print("Oops! web driver not on path:",chromedriver_path )
                    print('let uc automatically download chromedriver.')
                    driver = uc.Chrome(options=options, suppress_welcome=False)

                if driver is None:
                    print("create web drive object fail!")

                download_dir_path="."
                params = {
                    "behavior": "allow",
                    "downloadPath": os.path.realpath(download_dir_path)
                }
                #print("assign setDownloadBehavior.")
                driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
            else:
                # method 4:
                chrome_service = Service(chromedriver_path)
                driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


        if browser == "firefox":
            # default os is linux/mac
            chromedriver_path =Root_Dir+ "webdriver/geckodriver"
            if platform.system()=="windows":
                chromedriver_path =Root_Dir+ "webdriver/geckodriver.exe"

            firefox_service = Service(chromedriver_path)
            driver = webdriver.Firefox(service=firefox_service)

        time.sleep(1.0)

        # get url from dropdownlist.
        homepage_url = ""
        if len(homepage) > 0:
            target_str = u'http://'
            if target_str in homepage:
                target_index = homepage.find(target_str)
                homepage_url = homepage[target_index:]
            target_str = u'https://'
            if target_str in homepage:
                target_index = homepage.find(target_str)
                homepage_url = homepage[target_index:]

        if len(homepage_url) > 0:
            try:
                window_handles_count = len(driver.window_handles)
                if window_handles_count >= 1:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as excSwithFail:
                pass

            driver.get(homepage_url)
            print("after homepage:", homepage_url)

    return driver

def is_House_Rules_poped(driver):
    ret = False
    #---------------------------
    # part 1: check house rule pop
    #---------------------------
    house_rules_div = None

    try:
        house_rules_div = driver.find_element(By.ID, 'house-rules')
    except Exception as exc:
        #print("check house rules fail...")
        #print(exc)
        pass

    if house_rules_div is not None:
        if house_rules_div.is_enabled():
            #print("house rules window poped.")

            #houses_rules_button = house_rules_div.find_element(By.TAG_NAME, 'button')
            houses_rules_button = house_rules_div.find_element(By.XPATH, '//button[@data-cy="confirm-house-rule"]')
            
            if houses_rules_button is not None:
                new_houses_rules_text = "..."

                if not houses_rules_button.is_enabled():
                    #print("found disabled houses_rules_button, enable it.")
                    
                    # method 1: force enable, fail.
                    # driver.execute_script("arguments[0].disabled = false;", commit)

                    # metho 2: scroll to end.
                    houses_rules_scroll = house_rules_div.find_element(By.XPATH, '//div[@data-show-scrollbar="true"]/div/div')
                    if houses_rules_scroll is not None:
                        if houses_rules_scroll.is_enabled():
                            try:
                                #print("found enabled scroll bar. scroll to end.")
                                houses_rules_scroll.click()
                                
                                #print('send end key.')
                                #houses_rules_scroll.send_keys(Keys.END)
                                
                                #driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", houses_rules_scroll)
                                driver.execute_script("arguments[0].innerHTML='';", houses_rules_scroll);
                            except Exception as exc:
                                #print("check house rules fail...")
                                #print(exc)
                                pass

                        #new_houses_rules_text = houses_rules_scroll.text
                        #print("new text:", new_houses_rules_text)
                        # reset innerHTML cuase text==empty .
                
                if houses_rules_button.is_enabled():
                    print("found enabled houses_rules_button.")
                    try:
                        houses_rules_button.click()
                    except Exception as exc:
                            driver.execute_script("arguments[0].click();", houses_rules_button);
                            #print(exc)
                            pass


    return ret

def button_submit(el_form, by_method, query_keyword):
    # user name
    el_text_name = None
    try:
        el_text_name = el_form.find_element(by_method, query_keyword)
    except Exception as exc:
        pass
        #print("find el_text_%s fail" % (query_keyword))
    if el_text_name is not None:
        #print("found el_text_name")
        if el_text_name.is_enabled():
            try:
                el_text_name.click()
            except Exception as exc:
                print("send el_text_%s fail" % (query_keyword))
                #print(exc)

                try:
                    driver.execute_script("arguments[0].click();", el_text_name);
                except Exception as exc:
                    print("try javascript click on el_text_%s, still fail." % (query_keyword))
                    #print(exc)


def click_radio(el_form, by_method, query_keyword, assign_method='CLICK'):
    ret = False
    # user name
    
    el_text_name = None

    try:
        el_text_name = el_form.find_element(by_method, query_keyword)
    except Exception as exc:
        pass
        #print("find el_text_%s fail" % (query_keyword))
    if el_text_name is not None:
        #print("found el_text_name")
        ret = el_text_name.is_selected()
        if not el_text_name.is_selected():
            if assign_method=='CLICK':
                try:
                    el_text_name.click()
                except Exception as exc:
                    print("send el_text_%s fail" % (query_keyword))

                    #print(exc)
                    try:
                        driver.execute_script("arguments[0].click();", el_text_name);
                    except Exception as exc:
                        print("try javascript click on el_text_%s, still fail." % (query_keyword))
                        #print(exc)

            if assign_method=='JS':
                try:
                    driver.execute_script("arguments[0].checked;" % (default_value), el_text_name);
                except Exception as exc:
                    print("send el_text_%s fail" % (query_keyword))
                    print(exc)
        else:
            pass
            #print("text not empty, value:", text_name_value)

    return ret


def checkbox_agree(el_form, by_method, query_keyword, assign_method='CLICK'):
    ret = False
    # user name
    
    el_text_name = None
    el_label_name = None

    try:
        el_text_name = el_form.find_element(by_method, query_keyword)
        if by_method == By.ID:
            el_label_name = el_form.find_element(By.XPATH, '//label[@for="%s"]' % (query_keyword))
    except Exception as exc:
        pass
        #print("find el_text_%s fail" % (query_keyword))
    if el_text_name is not None:
        #print("found el_text_name")
        ret = el_text_name.is_selected()
        if not el_text_name.is_selected():
            if assign_method=='CLICK':
                #el_text_name.click()
                if el_label_name is not None:
                    print('click label for chekbox:', query_keyword)
                    try:
                        el_label_name.click()
                    except Exception as exc:
                        print("send el_text_%s fail" % (query_keyword))
                        #print(exc)
                        try:
                            driver.execute_script("arguments[0].click();", el_label_name);
                        except Exception as exc:
                            print("try javascript click on el_text_%s, still fail." % (query_keyword))
                            #print(exc)

            if assign_method=='JS':
                driver.execute_script("arguments[0].checked;", el_text_name);
        else:
            pass
            #print("text not empty, value:", text_name_value)

    return ret

# assign value in text.
# return:
#   True: value in text
#   False: assign fail.
def fill_text_by_default(el_form, by_method, query_keyword, default_value, assign_method='JS'):
    ret = False

    # user name
    el_text_name = None
    try:
        el_text_name = el_form.find_element(by_method, query_keyword)
    except Exception as exc:
        pass
        #print("find el_text_%s fail" % (query_keyword))
    if el_text_name is not None:
        #print("found el_text_name")
        try:
            text_name_value = str(el_text_name.get_attribute('value'))
            if text_name_value == "":
                #print("try to send keys:", user_name)
                if assign_method=='SENDKEY':
                    el_text_name.send_keys(default_value)
                    ret = True
                if assign_method=='JS':
                    driver.execute_script("arguments[0].value='%s';" % (default_value), el_text_name);
            else:
                ret = True
                pass
                #print("text not empty, value:", text_name_value)
        except Exception as exc:
            print("send el_text_%s fail" % (query_keyword))

    return ret

def fill_personal_info(url, driver):
    ret = False
    #print("fill form")

    # user form
    el_form = None
    try:
        el_form = driver.find_element(By.ID, 'contact-form')
    except Exception as exc:
        pass

    if not el_form is None:
        #print("found form")

        # gender-female
        # gender-male
        if user_gender == "先生":
            ret = click_radio(el_form, By.ID, 'gender-male')
        if user_gender == "小姐":
            ret = click_radio(el_form, By.ID, 'gender-female')

        ret = fill_text_by_default(el_form, By.ID, 'name', user_name)
        ret = fill_text_by_default(el_form, By.ID, 'phone', user_phone)
        ret = fill_text_by_default(el_form, By.ID, 'email', user_email)
        
        ret = fill_text_by_default(el_form, By.ID, 'cardholder-name', cardholder_name)
        ret = fill_text_by_default(el_form, By.ID, 'cardholder-email', cardholder_email)

        iframes = el_form.find_elements(By.TAG_NAME, "iframe")
        #print('start to travel iframes...')
        cc_check=[False,False,False]
        idx_iframe=0
        for iframe in iframes:
            iframe_url = ""
            try:
                iframe_url = str(iframe.get_attribute('src'))
                #print("url:", iframe_url)
            except Exception as exc:
                print("get iframe url fail.")
                #print(exc)
                pass

            idx_iframe += 1
            driver.switch_to.frame(iframe)
            if "card-number" in iframe_url:
                if not cc_check[0]:
                    #print('check cc-number at loop(%d)...' % (idx_iframe))
                    ret = fill_text_by_default(driver, By.ID, 'cc-number', cc_number,assign_method="SENDKEY")
                    cc_check[0]=ret
                    #print("cc-number ret:", ret)
            if "expiration-date" in iframe_url:
                if not cc_check[1]:
                    #print('check cc-exp at loop(%d)...' % (idx_iframe))
                    ret = fill_text_by_default(driver, By.ID, 'cc-exp', cc_exp)
                    cc_check[1]=ret
                    #print("cc-exp ret:", ret)
            if "ccv" in iframe_url:
                if not cc_check[2]:
                    #print('check cc-ccv at loop(%d)...' % (idx_iframe))
                    ret = fill_text_by_default(driver, By.ID, 'cc-ccv', cc_ccv)
                    cc_check[2]=ret
                    #print("cc-ccv ret:", ret)
            driver.switch_to.default_content()

        pass_all_check = True

        # check credit card.
        for item in cc_check:
            if item == False:
                pass_all_check = False

        # check agree
        try:
            #print("check agree...")
            #driver.execute_script("$(\"input[type='checkbox']\").prop('checked', true);")
            #driver.execute_script("document.getElementById(\"deposit-policy\").checked;")
            #driver.execute_script("document.getElementById(\"privacy-policy\").checked;")
            agree_ret = checkbox_agree(el_form, By.ID, 'deposit-policy')
            if not agree_ret:
                pass_all_check = False
            agree_ret = checkbox_agree(el_form, By.ID, 'privacy-policy')
            if not agree_ret:
                pass_all_check = False
        except Exception as exc:
            print("javascript check agree fail")
            print(exc)
            pass

        #print("auto_submit:", cc_auto_submit)
        if pass_all_check and cc_auto_submit:
            print("press submit button.")
            ret = button_submit(el_form, By.XPATH,'//button[@type="submit"]')
            pass

    return ret

# reutrn: 
#   False: book fail.
#   True: one of book item is seleted, must to do nothing.
# fail_code:
#   0: no target time in button list.
#   1: time_picker not viewable.
#   100: target time full.
#   200: target button is not viewable or not enable.
#   201: target time click fail.
def book_time(el_time_picker_list, target_time):
    ret = False
    fail_code = 0

    is_one_of_time_picket_viewable = False

    if not el_time_picker_list is None:
        for el_time_picker in el_time_picker_list:
            if el_time_picker.is_enabled():
                is_one_of_time_picket_viewable = True

                time_picker_text = str(el_time_picker.text)
                if ":" in time_picker_text:
                    #print("button text:", time_picker_text)
                    button_cass = str(el_time_picker.get_attribute('class'))
                    
                    is_button_able_to_select = True
                    if "selected" in button_cass:
                        is_button_able_to_select = False
                        ret = True
                        #print("button is selected:", button_cass, time_picker_text)

                        # no need more loop.
                        break

                    if "full" in button_cass:
                        is_button_able_to_select = False
                        if target_time in time_picker_text:
                            #print("button is full:", button_cass, time_picker_text)
                            fail_code = 100

                            # no need more loop.
                            break

                    
                    if is_button_able_to_select:
                        if target_time in time_picker_text:
                            is_able_to_click = True
                            if is_able_to_click:
                                if el_time_picker.is_enabled():
                                    print('click this time block:', time_picker_text)

                                    try:
                                        el_time_picker.click()
                                        ret = True
                                    except Exception as exc:
                                        # is not clickable at point
                                        #print("click target time fail.", exc)
                                        fail_code = 201

                                        # scroll to view ... fail.
                                        #driver.execute_script("console.log(\"scroll to view\");")
                                        #driver.execute_script("arguments[0].scrollIntoView(false);", el_time_picker)

                                        # JS
                                        print('click to button using javascript.')
                                        driver.execute_script("console.log(\"click to button.\");")
                                        driver.execute_script("arguments[0].click();", el_time_picker)
                                        pass
                                else:
                                    fail_code = 200
                                    print("target button is not viewable or not enable.")
                                    pass

        if not is_one_of_time_picket_viewable:
            fail_code = 1
    return ret, fail_code

def assign_adult_picker(driver):
    is_alult_picker_assigned = False

    # member number.
    el_adult_picker = None
    try:
        el_adult_picker = driver.find_element(By.ID, 'adult-picker')
    except Exception as exc:
        pass
    if not el_adult_picker is None:
        if el_adult_picker.is_enabled():
            selected_value = str(el_adult_picker.get_attribute('value'))
            #print('seleced value:', selected_value)

            is_need_assign_select = True

            if selected_value != "0":
                # not is default value, do assign.
                is_need_assign_select = False
                is_alult_picker_assigned = True

            if is_need_assign_select:
                #print('assign new value("%s") for select.' % (adult_picker))
                adult_number_select = Select(el_adult_picker)
                try:
                    adult_number_select.select_by_value(adult_picker)
                    is_alult_picker_assigned = True
                except Exception as exc:
                    print("select_by_value for adult-picker fail")
                    print(exc)
                    pass

    return is_alult_picker_assigned

def assign_time_picker(driver):
    ret = False

    el_time_picker = None
    try:
        el_time_picker_list = driver.find_elements(By.XPATH, '//button[contains(@class, "ime-slot")]')
        # default use main time.
        book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time)
        print("booking target time:", book_time_ret, book_fail_code, book_now_time)
        if not book_time_ret:
            if book_fail_code >= 200:
                # [200,201] ==> retry
                # retry main target time.
                book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time)
                print("retry booking target time:", book_time_ret, book_fail_code, book_now_time)
            else:
                # try alt time.
                book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time_alt)
                print("booking alt target time:", book_time_ret, book_fail_code, book_now_time_alt)
    except Exception as exc:
        #print("booking Exception:", exc)
        pass
    
    return ret

def inline_reg(url, driver):
    ret = False

    house_rules_ret = is_House_Rules_poped(driver)

    if not house_rules_ret:
        # date picker.
        is_alult_picker_assigned = assign_adult_picker(driver)
        if not is_alult_picker_assigned:
            # retry once.
            is_alult_picker_assigned = assign_adult_picker(driver)

        # time picker.
        if is_alult_picker_assigned:
            ret = assign_time_picker(driver)

    return ret

def main():
    global driver
    driver = load_config_from_local(driver)

    # internal variable. 說明：這是一個內部變數，請略過。
    url = ""
    last_url = ""

    global debugMode
    if debugMode:
        print("Start to looping, detect browser url...")

    while True:
        time.sleep(0.1)

        is_alert_popup = False

        # pass if driver not loaded.
        if driver is None:
            continue

        try:
            alert = None
            if not driver is None:
                alert = driver.switch_to.alert
            if not alert is None:
                if not alert.text is None:
                    alert.accept()
                    is_alert_popup = True
            else:
                print("alert3 not detected")
        except NoAlertPresentException as exc1:
            #logger.error('NoAlertPresentException for alert')
            pass
        except NoSuchWindowException:
            #print('NoSuchWindowException2 at this url:', url )
            #print("last_url:", last_url)
            try:
                window_handles_count = len(driver.window_handles)
                if window_handles_count >= 1:
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as excSwithFail:
                pass
        except Exception as exc:
            logger.error('Exception2 for alert')
            logger.error(exc, exc_info=True)

        #MUST "do nothing: if alert popup.
        #print("is_alert_popup:", is_alert_popup)
        if is_alert_popup:
            continue

        url = ""
        try:
            url = driver.current_url
        except NoSuchWindowException:
            #print('NoSuchWindowException at this url:', url )
            #print("last_url:", last_url)
            try:
                window_handles_count = len(driver.window_handles)
                if window_handles_count >= 1:
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as excSwithFail:
                pass
        except Exception as exc:
            logger.error('Exception')
            logger.error(exc, exc_info=True)

            #UnicodeEncodeError: 'ascii' codec can't encode characters in position 63-72: ordinal not in range(128)
            str_exc = ""
            try:
                str_exc = str(exc)
            except Exception as exc2:
                pass

            if len(str_exc)==0:
                str_exc = repr(exc)
            
            exit_bot_error_strings = [u'Max retries exceeded with url', u'chrome not reachable', u'without establishing a connection']
            for str_chrome_not_reachable in exit_bot_error_strings:
                # for python2
                try:
                    basestring
                    if isinstance(str_chrome_not_reachable, unicode):
                        str_chrome_not_reachable = str(str_chrome_not_reachable)
                except NameError:  # Python 3.x
                    basestring = str

                if isinstance(str_exc, str):
                    if str_chrome_not_reachable in str_exc:
                        print(u'quit bot')
                        driver.quit()
                        import sys
                        sys.exit()

            print("exc", str_exc)
            pass
            
        if url is None:
            continue
        else:
            if len(url) == 0:
                continue

        # 說明：輸出目前網址，覺得吵的話，請註解掉這行。
        if debugMode:
            print("url:", url)

        if len(url) > 0 :
            if url != last_url:
                print(url)
            last_url = url

        # 
        target_domain_list = ['//inline.app/booking/']
        for each_domain in target_domain_list:
            if each_domain in url:
                current_progress_array = url.split('/')
                current_progress_length = len(current_progress_array)
                if current_progress_length >= 6:
                    branch_field = current_progress_array[5]
                    if len(branch_field) >= 0:
                        is_form_mode = False
                        if current_progress_length >= 7:
                            if current_progress_array[6] == 'form':
                                is_form_mode = True

                        if is_form_mode:
                            # fill personal info.
                            ret = fill_personal_info(url, driver)
                        else:
                            # select date.
                            ret = inline_reg(url, driver)


if __name__ == "__main__":
    main()