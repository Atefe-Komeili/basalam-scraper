from requests.structures import CaseInsensitiveDict
from datetime import date
import pandas as pd
import jdatetime
import requests

word = input("enter word for search : ")
num_of_products = int(input("enter number of products : "))

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
final_data = []

for i in range(1, num_of_products, 24):
    print(i, 'to', min(num_of_products, (i + 24)))
    resp = requests.get(
        f"https://search.basalam.com/ai-engine/api/v2.0/product/search?productAds=false&adsImpressionDisable=true&q={word}&bazarGardy=false&from={i}&size={num_of_products - i + 1}&filters.hasDiscount=false&filters.isReady=false&filters.isExists=true&filters.hasDelivery=false&filters.queryNamedTags=false",
        headers=headers)
    resp.raise_for_status()
    basalam_data = resp.json()["products"]
    print(len(basalam_data))
    for product in basalam_data:
        final_data.append({
            'title': product['name'],
            'brand': None,
            'price': product['primaryPrice'] if product['primaryPrice'] != 0 else product['price'],
            'weight': product['weight'],
            'off_price': product['price'],
            'seller': product['vendor']['name'],
            'rating': product['rating']['average'],
            'rating_count': product['rating']['count'],
            'image': product['photo']['MEDIUM'] if product['photo'] else '',
            'time': str(jdatetime.date.fromgregorian(date=date.today())),
            'params': {},

        })

# Change datatype to Dataframe and save as csv file with correct day-month-year
data = pd.DataFrame(final_data)
data.to_csv("basalam  " + str(jdatetime.date.fromgregorian(date=date.today())) + ".csv")
