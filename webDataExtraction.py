from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        bright_star_table = soup.find("table", attrs={"class","wikitable"})
        table_body = bright_star_table.find('tbody')
        table_rows = table_body.find_all('tr')

        for row in table_rows:
            table_cols = row.find_all('td')
            #print(table_cols)
            temp_list = []

            for col_data in table_cols:
                #print(col_data.text)
                data = col_data.text.strip()
                #print(data)
                temp_list.append(data)
            for index, table_rows in enumerate(table_rows):
                if index == 0:
                    temp_list.append(table_rows.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(table_rows.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_li_tag = table_rows[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            scraped_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


# Calling Method
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Define pandas DataFrame 
planet_df_1 = pd.DataFrame(scraped_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv',index=True, index_label="id")