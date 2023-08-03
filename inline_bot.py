#!/usr/bin/env python3
#encoding=utf-8
# seleniumwire not support python 2.x.
# if you want running under python 2.x, you need to assign driver_type = 'stealth'
import os
import pathlib
import sys
import platform
import json
import random

# for close tab.
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
# for alert 2
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
# for selenium 4
from selenium.webdriver.chrome.service import Service
# for wait #1
import time
# for error output
import logging
logging.basicConfig()
logger = logging.getLogger('logger')
# for check reg_info
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import argparse
import chromedriver_autoinstaller

CONST_APP_VERSION = "MaxinlineBot (2023.07.01)"

CONST_MAXBOT_CONFIG_FILE = 'settings.json'
CONST_MAXBOT_LAST_URL_FILE = "MAXBOT_LAST_URL.txt"
CONST_MAXBOT_INT28_FILE = "MAXBOT_INT28_IDLE.txt"

CONST_HOMEPAGE_DEFAULT = "https://inline.app/"

CONST_CHROME_VERSION_NOT_MATCH_EN="Please download the WebDriver version to match your browser version."
CONST_CHROME_VERSION_NOT_MATCH_TW="請下載與您瀏覽器相同版本的WebDriver版本，或更新您的瀏覽器版本。"

CONST_WEBDRIVER_TYPE_SELENIUM = "selenium"
CONST_WEBDRIVER_TYPE_UC = "undetected_chromedriver"


def t_or_f(arg):
    ret = False
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
        ret = True
    elif 'YES'.startswith(ua):
        ret = True
    return ret

def sx(s1):
    key=18
    return ''.join(chr(ord(a) ^ key) for a in s1)

def decryptMe(b):
    s=""
    if(len(b)>0):
        s=sx(base64.b64decode(b).decode("UTF-8"))
    return s

def encryptMe(s):
    data=""
    if(len(s)>0):
        data=base64.b64encode(sx(s).encode('UTF-8')).decode("UTF-8")
    return data

def get_app_root():
    # 讀取檔案裡的參數值
    basis = ""
    if hasattr(sys, 'frozen'):
        basis = sys.executable
    else:
        basis = sys.argv[0]
    app_root = os.path.dirname(basis)
    return app_root

def get_config_dict(args):
    app_root = get_app_root()
    config_filepath = os.path.join(app_root, CONST_MAXBOT_CONFIG_FILE)

    # allow assign config by command line.
    if not args.input is None:
        if len(args.input) > 0:
            config_filepath = args.input

    config_dict = None
    if os.path.isfile(config_filepath):
        with open(config_filepath) as json_data:
            config_dict = json.load(json_data)
    return config_dict

def write_last_url_to_file(url):
    outfile = None
    if platform.system() == 'Windows':
        outfile = open(CONST_MAXBOT_LAST_URL_FILE, 'w', encoding='UTF-8')
    else:
        outfile = open(CONST_MAXBOT_LAST_URL_FILE, 'w')

    if not outfile is None:
        outfile.write("%s" % url)

def read_last_url_from_file():
    ret = ""
    with open(CONST_MAXBOT_LAST_URL_FILE, "r") as text_file:
        ret = text_file.readline()
    return ret


def get_favoriate_extension_path(webdriver_path):
    print("webdriver_path:", webdriver_path)
    extension_list = []
    extension_list.append(os.path.join(webdriver_path,"Adblock_3.18.1.0.crx"))
    extension_list.append(os.path.join(webdriver_path,"Buster_2.0.1.0.crx"))
    extension_list.append(os.path.join(webdriver_path,"no_google_analytics_1.1.0.0.crx"))
    extension_list.append(os.path.join(webdriver_path,"proxy-switchyomega_2.5.21.0.crx"))
    extension_list.append(os.path.join(webdriver_path,"tampermonkey_4.19.0.0.crx"))
    return extension_list

