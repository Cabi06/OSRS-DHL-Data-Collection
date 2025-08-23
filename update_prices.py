import requests
import csv
import os
from datetime import datetime

# API endpoint for Dragon Hunter Lance
API_URL = "https://prices.runescape.wiki/api/v1/osrs/latest?id=22978"
CSV_FILE = "prices.csv"
HTML_FILE = "prices.html"

def fetch_price():
    response = requests.get(API_URL, headers={"User-Agent": "github-pages-price-tracker"})
    data = response.json()
    price_h = data["data"]["22978"]["high"]
    price_l = data["data"]["22978"]["low"]
    price = (price_h + price_l)/2 # Average daily price
    return price

def update_csv(price):
    # Create CSV if it doesn't exist
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "price"])
        writer.writerow([datetime.today().strftime("%Y-%m-%d"), price])

def generate_html():
    # Read the CSV back
    rows = []
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Build a simple scrollable HTML table
    table_rows = "\n".join(
        f"<tr><td>{date}</td><td>{price}</td></tr>"
        for date, price in rows[1:]  # skip header
    )

    html = f"""
    <html>
    <head>
        <title>Dragon Hunter Lance Prices</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 300px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .scrollable {{ max-height: 300px; overflow-y: scroll; }}
        </style>
    </head>
    <body>
        <h1>Dragon Hunter Lance Prices</h1>
        <div class="scrollable">
            <table>
                <tr><th>Date</th><th>Price</th></tr>
                {table_rows}
            </table>
        </div>
        <p> 
            <a href="prices.csv" download="DragonHunterLancePrices.csv">
                <button> Download CSV </button>
        </p>
        <br><br><br>
        <p>Data updates daily via GitHub Actions. Data Collected from runescape wiki. </p>
    </body>
    </html>
    """

    with open(HTML_FILE, "w") as f:
        f.write(html)

if __name__ == "__main__":
    price = fetch_price()
    update_csv(price)
    generate_html()
    print(f"Updated with price {price}")

