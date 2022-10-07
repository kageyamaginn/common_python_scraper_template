from ast import Str
from ctypes.wintypes import BOOLEAN
import enum
from http.client import SWITCHING_PROTOCOLS
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import sysinfo

from bs4 import BeautifulSoup


from selenium.webdriver.common.action_chains import ActionChains

pip_path:str = 'c:/'
driver_path='chromedriver.exe'


def precheck():
    # check if selenium package is install
    print(sysinfo.WinSys.version())
    # check if current chrome driver version match chrome app version
    try:
        driver = webdriver.Chrome(driver_path)
        driver.quit()
    except Exception as ex:
        if type(ex) is selenium.common.exceptions.SessionNotCreatedException:
            print("chromedriver version not match with chrome,download the corresponding version from: https://chromedriver.chromium.org/downloads")

class ChromeDriverOption():
    def __init__(self):
        self.path = driver_path
    path:Str
    headless = False
    download_path:Str

def addHttpsPrefix(url:Str):
    if url.startswith('https') or url.startswith('http'):
        return url
    else:
        return 'https://'+url


class Element:

    def __init__(self,ele:WebElement,driver:webdriver.Chrome) -> None:
        self.ele = ele
        self.driver = driver

    def action(self) -> ActionChains:
        return ActionChains(self.driver)

    def click(self):
        if self.ele.is_displayed():
            self.ele.click()
        else:
            self.action().scroll_to_element(self.ele).click().perform()
        return self
    
    def input(self,text):
        self.ele.send_keys(text)
        return self

    def text(self)->Str:
        return self.ele.get_attribute('innerText')

    def find_elements(self, xpath:Str,wait=30,delay=0):
        '''
        please start with .//
        like .//div
        '''
        try:
            WebDriverWait(self.driver,wait).until(EC.presence_of_element_located((By.XPATH,xpath)))
        except Exception as ex:
            return None
        if delay>0:
            time.sleep(delay)
        return [Element(item,self.driver) for item in self.ele.find_elements(by=By.XPATH,value=xpath)]

    def hover(self):
        self.action().move_to_element(self.ele).perform()

class ChromeTab:
    def name(self):
        return self.name

    def __init__(self,driver:webdriver.Chrome,handle:Str,name:Str) -> None:
        self.driver = driver
        self.handle = handle
        self.name=name

    def refresh(self):
        self.driver.refresh()

    def index(self):
        return self.driver.window_handles.index(self.handle)

    def redirect(self,url:Str):
        self.driver.get(addHttpsPrefix(url))
    
    def switch(self):
        self.driver.switch_to.window(self.handle)

    def to_frame(self, id:Str):
        '''
        id: frame name/id
        you can use frame_id1.frame_id2 for convience
        '''
        frames = id.split('.')
        self.driver.switch_to.default_content()
        for f in frames:
            self.wait('//iframe[@name="{}" or @id="{}"]'.format(f,f))
            self.driver.switch_to.frame(f)
    
    def close(self):
        self.switch()
        self.driver.close()

    def find_elements(self, xpath:Str,wait=30,delay=0):
        try:
            WebDriverWait(self.driver,wait).until(EC.presence_of_element_located((By.XPATH,xpath)))
        except Exception as ex:
            return []
        if delay>0:
            time.sleep(delay)
        return [Element(item,self.driver) for item in self.driver.find_elements(by=By.XPATH,value=xpath)]

    def wait(self, xpath:str,timeout:int=30) -> BOOLEAN:
        try:
            WebDriverWait(self.driver,timeout).until(EC.visibility_of_all_elements_located((By.XPATH,xpath)))
            return True
        except Exception as ex:
            return False
    def source(self):
        return PageSource(self.driver.page_source)

class PageSource:
    def __init__(self,source:Str):
        self.soup = BeautifulSoup(source,'html.parser')
    
    def sp(self)->BeautifulSoup:
        return self.soup

class ChromeDriver:

    driver: webdriver.Chrome

    tabs={Str:ChromeTab}

    def __init__(self,opt:ChromeDriverOption) -> None:
        self.__create_chrome(opt=opt)

    def __create_chrome(self, opt:ChromeDriverOption)->webdriver.Chrome:
        if opt is not None:
            options = self.__consumeOptions(opt)
        try:
            self.driver = webdriver.Chrome(opt.path,options=options)
            self.tabs[self.driver.window_handles[0]]= ChromeTab(self.driver,self.driver.window_handles[0],name="default")
        except Exception as ex:
            if type(ex) is selenium.common.exceptions.SessionNotCreatedException:
                print("chromedriver version not match with chrome,download the corresponding version from: https://chromedriver.chromium.org/downloads")

    def __consumeOptions(self,opt:ChromeDriverOption):
        options = webdriver.ChromeOptions()
        options.headless = opt.headless
        if opt.__dict__.get("download_path") is not None:
            self.sendCommand({'cmd':'Page.setDownloadBehavior','params':{'behavior':'allow'}})
        return options

    def sendCommand(self,params:object):
        # add missing support for chrome "send_command"  to selenium webdriver
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        self.driver.execute(params)


    def open(self, url:Str,valid:str=None)->ChromeTab:
        curr_tab=self.tabs[self.driver.current_window_handle]
        curr_tab.redirect(url=url)
        if valid is not None:
            if curr_tab.find_elements(valid,5)==None:
                curr_tab.refresh()
                curr_tab.find_elements(valid)
        return self.tabs[self.driver.current_window_handle]

    def openNewTab(self, url:Str=None,name:Str=None)->ChromeTab:
        handle= self.driver.switch_to.new_window()
        self.tabs[self.driver.current_window_handle] = ChromeTab(driver=self.driver,handle=self.driver.current_window_handle,name=name)
        if url is not None:
            self.open(url)
        
        return self.tabs[self.driver.current_window_handle]
    
    def find_tab_by_name(self, name:Str) -> ChromeTab:
        for tab in self.tabs.values():
            if tab.name == name:
                return tab
        return None

    def switch_2_next_tab(self,step=1):
        handles= self.driver.window_handles
        
        curr_tab_index = handles.index(self.driver.current_window_handle())
        if curr_tab_index == len(handles)-1:
            self.driver.switch_to.window(handles[0])
        else:
            self.driver.switch_to.window(handles[curr_tab_index+step])

    def refreshTabs(self,switch_to_new_tab:BOOLEAN=True)->ChromeTab:
        new_tabs={}
        new_tab_handles=[]
        for t_handle in self.driver.window_handles:
            old_tab = self.tabs.get(t_handle)
            if old_tab ==None:
                new_tab_handles.append(t_handle)
                new_tabs[t_handle] = ChromeTab(self.driver,t_handle,None)
            else:
                new_tabs[t_handle] = old_tab
        
        self.tabs = new_tabs
        if switch_to_new_tab and len(new_tab_handles)>0:
            self.driver.switch_to.window(new_tab_handles[0])
            return new_tabs[new_tab_handles[0]]
        
        


        
