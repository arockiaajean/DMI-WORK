from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Step 1: Set up Selenium with Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 2: Load the webpage
url = 'https://mycollegevcampus.com/dmiseu/ADMISSION/viewstudentsup.php?username=&role=Registrar-IVDL'  # Replace with the actual URL
driver.get(url)

# Wait for content to load (adjust time as needed)
time.sleep(5)

# Step 3: Retrieve HTML after JavaScript loads and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # Close the browser

# Step 4: Extract data (modify this part based on webpage structure)
data = []
table = soup.find('table')  # Modify to locate the specific element with the data

if table:
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        data_row = [col.text.strip() for col in columns]
        if data_row:
            data.append(data_row)

# Step 5: Convert to DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('full_webpage_data15.11.2024.xlsx', index=False)
print("Data saved to 'full_webpage_data14.11.xlsx' successfully!")

