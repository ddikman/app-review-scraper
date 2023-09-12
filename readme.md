# App reviews download

This script helps put to use the two packages [app-store-scraper](https://pypi.org/project/app-store-scraper/) and [google-play-scraper](https://pypi.org/project/google-play-scraper/) to download the reviews of an app.

Install the dependencies and run it and it will prompt you for the details needed.

```shell
pipenv install
pipenv run python script.py
```

Usage example:

```shell
Enter the language code (en):
Enter the country (en): us
Enter the Google Play URL (https://play.google.com/store/apps/details?id=se.greycastle.actual_swedish):
Enter the appstore URL (https://apps.apple.com/us/app/jwords/id1616595660):
id: se.greycastle.actual_swedish
google play reviews saved to:  reviews_google_play_en_us.json
2023-09-12 12:11:29,681 [INFO] Base - Initialised: AppStore('us', 'jwords', 1616595660)
2023-09-12 12:11:29,681 [INFO] Base - Ready to fetch reviews from: https://apps.apple.com/us/app/jwords/id1616595660
2023-09-12 12:11:48,206 [ERROR] Base - Something went wrong: HTTPSConnectionPool(host='amp-api.apps.apple.com', port=443): Max retries exceeded with url: /v1/catalog/us/apps/1616595660/reviews?l=en-GB&offset=0&limit=20&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac (Caused by ResponseError('too many 404 error responses'))
2023-09-12 12:11:48,208 [INFO] Base - [id:1616595660] Fetched 0 reviews (0 fetched in total)
appstore reviews saved to:  reviews_appstore_en_us.json
all done
```