def get_chromedriver_path(webdriver_path):
    chromedriver_path = os.path.join(webdriver_path,"chromedriver")
    if platform.system().lower()=="windows":
        chromedriver_path = os.path.join(webdriver_path,"chromedriver.exe")
    return chromedriver_path

def get_brave_bin_path():
    brave_path = ""
    if platform.system() == 'Windows':
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = os.path.expanduser('~') + "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = "D:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    if platform.system() == 'Linux':
        brave_path = "/usr/bin/brave-browser"

    if platform.system() == 'Darwin':
        brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

    return brave_path

def get_chrome_options(webdriver_path, adblock_plus_enable, browser="chrome", headless = False):
    chrome_options = webdriver.ChromeOptions()
    if browser=="edge":
        chrome_options = webdriver.EdgeOptions()
    if browser=="safari":
        chrome_options = webdriver.SafariOptions()

    # some windows cause: timed out receiving message from renderer
    if adblock_plus_enable:
        # PS: this is ocx version.
        extension_list = get_favoriate_extension_path(webdriver_path)
        for ext in extension_list:
            if os.path.exists(ext):
                chrome_options.add_extension(ext)
    if headless:
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--lang=zh-TW')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument("--no-sandbox");

    # for navigator.webdriver
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # Deprecated chrome option is ignored: useAutomationExtension
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False, "translate":{"enabled": False}})

    if browser=="brave":
        brave_path = get_brave_bin_path()
        if os.path.exists(brave_path):
            chrome_options.binary_location = brave_path

    chrome_options.page_load_strategy = 'eager'
    #chrome_options.page_load_strategy = 'none'
    chrome_options.unhandled_prompt_behavior = "accept"

    return chrome_options

def load_chromdriver_normal(config_dict, driver_type):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

    driver = None

    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    chromedriver_path = get_chromedriver_path(webdriver_path)

    if not os.path.exists(webdriver_path):
        os.mkdir(webdriver_path)

    if not os.path.exists(chromedriver_path):
        print("WebDriver not exist, try to download...")
        chromedriver_autoinstaller.install(path="webdriver", make_version_dir=False)

    if not os.path.exists(chromedriver_path):
        print("Please download chromedriver and extract zip to webdriver folder from this url:")
        print("請下在面的網址下載與你chrome瀏覽器相同版本的chromedriver,解壓縮後放到webdriver目錄裡：")
        print(URL_CHROME_DRIVER)
    else:
        chrome_service = Service(chromedriver_path)
        chrome_options = get_chrome_options(webdriver_path, config_dict["advanced"]["adblock_plus_enable"], browser=config_dict["browser"], headless=config_dict["advanced"]["headless"])
        try:
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        except Exception as exc:
            error_message = str(exc)
            if show_debug_message:
                print(exc)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)

            if "This version of ChromeDriver only supports Chrome version" in error_message:
                print(CONST_CHROME_VERSION_NOT_MATCH_EN)
                print(CONST_CHROME_VERSION_NOT_MATCH_TW)

                # remove exist download again.
                try:
                    os.unlink(chromedriver_path)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
                chromedriver_autoinstaller.install(path="webdriver", make_version_dir=False)
                chrome_service = Service(chromedriver_path)
                try:
                    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                except Exception as exc2:
                    pass


    if driver_type=="stealth":
        from selenium_stealth import stealth
        # Selenium Stealth settings
        stealth(driver,
              languages=["zh-TW", "zh"],
              vendor="Google Inc.",
              platform="Win32",
              webgl_vendor="Intel Inc.",
              renderer="Intel Iris OpenGL Engine",
              fix_hairline=True,
          )
    #print("driver capabilities", driver.capabilities)

    return driver

