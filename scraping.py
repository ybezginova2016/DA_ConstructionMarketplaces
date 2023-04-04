import time
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

start_time = time.time()
# cities = ['Санкт-Петербург', 'спб', 'питер', 'сзфо', 'петербург', 'ленобласть', 'санкт петербург', 'Ленинградская область',
#           'Архангельская область', 'Вологодская область', 'Псковская область', 'Новгородская область',
#           'Ненецкий автономный округ', 'Мурманская область', 'Республика Коми',
#           'Республика Карелия', 'Калининградская область']

link1 = "https://www.google.com/maps/search/строительные+магазины+спб/"
link2 = "https://www.google.com/maps/search/строительные+магазины+ленобласть/"
link3 = "https://www.google.com/maps/search/строительные+магазины+санкт+петербург/"
link4 = "https://www.google.com/maps/search/строительные+магазины+Ленинградская+область/"
link5 = "https://www.google.com/maps/search/строительные+магазины+Архангельская+область/"
link6 = "https://www.google.com/maps/search/строительные+магазины+Республика+Карелия/"
link7 = "https://www.google.com/maps/search/строительные+магазины+Вологодская+область"
link8 = "https://www.google.com/maps/search/строительные+магазины+Псковская+область"
link9 = "https://www.google.com/maps/search/строительные+магазины+Новгородская+область"
link10 = "https://www.google.com/maps/search/строительные+магазины+Ненецкий+автономный+округ"
link11 = "https://www.google.com/maps/search/строительные+магазины+Мурманская+область"
link12 = "https://www.google.com/maps/search/строительные+магазины+Республика+Коми"
link13 = "https://www.google.com/maps/search/строительные+магазины+Калининградская+область"
# link14 = "https://www.google.com/maps/search/строительные+магазины+СЗФО/"

links = [link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12, link13]

directory = 'C:/Users/HOME/PycharmProjects/DA_ConstructionMarketplaces/'
browser = webdriver.Chrome()

record = []
e = []
le = 0

def Selenium_extractor():
    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    while len(a) < 500:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a) - 1])
        action.scroll_from_origin(scroll_origin, 0, 500).perform()
        time.sleep(30)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le += 1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 500).perform()
        action.move_to_element(a[i]).perform()
        wait = WebDriverWait(browser, 30)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc")))
        try:
            browser.execute_script("arguments[0].click();", a[i])
        except WebDriverException:
            continue

        time.sleep(20)
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

                Address_Html = divs[0]
                address = Address_Html.text
                try:
                    for z in range(len(divs)):
                        if str(divs[z].text)[-4] == "." or str(divs[z].text)[-3] == ".":
                            website = divs[z].text
                except:
                    website = "Not available"
                print([name, phone, address, website])
                record.append((name, phone, address, website))
                df = pd.DataFrame(record, columns=['Name', 'Phone', 'Address', 'Website'])  # writing data to the file
                df.to_csv(directory + 'data.csv', index=False, encoding='utf-8-sig')
        except:
            print("error")
            continue


# Loop through the links
for link in links:
    browser.get(link)
    time.sleep(30)
    le = 0 # Initialize the counter le
    Selenium_extractor()

browser.quit()

end_time = time.time()

total_time = end_time - start_time
print(f"Total execution time: {total_time:.2f} seconds")