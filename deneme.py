PATH = "C:\Program Files (x86)\chromedriver.exe"
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome(PATH)

formatted_lines = []
car_driver = webdriver.Chrome(PATH)
car_driver.get("https://dod.com.tr/arac-detay/volkswagen/golf/233441447")
WebDriverWait(driver, 15).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "do-search-result-table__container__cards")))
    
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

data2 = []

for rapor in ekspertiz:
    data2.append(rapor.text)
    
data = []
for car_specs in formatted_lines:
    for spec in car_specs:
        value = spec.text
        data.append(value)
    

for i in range(3,9):
    data[i] = data[i].split("\n")[1]

del data[8:12]

if(len(data2) > 0):
    updated_list = [entry.replace('\n', ':') for entry in data2]

new_data = data + updated_list

with open('output2.txt', 'a', encoding='utf-8') as file:
    file.write(';'.join(map(str, new_data)) + '\n')
















driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://dod.com.tr/arac-detay/volkswagen/golf/233441447")
sleep(5)

ekspertiz = driver.find_elements(By.CLASS_NAME, "do-vehicle-expert-report-section__description-item")
data = []
for rapor in ekspertiz:
    data.append(rapor.text)

if(len(data) > 0):
    updated_list = [entry.replace('\n', ':') for entry in data]

print(updated_list)

























# Find the SVG element
svg_element = driver.find_element(By.XPATH, "//*[local-name()='svg' and @class='do-expert-vehicle-report__image']")

# Get the SVG content
svg_content = svg_element.get_attribute("outerHTML")

def convert_svg_to_png(input_svg, output_png):
    # Read the SVG file
    with open(input_svg, 'rb') as svg_file:
        # Create a Wand Image object from the SVG content
        with Image(blob=svg_file.read(), format='svg') as img:
            # Convert the image to PNG format
            img.format = 'png'

            # Save the PNG file
            img.save(filename=output_png)

with open('./output.svg', 'r') as svg_file:
    content = svg_file.read()
with open('./output.png', 'r') as svg_file:
    png_file = svg_file.read()

# Example usage
input_svg_file = 'input.svg'
output_png_file = 'output.png'

convert_svg_to_png(content, png_file)

# Save the SVG content to a file
with open("output.svg", "w", encoding="utf-8") as svg_file:
    svg_file.write(svg_content)



# Close the WebDriver
driver.quit()
