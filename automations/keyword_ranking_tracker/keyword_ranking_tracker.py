import argparse
import os
import sys
import requests
import pandas as pd
import yaml
from datetime import datetime

# Optional Google Sheets integration
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    gspread = None


def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_keywords(keywords_path):
    with open(keywords_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def fetch_serp_data(keyword, api_key, target_domain):
    url = f"https://serpapi.com/search.json?q={keyword}&engine=google&api_key={api_key}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Error fetching SERP for {keyword}: {resp.status_code}", file=sys.stderr)
        return None
    data = resp.json()
    results = data.get('organic_results', [])
    search_volume = data.get('search_information', {}).get('total_results', None)
    rank = None
    matched_url = None
    for idx, result in enumerate(results, 1):
        if target_domain in result.get('link', ''):
            rank = idx
            matched_url = result.get('link')
            break
    return {
        'keyword': keyword,
        'rank': rank,
        'url': matched_url,
        'search_volume': search_volume,
        'timestamp': datetime.utcnow().isoformat()
    }


def save_to_csv(results, output_path):
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)


def update_google_sheet(results, credentials_json, sheet_name):
    if not gspread:
        print("gspread not installed. Skipping Google Sheets update.")
        return
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    for row in results:
        sheet.append_row([row['keyword'], row['rank'], row['url'], row['search_volume'], row['timestamp']])


def main():
    parser = argparse.ArgumentParser(description="Keyword Ranking Tracker")
    parser.add_argument('--keywords', type=str, default='automations/keyword_ranking_tracker/keywords.txt', help='Path to keywords.txt')
    parser.add_argument('--config', type=str, default='automations/keyword_ranking_tracker/config.yaml', help='Path to config.yaml')
    parser.add_argument('--output', type=str, default=None, help='Output CSV path')
    parser.add_argument('--google_sheet', type=str, default=None, help='Google Sheet name (optional)')
    args = parser.parse_args()

    config = load_config(args.config)
    api_key = os.getenv('SERPAPI_KEY', config.get('SERPAPI_KEY'))
    target_domain = os.getenv('TARGET_DOMAIN', config.get('TARGET_DOMAIN'))
    credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS', config.get('GOOGLE_SHEETS_CREDENTIALS'))

    if not api_key or not target_domain:
        print("SERPAPI_KEY and TARGET_DOMAIN must be set in environment or config.", file=sys.stderr)
        sys.exit(1)

    keywords = load_keywords(args.keywords)
    results = []
    for kw in keywords:
        res = fetch_serp_data(kw, api_key, target_domain)
        if res:
            results.append(res)

    today = datetime.utcnow().strftime('%Y-%m-%d')
    output_path = args.output or f'results/keyword_rankings_{today}.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_to_csv(results, output_path)
    print(f"Saved results to {output_path}")

    if args.google_sheet and credentials_json:
        update_google_sheet(results, credentials_json, args.google_sheet)

if __name__ == "__main__":
    main()
