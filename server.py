from flask import Flask
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qs

app = Flask(__name__)

@app.route("/")
def parse_urls(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.select("a.result__a"):
        href = a.get("href")

        if "/l/?" in href:
            parsed = parse_qs(urlparse(href).query)
            if "uddg" in parsed:
                href = unquote(parsed["uddg"][0])

            if href and href.startswith("http"):
                links.append((a.get_text(strip=True), href))

            if len(links) >= 100:
                break
            return links
