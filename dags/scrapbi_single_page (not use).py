# Import Library
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define a function to search for the keyword and return the search results URL
def search_keyword(keyword):
    base_url = "https://search.bisnis.com/"
    search_url = f"{base_url}?q={keyword}"
    return search_url

# Define a function to scrape data from the search results page
def scrape_search_results(search_url):
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

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(search_url)

    try:
        # Wait for the search results to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list-news")))

        # Get the HTML content of the page
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract data from the search results
        results = []

        for item in soup.select(".list-news li"):
            title_element = item.select_one("h2 a")
            title = title_element.text.strip() if title_element else ""

            link_element = title_element["href"] if title_element else ""

            tag_element = item.select_one(".channel a")
            tag = tag_element.text.strip() if tag_element else ""

            date_element = item.select_one(".date")
            date = date_element.text.strip() if date_element else ""

            description_element = item.select_one(".description")
            description = description_element.text.strip() if description_element else ""

            results.append({
                "Title": title.replace('"', ''),  # Remove double quotes from the title
                "Link": link_element,
                "Tag": tag,
                "Date": date,
                "Description": description,
            })

        return results

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = "umkm"  # Replace with your desired keyword
    search_url = search_keyword(keyword)
    search_results = scrape_search_results(search_url)

    if search_results:
        df = pd.DataFrame(search_results)
        df.to_csv("bisnis_search_results_single_page.csv", index=False, sep=";")  # Set delimiter to semicolon
        print(f"Scraped {len(search_results)} search results and saved to bisnis_search_results.csv")
    else:
        print("No search results found.")