def clean_uc_exe_cache():
    is_cache_exist = False
    exe_name = "chromedriver%s"

    platform = sys.platform
    if platform.endswith("win32"):
        exe_name %= ".exe"
    if platform.endswith(("linux", "linux2")):
        exe_name %= ""
    if platform.endswith("darwin"):
        exe_name %= ""

    if platform.endswith("win32"):
        d = "~/appdata/roaming/undetected_chromedriver"
    elif "LAMBDA_TASK_ROOT" in os.environ:
        d = "/tmp/undetected_chromedriver"
    elif platform.startswith(("linux", "linux2")):
        d = "~/.local/share/undetected_chromedriver"
    elif platform.endswith("darwin"):
        d = "~/Library/Application Support/undetected_chromedriver"
    else:
        d = "~/.undetected_chromedriver"
    data_path = os.path.abspath(os.path.expanduser(d))

    p = pathlib.Path(data_path)
    files = list(p.rglob("*chromedriver*?"))
    for file in files:
        is_cache_exist = True
        try:
            os.unlink(str(file))
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    return is_cache_exist

def load_chromdriver_uc(config_dict):
    import undetected_chromedriver as uc

    show_debug_message = True       # debug.
    show_debug_message = False      # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    chromedriver_path = get_chromedriver_path(webdriver_path)

    if not os.path.exists(webdriver_path):
        os.mkdir(webdriver_path)

    if not os.path.exists(chromedriver_path):
        print("WebDriver not exist, try to download...")
        chromedriver_autoinstaller.install(path="webdriver", make_version_dir=False)

    options = uc.ChromeOptions()
    options.page_load_strategy = 'eager'
    #options.page_load_strategy = 'none'
    options.unhandled_prompt_behavior = "accept"

    #print("strategy", options.page_load_strategy)

    if config_dict["advanced"]["adblock_plus_enable"]:
        load_extension_path = ""
        extension_list = get_favoriate_extension_path(webdriver_path)
        for ext in extension_list:
            ext = ext.replace('.crx','')
            if os.path.exists(ext):
                load_extension_path += ("," + os.path.abspath(ext))
        if len(load_extension_path) > 0:
            print('load-extension:', load_extension_path[1:])
            options.add_argument('--load-extension=' + load_extension_path[1:])

    if config_dict["advanced"]["headless"]:
        #options.add_argument('--headless')
        options.add_argument('--headless=new')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-translate')
    options.add_argument('--lang=zh-TW')
    options.add_argument('--disable-web-security')
    options.add_argument("--no-sandbox");

    options.add_argument("--password-store=basic")
    options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False, "translate":{"enabled": False}})

    if config_dict["browser"]=="brave":
        brave_path = get_brave_bin_path()
        if os.path.exists(brave_path):
            options.binary_location = brave_path

    driver = None
    if os.path.exists(chromedriver_path):
        # use chromedriver_autodownload instead of uc auto download.
        is_cache_exist = clean_uc_exe_cache()

        try:
            driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options, headless=config_dict["advanced"]["headless"])
        except Exception as exc:
            print(exc)
            error_message = str(exc)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)

            if "This version of ChromeDriver only supports Chrome version" in error_message:
                print(CONST_CHROME_VERSION_NOT_MATCH_EN)
                print(CONST_CHROME_VERSION_NOT_MATCH_TW)

            # remove exist chromedriver, download again.
            try:
                os.unlink(chromedriver_path)
            except PermissionError:
                pass
            except FileNotFoundError:
                pass

            chromedriver_autoinstaller.install(path="webdriver", make_version_dir=False)
            try:
                driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options, headless=config_dict["advanced"]["headless"])
            except Exception as exc2:
                pass
    else:
        print("WebDriver not found at path:", chromedriver_path)

    if driver is None:
        print('WebDriver object is None..., try again..')
        try:
            driver = uc.Chrome(options=options, headless=config_dict["advanced"]["headless"])
        except Exception as exc:
            print(exc)
            error_message = str(exc)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)

            if "This version of ChromeDriver only supports Chrome version" in error_message:
                print(CONST_CHROME_VERSION_NOT_MATCH_EN)
                print(CONST_CHROME_VERSION_NOT_MATCH_TW)
            pass

    if driver is None:
        print("create web drive object by undetected_chromedriver fail!")

        if os.path.exists(chromedriver_path):
            print("Unable to use undetected_chromedriver, ")
            print("try to use local chromedriver to launch chrome browser.")
            driver_type = "selenium"
            driver = load_chromdriver_normal(config_dict, driver_type)
        else:
            print("建議您自行下載 ChromeDriver 到 webdriver 的資料夾下")
            print("you need manually download ChromeDriver to webdriver folder.")

    return driver

