import urllib.request

import numpy as np
from bs4 import BeautifulSoup
from enum import Enum


class Capacity(Enum):
    cap_1_6 = 1598
    cap_1_9 = 1896
    cap_2_0 = 1968

def get_html(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    return soup


def count_pages(main_url):
    soup = get_html(main_url)
    return int(soup.find_all('span', attrs={'class': 'page'})[-2].text)


def collect_data(main_url, pages=3):
    Xy = np.empty((0, 4))
    for page in range(1, pages + 1):
        print('\rParsing page: ' + str(page), end='')
        url = main_url + '&page=' + str(page)
        soup = get_html(url)
        articles = soup.find_all('article')

        for article in articles:
            # year
            year_tag = article.find("li", attrs={'data-code': 'year'})
            if (year_tag == None):
                continue
            year = int(year_tag.text)
            # mileage
            mileage_tag = article.find("li", attrs={'data-code': 'mileage'})
            if (mileage_tag == None):
                continue
            mileage = int(mileage_tag.span.text.replace(' ', '')[:-2])
            # capacity
            capacity_tag = article.find("li", attrs={'data-code': 'engine_capacity'})
            if (capacity_tag == None):
                continue
            capacity = parse_capacity(int(capacity_tag.span.text.replace(' ', '')[:-3]))
            # price
            price_tag = article.find("span", attrs={'class': 'offer-price__number'})
            if (price_tag == None):
                continue
            price = int(price_tag.contents[0].replace(' ', ''))

            Xy = np.append(Xy, [[year, mileage, capacity, price]], axis=0)
    print('\n')
    return Xy


def split_data(Xy, percent_of_test_data=30):
    n = len(Xy)
    # print(Xv[-10:])
    # np.random.shuffle(Xy)

    n_train = round((100 - percent_of_test_data) / 100 * n)
    n_test = n - n_train

    [Xy_train, Xy_test, _] = np.split(Xy, [n_train, n_train + n_test])

    X_train = Xy_train[:, [0, 1, 2]]
    y_train = Xy_train[:, [3]]

    X_test = Xy_test[:, [0, 1, 2]]
    y_test = Xy_test[:, [3]]

    return X_train, y_train, X_test, y_test


def parse_capacity(capacity):
    if capacity < Capacity.cap_1_9.value:
        capacity = Capacity.cap_1_6.value
    elif capacity >= Capacity.cap_1_9.value and capacity < Capacity.cap_2_0.value:
        capacity = Capacity.cap_1_9.value
    else:
        capacity = Capacity.cap_2_0.value

    return capacity
