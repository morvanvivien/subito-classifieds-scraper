# How to Scrape Subito.it: Italy Classified Ads (Price, Category, Seller Type)

> **Run it now, no code: [subito-classifieds-scraper on the Apify Store](https://apify.com/bibian/subito-classifieds-scraper)** &nbsp;|&nbsp; $3.00 per 1,000 listings &nbsp;|&nbsp; no browser, no proxy, no login

Subito.it is one of Italy's largest classifieds sites, covering cars, electronics, real estate, jobs and general second-hand items. It has no public export and no official API for third parties. This guide shows how to get its listings as clean structured data: title, description, price, location and seller type, with a free Apify Actor, from the console or from code.

Searches this page answers: subito.it scraper, italy classifieds scraper, subito price data, scrape subito listings.

## What you get from the Subito.it scraper

- Every listing matching your keywords, category and region, newest first.
- Price (`price`, null when the seller did not set one) and full location (region, province, city).
- Seller type always flagged: `isCompany` and `sellerName` tell shops apart from private sellers.
- Category, condition and posting date for every listing.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, personal data removed, long texts truncated) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | Subito listing id and public link |
| `category`, `title`, `description` | Listing category, title and text |
| `price` | Asking price in EUR, null when not set |
| `region`, `province`, `city` | Where the listing is located |
| `condition` | Item condition as described by the seller |
| `isCompany`, `sellerName` | Seller type; `sellerName` is only filled for business accounts |
| `datePosted` | When the listing was posted |

## Use cases

- **Monitor a category or region.** Track new listings by category (cars, electronics, real estate, jobs, general items...) and Italian region.
- **Track asking prices.** Group `price` by category and region to see what a given item sells for across Italy.
- **Separate shops from private sellers.** Filter on `isCompany` to find business listings only, with the shop name.
- **Feed an alert or an aggregator.** Run it daily with your usual category and region, dedupe by `id` to catch only the new listings.

## Input

| Field | What it does |
|---|---|
| `keywords` | Search term, for example `bicicletta` or `iphone`. Empty browses a category. |
| `category` | Category URL slug as used by Subito.it, for example `auto`, `moto-e-scooter` or `elettronica`. Defaults to `usato` (general second-hand items). |
| `region` | Italian region URL slug, for example `lombardia` or `lazio`. Empty rotates across major regions. |
| `maxItems` | The run stops once this many listings are saved (default 50). |

Example input:

```json
{
  "keywords": "iphone",
  "category": "elettronica",
  "region": "lazio",
  "maxItems": 100
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/subito-classifieds-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, category, region and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/subito-classifieds-scraper').call({
    "keywords": "iphone",
    "category": "elettronica",
    "region": "lazio",
    "maxItems": 100
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.city} | ${item.price ?? '-'} EUR | ${item.isCompany ? item.sellerName ?? 'shop' : 'private seller'}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/subito-classifieds-scraper").call(run_input={
    "keywords": "iphone",
    "category": "elettronica",
    "region": "lazio",
    "maxItems": 100,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    seller = item.get("sellerName") or "shop" if item.get("isCompany") else "private seller"
    print(f"{item['title']} | {item.get('city')} | {item.get('price')} EUR | {seller}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$3.00 per 1,000 listings** (that is $0.003 per listing), plus a tiny start fee. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/subito-classifieds-scraper) when this guide was written; the Store page is the reference.

## Why this one

- **No login, no account.** Everything comes from Subito's own public category and region pages.
- **Any category, any region, one actor.** No need to run a separate tool per category.
- **Seller type always flagged.** `isCompany` and `sellerName` tell shops apart from private sellers on every record, not buried in the description.

## Limits and honest notes

- Subito's own pagination (`?o=`) is off-limits to robots; this actor instead rotates through one Italian region per step when none is requested, each its own first page of results.
- Results follow Subito's own search, so a broad category can include listings from several sub-categories.
- `price` is empty for listings where the seller did not set one (common for free or "contact for price" items).
- Private sellers are never named: `sellerName` is only filled for business accounts (`isCompany: true`), from the shop name Subito itself displays.
- A line that carries an e-mail address or a raw Italian phone number is dropped from the description: Subito already masks most phone numbers typed into a listing, this actor catches the rest.
- This is an unofficial tool, not affiliated with Subito.it. Check the site terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
No. The Actor reads the data directly, so runs are fast and cheap.

**How do I only get new listings every day?**  
Schedule the Actor once a day and dedupe the results by `id` in your own pipeline.

**Can I search a specific category and region together?**  
Yes, set both `category` and `region` to narrow the search.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open subito-classifieds-scraper on the Apify Store](https://apify.com/bibian/subito-classifieds-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