def close_browser_tabs(driver):
    if not driver is None:
        try:
            window_handles_count = len(driver.window_handles)
            if window_handles_count > 1:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except Exception as excSwithFail:
            pass

def get_driver_by_config(config_dict):
    global driver

    # read config.
    homepage = config_dict["homepage"]

    if not config_dict is None:
        # output config:
        print("maxbot app version", CONST_APP_VERSION)
        print("python version", platform.python_version())
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
    if homepage is None:
        homepage = ""
    if len(homepage) == 0:
        homepage = CONST_HOMEPAGE_DEFAULT

    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    print("platform.system().lower():", platform.system().lower())

    if config_dict["browser"] in ["chrome","brave"]:
        # method 6: Selenium Stealth
        if config_dict["webdriver_type"] != CONST_WEBDRIVER_TYPE_UC:
            driver = load_chromdriver_normal(config_dict, config_dict["webdriver_type"])
        else:
            # method 5: uc
            # multiprocessing not work bug.
            if platform.system().lower()=="windows":
                if hasattr(sys, 'frozen'):
                    from multiprocessing import freeze_support
                    freeze_support()
            driver = load_chromdriver_uc(config_dict)

    if config_dict["browser"] == "firefox":
        # default os is linux/mac
        # download url: https://github.com/mozilla/geckodriver/releases
        chromedriver_path = os.path.join(webdriver_path,"geckodriver")
        if platform.system().lower()=="windows":
            chromedriver_path = os.path.join(webdriver_path,"geckodriver.exe")

        if "macos" in platform.platform().lower():
            if "arm64" in platform.platform().lower():
                chromedriver_path = os.path.join(webdriver_path,"geckodriver_arm")

        webdriver_service = Service(chromedriver_path)
        driver = None
        try:
            from selenium.webdriver.firefox.options import Options
            options = Options()
            if config_dict["advanced"]["headless"]:
                options.add_argument('--headless')
                #options.add_argument('--headless=new')
            if platform.system().lower()=="windows":
                binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                if not os.path.exists(binary_path):
                    binary_path = os.path.expanduser('~') + "\\AppData\\Local\\Mozilla Firefox\\firefox.exe"
                if not os.path.exists(binary_path):
                    binary_path = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
                if not os.path.exists(binary_path):
                    binary_path = "D:\\Program Files\\Mozilla Firefox\\firefox.exe"
                options.binary_location = binary_path

            driver = webdriver.Firefox(service=webdriver_service, options=options)
        except Exception as exc:
            error_message = str(exc)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)
            else:
                print(exc)

    if config_dict["browser"] == "edge":
        # default os is linux/mac
        # download url: https://developer.microsoft.com/zh-tw/microsoft-edge/tools/webdriver/
        chromedriver_path = os.path.join(webdriver_path,"msedgedriver")
        if platform.system().lower()=="windows":
            chromedriver_path = os.path.join(webdriver_path,"msedgedriver.exe")

        webdriver_service = Service(chromedriver_path)
        chrome_options = get_chrome_options(webdriver_path, config_dict["advanced"]["adblock_plus_enable"], browser="edge", headless=config_dict["advanced"]["headless"])

        driver = None
        try:
            driver = webdriver.Edge(service=webdriver_service, options=chrome_options)
        except Exception as exc:
            error_message = str(exc)
            #print(error_message)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)

    if config_dict["browser"] == "safari":
        driver = None
        try:
            driver = webdriver.Safari()
        except Exception as exc:
            error_message = str(exc)
            #print(error_message)
            left_part = None
            if "Stacktrace:" in error_message:
                left_part = error_message.split("Stacktrace:")[0]
                print(left_part)

    if driver is None:
        print("create web driver object fail @_@;")
    else:
        try:
            print("goto url:", homepage)
            driver.get(homepage)
            time.sleep(3.0)
        except WebDriverException as exce2:
            print('oh no not again, WebDriverException')
            print('WebDriverException:', exce2)
        except Exception as exce1:
            print('get URL Exception:', exce1)
            pass

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
        pass

    houses_rules_button = None
    if house_rules_div is not None:
        is_visible = False
        try:
            if house_rules_div.is_enabled():
                is_visible = True
        except Exception as exc:
            pass
        if is_visible:
            try:
                #houses_rules_button = house_rules_div.find_element(By.TAG_NAME, 'button')
                houses_rules_button = house_rules_div.find_element(By.XPATH, '//button[@data-cy="confirm-house-rule"]')
            except Exception as exc:
                pass

    if houses_rules_button is not None:
        #print("found disabled houses_rules_button, enable it.")
        
        # method 1: force enable, fail.
        # driver.execute_script("arguments[0].disabled = false;", commit)

        # metho 2: scroll to end.
        houses_rules_scroll = None
        try:
            houses_rules_scroll = house_rules_div.find_element(By.XPATH, '//div[@data-show-scrollbar="true"]/div/div')
        except Exception as exc:
            pass
        
        if houses_rules_scroll is not None:
            try:
                if houses_rules_scroll.is_enabled():
                    #print("found enabled scroll bar. scroll to end.")
                    houses_rules_scroll.click()
                    
                    #PLAN A -- fail.
                    #print('send end key.')
                    #houses_rules_scroll.send_keys(Keys.END)
                    
                    #PLAN B -- OK.
                    #driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", houses_rules_scroll)
                    driver.execute_script("arguments[0].innerHTML='';", houses_rules_scroll);
            except Exception as exc:
                #print("check house rules fail...")
                #print(exc)
                pass


        houses_rules_is_visible = False
        try:
            if houses_rules_button.is_enabled():
                houses_rules_is_visible = True
        except Exception as exc:
            pass
        
        if houses_rules_is_visible:
            print("found enabled houses_rules_button.")
            try:
                houses_rules_button.click()
            except Exception as exc:
                    try:
                        driver.execute_script("arguments[0].click();", houses_rules_button);
                    except Exception as exc2:
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
        is_visible = False
        try:
            if el_text_name.is_enabled():
                is_visible = True
        except Exception as exc:
            pass
        
        if is_visible:
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
    is_radio_selected = False
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
            is_radio_selected = el_text_name.is_selected()
        except Exception as exc:
            pass

        if not is_radio_selected:
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
                    driver.execute_script("arguments[0].checked;", el_text_name);
                except Exception as exc:
                    print("send el_text_%s fail" % (query_keyword))
                    print(exc)
        else:
            pass
            #print("text not empty, value:", text_name_value)

    return is_radio_selected


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
def fill_text_by_default(el_form, by_method, query_keyword, default_value, assign_method='SENDKEY'):
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
        text_name_value = None
        try:
            text_name_value = str(el_text_name.get_attribute('value'))
        except Exception as exc:
            pass
        if not text_name_value is None:
            if text_name_value == "":
                #print("try to send keys:", user_name)
                if assign_method=='SENDKEY':
                    try:
                        el_text_name.send_keys(default_value)
                        ret = True
                    except Exception as exc:
                        try:
                            driver.execute_script("arguments[0].value='%s';" % (default_value), el_text_name);
                        except Exception as exc:
                            pass
                if assign_method=='JS':
                    try:
                        driver.execute_script("arguments[0].value='%s';" % (default_value), el_text_name);
                    except Exception as exc:
                        pass

            else:
                ret = True

    return ret

