#!/usr/bin/env python3

import json
import os
from google_play_scraper import app, reviews_all, Sort
from app_store_scraper import AppStore
import datetime

def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def download(app_id, lang, country, appstore_app_id, appstore_name):

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

  appstore_app = AppStore(country=country, app_name=appstore_name, app_id = appstore_app_id)
  appstore_app.review(how_many=1000)

  reviews_path = f'reviews_appstore_{lang}_{country}.json'
  with open(reviews_path, 'w') as outfile:
      json.dump(appstore_app.reviews, outfile, default=datetime_serializer)
      print('appstore reviews saved to: ', reviews_path)

  print('all done')

DEFAULTS_FILE = '.defaults'

def load_settings():
    if os.path.exists(DEFAULTS_FILE):
        with open(DEFAULTS_FILE, 'r') as f:
            settings = f.read().splitlines()
            if len(settings) == 5:
                return settings
    return "en", "en", None, None, None

def save_settings(language_code, country, app_id, appstore_app_id, appstore_name):
    with open(DEFAULTS_FILE, 'w') as f:
        f.write(f"{language_code}\n{country}\n{app_id}\n{appstore_app_id}\n{appstore_name}")

def prompt_with_default(prompt, default):
    return input(f"{prompt} ({default}): ") or default

def main():
    default_language_code, default_country, default_app_id, default_appstore_app_id, default_appstore_name = load_settings()

    if default_language_code:
        language_code = prompt_with_default("Enter the language code", default_language_code)
    else:
        language_code = input("Enter the language code: ")

    if default_country:
        country = prompt_with_default("Enter the country", default_country)
    else:
        country = input("Enter the country: ")

    if default_app_id:
        app_id = prompt_with_default("Enter the app id to download", default_app_id)
    else:
        app_id = input("Enter the app id to download: ")

    if default_appstore_app_id:
        appstore_app_id = prompt_with_default("Enter the appstore app id", default_appstore_app_id)
    else:
        appstore_app_id = input("Enter the appstore app id: ")

    if default_appstore_name:
        appstore_name = prompt_with_default("Enter the appstore app name", default_appstore_name)
    else:
        appstore_name = input("Enter the appstore app name: ")


    save_settings(language_code, country, app_id, appstore_app_id, appstore_name)

    download(app_id, language_code, country, appstore_app_id, appstore_name)

if __name__ == "__main__":
    main()
