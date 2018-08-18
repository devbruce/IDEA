from selenium import webdriver
import os
import urllib
import time

def sna_auto_crawler(keyword, page_range=3):
    data_list = []
    encoded_kw = urllib.parse.quote(u'{}'.format(keyword).encode('utf-8'))
    url = "https://www.google.co.kr/search?num=100&hl=ko&q={kw}&oq={kw}".format(kw=encoded_kw)
    driver = webdriver.PhantomJS(os.path.join(os.getcwd(),"additional/webdrivers/phantomjs"))
    driver.get(url)

    time.sleep(3)

    for st_data in driver.find_elements_by_class_name("st"):
        data_list.append(st_data.text)

    for page in range(2, page_range+1):
        try: driver.find_element_by_xpath("//span[@style='display:block;margin-left:53px']").click()
        except: break

        time.sleep(3)

        for st_data in driver.find_elements_by_class_name("st"):
            data_list.append(st_data.text)

    driver.quit()
    return data_list


def wc_auto_crawler(keyword, page_range=3):
    data_raw = ""
    encoded_kw = urllib.parse.quote(u'{}'.format(keyword).encode('utf-8'))
    url = "https://www.google.co.kr/search?num=100&hl=ko&q={kw}&oq={kw}".format(kw=encoded_kw)
    driver = webdriver.PhantomJS(os.path.join(os.getcwd(),"additional/webdrivers/phantomjs"))
    driver.get(url)

    time.sleep(3)

    for st_data in driver.find_elements_by_class_name("st"):
        data_raw += st_data.text
        data_raw += "\s"

    for page in range(2, page_range+1):
        try: driver.find_element_by_xpath("//span[@style='display:block;margin-left:53px']").click()
        except: break

        time.sleep(3)

        for st_data in driver.find_elements_by_class_name("st"):
            data_raw += st_data.text
            data_raw += "\s"

    driver.quit()   
    return data_raw