def fill_personal_info(driver, config_dict):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

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
        user_gender = config_dict["user_gender"]
        if user_gender == "先生":
            ret = click_radio(el_form, By.ID, 'gender-male')
        if user_gender == "小姐":
            ret = click_radio(el_form, By.ID, 'gender-female')

        user_name = config_dict["user_name"]
        user_phone = config_dict["user_phone"]
        user_email = config_dict["user_email"]
        ret = fill_text_by_default(el_form, By.ID, 'name', user_name)
        ret = fill_text_by_default(el_form, By.ID, 'phone', user_phone)
        ret = fill_text_by_default(el_form, By.ID, 'email', user_email)
        
        
        cardholder_name = config_dict["cardholder_name"]
        cardholder_email = config_dict["cardholder_email"]
        ret = fill_text_by_default(el_form, By.ID, 'cardholder-name', cardholder_name)
        ret = fill_text_by_default(el_form, By.ID, 'cardholder-email', cardholder_email)

        cc_number = config_dict["cc_number"]
        cc_exp = config_dict["cc_exp"]
        cc_ccv = config_dict["cc_ccv"]
        
        iframes = None
        try:
            iframes = el_form.find_elements(By.TAG_NAME, "iframe")
        except Exception as exc:
            pass

        if iframes is None:
            iframes = []

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
            try:
                driver.switch_to.frame(iframe)
            except Exception as exc:
                pass

            if "card-number" in iframe_url:
                if not cc_check[0]:
                    #print('check cc-number at loop(%d)...' % (idx_iframe))
                    ret = fill_text_by_default(driver, By.ID, 'cc-number', cc_number)
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
            try:
                driver.switch_to.default_content()
            except Exception as exc:
                pass

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

    for el_time_picker in el_time_picker_list:
        is_visible = False
        try:
            if el_time_picker.is_enabled():
                is_visible = True
        except Exception as exc:
            pass
        
        time_picker_text = None
        if is_visible:
            is_one_of_time_picket_viewable = True
            try:
                time_picker_text = str(el_time_picker.text)
            except Exception as exc:
                pass
        
        if time_picker_text is None:
            time_picker_text = ""

        if len(time_picker_text) > 0:
            if ":" in time_picker_text:
                #print("button text:", time_picker_text)
                button_class_string = None
                try:
                    button_class_string = str(el_time_picker.get_attribute('class'))
                except Exception as exc:
                    pass
                if button_class_string is None:
                    button_class_string = ""
                
                is_button_able_to_select = True
                if "selected" in button_class_string:
                    is_button_able_to_select = False
                    ret = True
                    #print("button is selected:", button_class_string, time_picker_text)

                    # no need more loop.
                    break

                if "full" in button_class_string:
                    is_button_able_to_select = False
                    if target_time in time_picker_text:
                        #print("button is full:", button_class_string, time_picker_text)
                        fail_code = 100

                        # no need more loop.
                        break
                
                if is_button_able_to_select:
                    if target_time in time_picker_text:
                        is_able_to_click = True
                        if is_able_to_click:
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
                                try:
                                    driver.execute_script("console.log(\"click to button.\");")
                                    driver.execute_script("arguments[0].click();", el_time_picker)
                                except Exception as exc:
                                    pass
                        else:
                            fail_code = 200
                            print("target button is not viewable or not enable.")
                            pass

        if not is_one_of_time_picket_viewable:
            fail_code = 1
    return ret, fail_code

