# Import the Library
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date
import pandas as pd

# Scrape Function
def scrap_data_A(**kwargs):

    # Set up ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
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

            # Check if row_data is not empty before accessing its elements
            if row_data:
                # Remove leading comma from the first element
                row_data[0] = row_data[0].lstrip(',')

                # Skip the first column before "Komoditas"
                data.append(row_data[1:])  # Skip the first column

        # Create a Pandas DataFrame from the extracted data
        df = pd.DataFrame(data, columns=headers[1:])  # Skip the first column in headers as well

        # Save the DataFrame to a CSV file with the current date in the file name
        current_date = date.today().strftime("%Y-%m-%d")
        output_file = f'/data/data_bahan_pokok_scrap_{current_date}.csv'
        df.to_csv(output_file, index=False, header=False, sep=";")
        print("Data saved to", output_file)

        # Push the DataFrame to XCom for other tasks to access
        kwargs['ti'].xcom_push(key='data_frame', value=df)

    # Close the WebDriver
    driver.quit()
