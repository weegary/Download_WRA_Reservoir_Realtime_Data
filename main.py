# -*- coding: utf-8 -*- 
""" 
Created on Thu Aug 18 14:41:21 2022 
@author: Gary Wee
@info: This program downloads real time data for that month of a reservoir from WRA website.
""" 

import bs4 
import requests 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select  # ComboBox 
import time

driverpath='chromedriver.exe'  # from https://chromedriver.chromium.org/downloads
browser= webdriver.Chrome(driverpath) 
url='https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx' 
browser.get(url) 

#%% CSS Selector 
table_css = '#ctl00_cphMain_gvList' 
combobox_year_css = '#ctl00_cphMain_ucDate_cboYear' 
combobox_month_css = '#ctl00_cphMain_ucDate_cboMonth' 
combobox_day_css = '#ctl00_cphMain_ucDate_cboDay' 
btn_search_css='#ctl00_cphMain_btnQuery' 

#%% 
combobox_day = Select(browser.find_element(By.CSS_SELECTOR, combobox_day_css)) 
selected_day = combobox_day.first_selected_option
selected_day = int(selected_day.text)
for i in range(1,selected_day+1):
    combobox_day = Select(browser.find_element(By.CSS_SELECTOR, combobox_day_css)) 
    combobox_day.select_by_value(str(i)) 
    btn_search= browser.find_element(By.CSS_SELECTOR, btn_search_css) 
    btn_search.click() 
    time.sleep(1)
    table = browser.find_element(By.CSS_SELECTOR, table_css) 
    t = table.get_attribute('outerHTML') 
    objsoup = bs4.BeautifulSoup(t,'lxml') 
    all_rows = objsoup.find_all('tr') 
    for r in all_rows: 
        if (len(r.find_all('td')) != 0): 
            if ((r.find_all('td')[0].text) == '集集攔河堰'): 
                for col in r.find_all('td'): 
                    print(col.text.strip()) 
    print('')

browser.close()