def assign_adult_picker(driver, adult_picker, force_adult_picker):
    is_adult_picker_assigned = False

    # member number.
    el_adult_picker = None
    try:
        el_adult_picker = driver.find_element(By.ID, 'adult-picker')
    except Exception as exc:
        pass
    
    if not el_adult_picker is None:
        is_visible = False
        try:
            if el_adult_picker.is_enabled():
                is_visible = True
        except Exception as exc:
            pass

        if is_visible:
            selected_value = None
            try:
                selected_value = str(el_adult_picker.get_attribute('value'))
                #print('seleced value:', selected_value)
            except Exception as exc:
                pass

            if selected_value is None:
                selected_value = ""
            
            if selected_value == "":
                selected_value = "0"

            is_need_assign_select = True
            if selected_value != "0":
                # not is default value, do assign.
                is_need_assign_select = False
                is_adult_picker_assigned = True

                if force_adult_picker:
                    if selected_value != adult_picker:
                        is_need_assign_select = True

            if is_need_assign_select:
                #print('assign new value("%s") for select.' % (adult_picker))
                adult_number_select = Select(el_adult_picker)
                try:
                    adult_number_select.select_by_value(adult_picker)
                    is_adult_picker_assigned = True
                except Exception as exc:
                    print("select_by_value for adult-picker fail")
                    print(exc)
                    pass

    return is_adult_picker_assigned

