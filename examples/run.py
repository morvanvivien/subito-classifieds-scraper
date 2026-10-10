"""Minimal example: run the subito-classifieds-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "iphone",
    "category": "elettronica",
    "region": "lazio",
    "maxItems": 100,
}

run = client.actor("bibian/subito-classifieds-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    seller = (item.get("sellerName") or "shop") if item.get("isCompany") else "private seller"
    print(f"{item['title']} | {item.get('city')} | {item.get('price')} EUR | {seller}")
print(f"{count} results")
