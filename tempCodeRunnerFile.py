PATH = "C:\Program Files (x86)\chromedriver.exe"
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome(PATH)
driver.maximize_window()

for page in range(16,18):
    driver.get("https://dod.com.tr/arac-arama?page=" + str(page))
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "do-search-result-table__container__cards")))
    cars = driver.find_elements(By.CLASS_NAME, 'do-vehicle-card__preview')
    car_links = []
    car_num = 1
    for car in cars:
        href = car.find_element(By.XPATH,"//*[@id='__layout']/div/div[3]/main/div[2]/div[2]/div[2]/div[3]/div/div[1]/div["+str(car_num)+"]/div/div[1]/div/a").get_attribute('href')
        car_num += 1
        car_links.append(href)

    formatted_line = []

    for car in car_links:

        formatted_lines = []

        car_driver = webdriver.Chrome(PATH)
        car_driver.get(car)
        WebDriverWait(car_driver, 15).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "do-vehicle-detail-primary-info__price-text")))
            
        price = car_driver.find_elements(By.CLASS_NAME,"do-vehicle-detail-primary-info__price-text")
        modal = car_driver.find_elements(By.CLASS_NAME,"do-vehicle-detail-primary-info__model")
        brand = car_driver.find_elements(By.CLASS_NAME,"do-vehicle-detail-primary-info__brand")
        details = car_driver.find_elements(By.CLASS_NAME,"do-vehicle-detail-info-section__other-specs__item__value")
        info = car_driver.find_elements(By.CLASS_NAME,"do-vehicle-detail-info-section__featured-specs__item__body")
        ekspertiz = car_driver.find_elements(By.CLASS_NAME, "do-vehicle-expert-report-section__description-item")
        formatted_lines.append(modal)
        formatted_lines.append(brand)
        formatted_lines.append(price)
        formatted_lines.append(info)
        formatted_lines.append(details)
            
        data = []
        for car_specs in formatted_lines:
            for spec in car_specs:
                value = spec.text
                data.append(value)
            
        
        for i in range(3,9):
            data[i] = data[i].split("\n")[1]

        del data[8:12]

        data2 = []
        for rapor in ekspertiz:
            data2.append(rapor.text)

        if(len(data2) > 0):
            updated_list = [entry.replace('\n', ':') for entry in data2]
            data = data + updated_list

        with open('output2.txt', 'a', encoding='utf-8') as file:
            file.write(';'.join(map(str, data)) + '\n')

        car_driver.close()

            