def assign_time_picker(driver, book_now_time, book_now_time_alt):
    show_debug_message = True       # debug.
    #show_debug_message = False      # online

    ret = False

    el_time_picker_list = None
    button_query_string = 'button.time-slot'
    try:
        el_time_picker_list = driver.find_elements(By.CSS_SELECTOR, button_query_string)
    except Exception as exc:
        if show_debug_message:
            print("find time buttons excpetion:", exc)
        pass

    if not el_time_picker_list is None:
        el_time_picker_list_size = len(el_time_picker_list)
        if show_debug_message:
            print("el_time_picker_list_size:", el_time_picker_list_size)

        if el_time_picker_list_size > 0:
            # default use main time.
            book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time)
            
            if show_debug_message:
                print("booking target time:", book_now_time)
                print("book_time_ret, book_fail_code:", book_time_ret, book_fail_code)
            
            if not book_time_ret:
                if book_fail_code >= 200:
                    # [200,201] ==> retry
                    # retry main target time.
                    book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time)
                    if show_debug_message:
                        print("retry booking target time:", book_time_ret, book_fail_code)
                else:
                    # try alt time.
                    book_time_ret, book_fail_code = book_time(el_time_picker_list, book_now_time_alt)
                    if show_debug_message:
                        print("booking ALT time:", book_now_time_alt)
                        print("booking ALT target time:", book_time_ret, book_fail_code)
        else:
            if show_debug_message:
                print("time element length zero...")
    else:
        if show_debug_message:
            print("not found time elements.")

    
    return ret

def inline_reg(driver, config_dict):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

    ret = False

    house_rules_ret = is_House_Rules_poped(driver)

    if show_debug_message:
        print("house_rules_ret:", house_rules_ret)

    if not house_rules_ret:
        adult_picker = config_dict["adult_picker"]
        force_adult_picker = config_dict["force_adult_picker"]

        # date picker.
        is_adult_picker_assigned = assign_adult_picker(driver, adult_picker, force_adult_picker)
        if show_debug_message:
            print("is_adult_picker_assigned:", is_adult_picker_assigned)

        if not is_adult_picker_assigned:
            # retry once.
            is_adult_picker_assigned = assign_adult_picker(driver, adult_picker, force_adult_picker)
            if show_debug_message:
                print("retry is_adult_picker_assigned:", is_adult_picker_assigned)

        # time picker.
        book_now_time = config_dict["book_now_time"]
        book_now_time_alt = config_dict["book_now_time_alt"]
        if is_adult_picker_assigned:
            ret = assign_time_picker(driver, book_now_time, book_now_time_alt)
            if show_debug_message:
                print("assign_time_picker return:", ret)

    return ret

