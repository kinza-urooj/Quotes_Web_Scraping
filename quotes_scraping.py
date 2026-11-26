import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from pathlib import Path

# Website URL
base_url = "https://quotes.toscrape.com/"

# Create data folder
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

# Headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Store quotes
quotes_data = []

# Starting page
current_url = base_url

# Create session
session = requests.Session()
session.headers.update(headers)

# Scrape multiple pages
while current_url:

    print("Scraping:", current_url)

    try:
        response = session.get(current_url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find quotes on current page
        quote_blocks = soup.select("div.quote")

        # Stop if no quotes found
        if not quote_blocks:
            print("No quotes found on this page.")
            break

        # Extract data from each quote
        for block in quote_blocks:

            # Quote text
            quote_text = block.select_one("span.text").get_text(strip=True)

            # Author name
            author = block.select_one("small.author").get_text(strip=True)

            # Author profile URL
            author_link = block.select_one("a[href*='/author/']")

            if author_link:
                author_url = requests.compat.urljoin(
                    current_url, author_link["href"]
                )
            else:
                author_url = None

            # Tags
            tags = [
                tag.get_text(strip=True)
                for tag in block.select("a.tag")
            ]

            # Store data
            quote_record = {
                "quote": quote_text,
                "author": author,
                "tags": tags,
                "author_url": author_url,
                "page_url": current_url
            }

            quotes_data.append(quote_record)

        # Find next page
        next_button = soup.select_one("li.next a")

        if next_button:
            next_page = next_button["href"]

            current_url = requests.compat.urljoin(
                current_url, next_page
            )
        else:
            current_url = None

        # Be polite to the website
        time.sleep(1)

    except requests.exceptions.RequestException as error:
        print("Website request error:", error)
        break

    except Exception as error:
        print("Error:", error)
        break


# Convert data into DataFrame for CSV
df = pd.DataFrame(quotes_data)

# Make tags readable in CSV
if not df.empty:
    df["tags"] = df["tags"].apply(
        lambda tag_list: ", ".join(tag_list)
    )

# Save CSV
csv_path = data_folder / "quotes_data.csv"

df.to_csv(
    csv_path,
    index=False,
    encoding="utf-8-sig"
)

# Save JSON
json_path = data_folder / "quotes_data.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(
        quotes_data,
        file,
        indent=4,
        ensure_ascii=False
    )

# Summary
print("\n========== QUOTES SCRAPING COMPLETED ==========")

print("Total quotes scraped:", len(quotes_data))
print("CSV saved:", csv_path)
print("JSON saved:", json_path)

print("\nFirst 5 quotes:")
print(df.head())

print("\nProject completed successfully!")