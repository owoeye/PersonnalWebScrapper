import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# website for web scrapping
LIST_URL = "https://steamdb.info/charts/"

# # Keeps browser open
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)

service = Service("C:\Development\chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

driver.get(LIST_URL)
driver.find_element(By.XPATH, '//*[@id="dt-length-0"]/option[8]').click()

soup = BeautifulSoup(driver.page_source, "html.parser")
table_header = soup.find_all(name="span", class_="dt-column-title")
table_header = [col_title.getText() for col_title in table_header]
print(table_header)

table_matrix = []
table_data = soup.find_all(name="tr", class_="app")
for table_row in table_data:
    row = table_row.find_all(name="td")
    data_list = []
    for data in row:
        if data.getText() == "":
            link = data.find(name="a").get("href")
            data_list.append(f"https://steamdb.info{link}")
        else:
            data_list.append(data.getText())

    table_matrix.append(data_list)

table_values = [[row[col] for row in table_matrix] for col in range(len(table_header))]
table_dict = {header: value for (header, value) in zip(table_header, table_values)}
table_df = pd.DataFrame(table_dict)
# print(table_df)

table_df.to_csv("webscraped.csv", index=False)