def get_current_url(driver):
    DISCONNECTED_MSG = ': target window already closed'

    url = ""
    is_quit_bot = False

    try:
        url = driver.current_url
    except NoSuchWindowException:
        print('NoSuchWindowException at this url:', url )
        #print("last_url:", last_url)
        #print("get_log:", driver.get_log('driver'))
        window_handles_count = 0
        try:
            window_handles_count = len(driver.window_handles)
            #print("window_handles_count:", window_handles_count)
            if window_handles_count >= 1:
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.default_content()
                time.sleep(0.2)
        except Exception as excSwithFail:
            #print("excSwithFail:", excSwithFail)
            pass
        if window_handles_count==0:
            try:
                driver_log = driver.get_log('driver')[-1]['message']
                print("get_log:", driver_log)
                if DISCONNECTED_MSG in driver_log:
                    print('quit bot by NoSuchWindowException')
                    is_quit_bot = True
                    driver.quit()
                    sys.exit()
            except Exception as excGetDriverMessageFail:
                #print("excGetDriverMessageFail:", excGetDriverMessageFail)
                except_string = str(excGetDriverMessageFail)
                if 'HTTP method not allowed' in except_string:
                    print('quit bot by close browser')
                    is_quit_bot = True
                    driver.quit()
                    sys.exit()

    except UnexpectedAlertPresentException as exc1:
        print('UnexpectedAlertPresentException at this url:', url )
        # PS: do nothing...
        # PS: current chrome-driver + chrome call current_url cause alert/prompt dialog disappear!
        # raise exception at selenium/webdriver/remote/errorhandler.py
        # after dialog disappear new excpetion: unhandled inspector error: Not attached to an active page
        is_pass_alert = False
        is_pass_alert = True
        if is_pass_alert:
            try:
                driver.switch_to.alert.accept()
            except Exception as exc:
                pass

    except Exception as exc:
        logger.error('Maxbot URL Exception')
        logger.error(exc, exc_info=True)

        #UnicodeEncodeError: 'ascii' codec can't encode characters in position 63-72: ordinal not in range(128)
        str_exc = ""
        try:
            str_exc = str(exc)
        except Exception as exc2:
            pass

        if len(str_exc)==0:
            str_exc = repr(exc)

        exit_bot_error_strings = ['Max retries exceeded'
        , 'chrome not reachable'
        , 'unable to connect to renderer'
        , 'failed to check if window was closed'
        , 'Failed to establish a new connection'
        , 'Connection refused'
        , 'disconnected'
        , 'without establishing a connection'
        , 'web view not found'
        , 'invalid session id'
        ]
        for each_error_string in exit_bot_error_strings:
            if isinstance(str_exc, str):
                if each_error_string in str_exc:
                    print('quit bot by error:', each_error_string)
                    is_quit_bot = True
                    driver.quit()
                    sys.exit()

        # not is above case, print exception.
        print("Exception:", str_exc)
        pass

    return url, is_quit_bot

def main(args):
    config_dict = get_config_dict(args)

    driver = None
    if not config_dict is None:
        driver = get_driver_by_config(config_dict)
    else:
        print("Load config error!")

    # internal variable. 說明：這是一個內部變數，請略過。
    url = ""
    last_url = ""

    while True:
        time.sleep(0.05)

        # pass if driver not loaded.
        if driver is None:
            print("web driver not accessible!")
            break

        url, is_quit_bot = get_current_url(driver)
        if is_quit_bot:
            break

        if url is None:
            continue
        else:
            if len(url) == 0:
                continue

        is_maxbot_paused = False
        if os.path.exists(CONST_MAXBOT_INT28_FILE):
            is_maxbot_paused = True

        if len(url) > 0 :
            if url != last_url:
                print(url)
                write_last_url_to_file(url)
                if is_maxbot_paused:
                    print("MAXBOT Paused.")
            last_url = url

        if is_maxbot_paused:
            time.sleep(0.2)
            continue

        if len(url) > 0 :
            if url != last_url:
                print(url)
            last_url = url

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
                            ret = fill_personal_info(driver, config_dict)
                        else:
                            # select date.
                            ret = inline_reg(driver, config_dict)


def cli():
    parser = argparse.ArgumentParser(
            description="MaxBot Aggument Parser")

    parser.add_argument("--input",
        help="config file path",
        type=str)

    parser.add_argument("--homepage",
        help="overwrite homepage setting",
        type=str)

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
