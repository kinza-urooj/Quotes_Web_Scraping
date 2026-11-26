# Quotes Web Scraping & Analytics Dashboard

A Python project that scrapes inspirational quotes, authors, and tags from **Quotes to Scrape** and visualizes the collected data through an interactive Streamlit dashboard.

## Features

- Scrapes quotes, authors, and tags
- Collects data from multiple pages
- Saves data in CSV and JSON formats
- Interactive Streamlit dashboard
- Search quotes and authors
- Filter quotes by author
- Visualize popular authors and tags
- Download datasets

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- Streamlit
- Plotly

## Project Structure

```text
Quotes_Web_Scraping/
│
├── data/
│   ├── quotes_data.csv
│   └── quotes_data.json
│
├── quotes_scraping.py
├── quotes_dashboard.py
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_LINK
```

### 2. Open the project folder

```bash
cd Quotes-Web-Scraping-Dashboard
```

### 3. Install dependencies

```bash
python -m pip install requests beautifulsoup4 pandas streamlit plotly
```

### 4. Run the scraper

```bash
python quotes_scraping.py
```

### 5. Launch the dashboard

```bash
python -m streamlit run quotes_dashboard.py
```

## Data Source

[Quotes to Scrape](https://quotes.toscrape.com/)

## Author

**Kinza Urooj**

Data Analysis & Python Projects

---

*Created as a learning project to practice web scraping, data processing, and data visualization.*
