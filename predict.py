import urllib.request

import numpy as np
from bs4 import BeautifulSoup


def collect_data(main_url):
    Xy = np.empty((0, 4))
    htm = None
    for page in range(1, 10):  # pages+1):
        url = main_url + '&page=' + str(page)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        articles = soup.find_all('article')
        print('Page: ' + str(page) + ' | Offers: ' + str(len(articles)))

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
            capacity = int(capacity_tag.span.text.replace(' ', '')[:-3])
            if capacity < 1896:
                capacity = 1598
            elif capacity >= 1896 and capacity < 1968:
                capacity = 1896
            else:
                capacity = 1968
            # price
            price_tag = article.find("span", attrs={'class': 'offer-price__number'})
            if (price_tag == None):
                continue
            price = int(price_tag.contents[0].replace(' ', ''))
            Xy = np.append(Xy, [[year, mileage, capacity, price]], axis=0)
    return Xy


def split_data(Xy, percent_of_test_data=30):
    n = len(Xy)
    print('\nTotal samples: ', n)

    # print(Xv[-10:])
    np.random.shuffle(Xy)

    n_train = round((100 - percent_of_test_data) / 100 * n)
    n_test = n - n_train

    [Xy_train, Xy_test, _] = np.split(Xy, [n_train, n_train + n_test])

    print('Training samples: %d' % len(Xy_train))
    print('Test samples: %d' % len(Xy_test))

    X_train = Xy_train[:, [0, 1, 2]]
    y_train = Xy_train[:, [3]]

    X_test = Xy_test[:, [0, 1, 2]]
    y_test = Xy_test[:, [3]]

    return X_train, y_train, X_test, y_test
