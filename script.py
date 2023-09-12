#!/usr/bin/env python3

import json
import os
from google_play_scraper import app, reviews_all, Sort
from app_store_scraper import AppStore
import datetime
import re

def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def download_google_play(lang, country, url):
  match = re.search(r'id=([^&]+)', url)
  if match:
    app_id = match.group(1)
    print(f"id: {app_id}")
  else:
    raise Exception('Invalid google play url, expected something like: https://play.google.com/store/apps/details?id=se.greycastle.actual_swedish')

  try:
    result = app(
        app_id,
        lang=lang,
        country=country
    )

    with open('app_info.json', 'w') as outfile:
        json.dump(result, outfile)

    reviews = reviews_all(
        app_id,
        sleep_milliseconds=4,
        lang=lang,
        country=country,
        sort=Sort.NEWEST
    )

    reviews_path = f'reviews_google_play_{lang}_{country}.json'
    with open(reviews_path, 'w') as outfile:
        json.dump(reviews, outfile, default=datetime_serializer)
        print('google play reviews saved to: ', reviews_path)
  except Exception as e:
    # pritn the message of the errror
    print("Failed to get google play reviews: ", e)
    print("Make sure the url is correct and the app is available in the country and language you specified")

def download_appstore(lang, country, url):
  match = re.search(r'/app/([^/]+)/id(\d+)', url)
  if match:
    app_name = match.group(1)
    app_id = match.group(2)
  else:
    raise Exception('Invalid appstore url, expected something like: https://apps.apple.com/us/app/jwords/id1616595660')

  appstore_app = AppStore(country=country, app_name=app_name, app_id = app_id)
  appstore_app.review(how_many=1000)

  reviews_path = f'reviews_appstore_{lang}_{country}.json'
  with open(reviews_path, 'w') as outfile:
      json.dump(appstore_app.reviews, outfile, default=datetime_serializer)
      print('appstore reviews saved to: ', reviews_path)

def download(lang, country, google_play_url, appstore_url):
  download_google_play(lang, country, google_play_url)
  download_appstore(lang, country, appstore_url)
  print('all done')

DEFAULTS_FILE = '.defaults'

def load_settings():
    if os.path.exists(DEFAULTS_FILE):
        with open(DEFAULTS_FILE, 'r') as f:
            settings = f.read().splitlines()
            if len(settings) == 4:
                return settings
    return "en", "us", None, None

def save_settings(language_code, country, google_play_url, appstore_url):
    with open(DEFAULTS_FILE, 'w') as f:
        f.write(f"{language_code}\n{country}\n{google_play_url}\n{appstore_url}")

def prompt_with_default(prompt, default):
    return input(f"{prompt} ({default}): ") or default

def main():
    default_language_code, default_country, default_google_play_url, default_apppstore_url = load_settings()

    if default_language_code:
        language_code = prompt_with_default("Enter the language code", default_language_code)
    else:
        language_code = input("Enter the language code: ")

    if default_country:
        country = prompt_with_default("Enter the country", default_country)
    else:
        country = input("Enter the country: ")

    if default_google_play_url:
        google_play_url = prompt_with_default("Enter the Google Play URL", default_google_play_url)
    else:
        google_play_url = input("Enter the Google Play URL: ")

    if default_apppstore_url:
        appstore_url = prompt_with_default("Enter the appstore URL", default_apppstore_url)
    else:
        appstore_url = input("Enter the appstore URL: ")


    save_settings(language_code, country, google_play_url, appstore_url)

    download(language_code, country, google_play_url, appstore_url)

if __name__ == "__main__":
    main()
