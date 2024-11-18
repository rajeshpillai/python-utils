import requests
from bs4 import BeautifulSoup
import time

# URL of the website to scrape
url = 'example.com'

# Mimic the headers from the curl request
headers = {
    'User-Agent': 'curl/7.81.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.ernestjones.co.uk/',
    'Connection': 'keep-alive'
}

# Add cookies that were set in the curl response (these may change over time)
cookies = {
    'SITE_IMP': 'HYB',
    'AKA_NUM': '0_acf5d217_1731567127_54382af9',
    'akavpau_prod_ernestJones_vp': '1731567427~id=11b5bad9f80abf4a9956c40821449ff8',
    '_abck': '6F61E72EB0E40F45FCAD742865CF374D~-1~YAAQrPXSF5DV2wqTAQAAhItxKQxCinQ4w2HqsHBbJholXSLf+jH3xOTvySkwxaOOi1tv4Y7N4RqZEquj7xKGPI8e+U0pZagxrZhOBiVa4mnExDesY6Nxe/m8nDosQ0DRkIuqJbUBNklJHDipPkLNt9ty6Zl/7jMY7CBJzUlI/XtZC+XhlCJGqbN1Fkc2xNpuqD0EzYDJIf3p4xHFG4eujlZ8F4IpKBMSfuax/iuxlc0gzozayXA2UpdsWdUfnVPbOWpP3xreZsdM6KEfoM7HK74Sp//vQGRo2n9VXFsS5khfc6fd6vX6DZ6fkpopdJJaEh4+4hEYR0UYml6OI2zHgb7fa3/rUsAOjX0IRIS/DeSk0Tz2ENM46Ymb9qvPFPl3jvY6/Sdd7NPDELD72nZYMQBZah/1yWEUjfQYHsShWZu9~-1~-1~-1',
    'bm_sz': 'F50A8E83D1FE1D33AEAE2CF6C6AE07A2~YAAQrPXSF5HV2wqTAQAAhItxKRkDRA9p5CBUsIehjm9BBmGK767s0uzh5KjQf0VgYE+74i3+Gu9OqREGCrogOsI4T70+D60gMtZLUsQAlpj1767zjlO/4vlcLo3zohSz9FfRJjil4X3AHD3AtZfZuQfwONXCqjvS/u1CUHrQt0uWakQ2qe+SObYzEXi3HCreGn9BB0oHiKbIVD17zwFXNWmdTowfZr+uICP/ikXvWoKUPYiWtDnvUtG1r8/WVK3klzl0bkj9AyvzxFrXg6r+H0h2WSy8GrJSo4M70wB+CEdJn4IDOVGGu27vib0RMI8CU9ZUFT97Jjr78E1CLX0psD4KiuXuMXZwEEAxhHZq3/49kLMu6xIeqqj7sdzNTRdNDptXN3QtMm3+Lh2CCue3bc0=~4473653~3424581'
}

# Start a session to maintain cookies
session = requests.Session()
session.headers.update(headers)

try:
    # Request the page with cookies
    response = session.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()  # Raise an error if status is not 200

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all products on the page
    products = soup.find_all('div', class_='product-item')
    for product in products:
        # Extract image, category, attributes, and price
        image_tag = product.find('img')
        image = image_tag['src'] if image_tag else 'N/A'
        category = 'Platinum Rings'  # Set category based on URL
        attributes_tag = product.find('div', class_='product-attributes')
        attributes = attributes_tag.text.strip() if attributes_tag else 'N/A'
        price_tag = product.find('div', class_='price')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Print or save the scraped data
        print(f'Image URL: {image}')
        print(f'Category: {category}')
        print(f'Attributes: {attributes}')
        print(f'Price: {price}')
        print('---')

        # Delay to prevent overloading the server
        time.sleep(2)

except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred: {err}')
except Exception as err:
    print(f'An error occurred: {err}')
