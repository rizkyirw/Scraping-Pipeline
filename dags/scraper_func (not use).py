# Import the Library
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date
import pandas as pd

# Scrape Function
def scrap_data_A():

    # Set up ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # On the newest selenium and webdriver_manager version, just add "=new" on the headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Set up Selenium WebDriver with ChromeDriver executable path inside options
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://sp2kp.kemendag.go.id/"

    # Load the webpage
    driver.get(url)

    # Wait for the table element to be present
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "datatable_harga_keb_pokok")))

    # Verify if the table element is present on the page
    if table is None:
        print("Table with ID 'datatable_harga_keb_pokok' not found on the page.")
    else:
        # Extract the table data and store it in a list
        data = []

        # Extract the table head
        thead = table.find_element(By.CLASS_NAME, "Beranda_theadDtTable__sp6_g")
        headers = [header.text.strip() for header in thead.find_elements(By.TAG_NAME, "th")]

        # Extract the table rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            row_data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            if len(row_data) == len(headers):  # Ensure the number of items in each row matches the number of columns
                data.append(row_data)
            else:
                print(f"Skipping row: {row_data} as the number of items doesn't match the number of columns.")

        # Create a Pandas DataFrame from the extracted data
        df = pd.DataFrame(data, columns=headers)

        # Save the DataFrame to a CSV file with the current date in the file name
        output_file = f"./dags/data_bahan_pokok_scrap_{date.today()}.csv"
        df.to_csv(output_file, index=False, header=False)
        print("Data saved to", output_file)
    
    # Close the WebDriver
    driver.quit()
