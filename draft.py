from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

filename = "data"
directory = 'C:/Users/HOME/PycharmProjects/DA_ConstructionMarketplaces/'
link = "https://www.google.com/maps/search/%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5+%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D1%8B+%D1%81%D0%B7%D1%84%D0%BE/@43.2928347,11.5631002,4z/data=!3m1!4b1"
browser = webdriver.Chrome()
record = []
e = []
le = 0

def Selenium_extractor():

    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le+=1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})

            name = Name_Html[0].text
            if name not in e:
                e.append(name)
                divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
                for j in range(len(divs)):
                    if str(divs[j].text)[0] == "+":
                        phone = divs[j].text

                Address_Html= divs[0]
                address=Address_Html.text
                try:
                    for z in range(len(divs)):
                        if str(divs[z].text)[-4] == "." or str(divs[z].text)[-3] == ".":
                            website = divs[z].text
                except:
                    website="Not available"
                print([name,phone,address,website])
                record.append((name,phone,address,website))
                df=pd.DataFrame(record,columns=['Name','Phone number','Address','Website'])  # writing data to the file
                df.to_csv(directory + 'data.csv', index=False, encoding='utf-8-sig')
        except:
            print("error")
            continue



browser.get(str(link))
time.sleep(5)
Selenium_extractor()