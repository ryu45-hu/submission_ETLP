from datetime import datetime
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Mengumpulkan konten
def collect_content(url):
    try:
        respons = requests.get(url, headers=HEADERS)
        respons.raise_for_status()
        return respons.content
    except requests.exceptions.RequestException as e:
        print(f"Error Collecting {url}: {e}")
        return None

# Analisis html product
def extract_product(card):
    title = card.find("h3", class_="product-title")
    price = card.find("span", class_="price")
    details = card.find_all("p")

    return {
        "Title": title.text.strip() if title else "Unknown",
        "Price": price.text.strip() if price else "Price Unavailable",
        "Rating": details[0].text.strip() if len(details) > 0 else "Invalid Rating / 5",
        "Colors": details[1].text.strip() if len(details) > 1 else "-",
        "Size": details[2].text.strip() if len(details) > 2 else "-",
        "Gender": details[3].text.strip() if len(details) > 3 else "-",
        "Timestamp": datetime.now().isoformat(sep=' ', timespec='microseconds')
    }

# Fungsi scraping mengambil dari URL
def scraping_product(page1, pages_url, start_page=1, end_page=50, delay=1):
    content_data = []

    for page in range(start_page, end_page + 1):
        if page == 1:
            url = page1
        else:
            url = pages_url.format(page)

        print(f"Scraping: {url}")
        content = collect_content(url)
        if not content:
            continue

        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all("div", class_="collection-card")

        for card in cards:
            product = extract_product(card)
            content_data.append(product)

        time.sleep(delay)

    return pd.DataFrame(content_data)
