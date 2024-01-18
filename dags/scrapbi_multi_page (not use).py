# Import Library
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define a function to search for the keyword and return the search results URL for a specific page
def search_keyword_page(keyword, page):
    base_url = "https://search.bisnis.com/"
    search_url = f"{base_url}?q={keyword}&per_page={page}"
    return search_url

# Define a function to scrape data from a specific search results page
def scrape_search_results_page(driver, search_url):
    try:
        driver.get(search_url)

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
                "Title": title.replace('"', ''),
                "Link": link_element,
                "Tag": tag,
                "Date": date,
                "Description": description,
            })

        return results

    except Exception as e:
        print("Error:", e)
        return []

# Define a function to scrape data from multiple search results pages
def scrape_search_results(keyword, max_pages):
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

    all_results = []

    for page in range(1, max_pages + 1):
        search_url = search_keyword_page(keyword, page)
        search_results = scrape_search_results_page(driver, search_url)

        if search_results:
            all_results.extend(search_results)
        else:
            break  # Stop scraping if no results found on a page

    driver.quit()
    return all_results

if __name__ == "__main__":
    keyword = "UMKM"  # Replace with your desired keyword here (Oleh-oleh, sembako, makanan olahan, minuman olahan)
    max_pages = 1  # Set the maximum number of pages to scrape (edit : 20)

    all_results = scrape_search_results(keyword, max_pages)

    if all_results:
        df = pd.DataFrame(all_results)
        output_file = f"./dags/bisnis_search_results_multi_page_{date.today()}.csv"
        df.to_csv(output_file, index=False, sep=";")
        print(f"Scraped {len(all_results)} search results and saved to {output_file}")
    else:
        print("No search results found.")