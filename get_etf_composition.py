import datetime
import logging
import warnings

from config.config_etf import ETF_CONFIG

warnings.filterwarnings('ignore')

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__file__)

headers = {"Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": "Java-http-client/"}
config = ETF_CONFIG
def get_etf_symbols_nasdaq():
    etf_url = "https://api.nasdaq.com/api/screener/etf?tableonly=true&limit=25&offset=0&download=true"
    etf_response = requests.get(etf_url, headers=headers)
    etf_json = etf_response.json()
    etf_df = pd.DataFrame(etf_json['data']['data']['rows'])
    return list(etf_df.symbol)

def download_etf_profile(etf_tickers):
    etf_details = []

    for ticker in etf_tickers:
        try:  # <span class="Fl(end)">4.94%</span>
            url = r'https://finance.yahoo.com/quote/{}/profile?p={}'.format(ticker, ticker)
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text)
            keys = [i.text for i in soup.find(class_='Mb(25px)').find_all(class_='Fl(start)')]
            vals = [i.text for i in soup.find(class_='Mb(25px)').find_all(class_='Fl(end)')]
            res_dict = dict(zip(keys, vals))
            res_dict['symbol'] = ticker
            etf_details.append(res_dict)
            logger.info("Done for {}".format(ticker))
        except Exception as e:
            logger.info("Error {} for {}".format(str(e), ticker))

    return pd.DataFrame(etf_details)

def download_etf_holdings(etf_tickers):

    for ticker in etf_tickers:
        try:  # <span class="Fl(end)">4.94%</span>
            url = r'https://finance.yahoo.com/quote/{}/holdings?p={}'.format(ticker, ticker)
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text)

            ##Overall portfolio composition
            html_config = config["ETF_HTML_CONFIG"]
            holdings = list(soup.find_all(class_='Mb(25px)'))
            details = []
            for i in range(0, len(html_config)):
                keys = [j.text for j in holdings[i].find_all(class_=html_config[i]['KEY_HTML'])]
                values = [j.text for j in holdings[i].find_all(class_=html_config[i]['VALUE_HTML'])[html_config[i]['START_POINT']:]]
                res_dict = dict(zip(keys, values))
                res_dict['symbol'] = ticker
                res_dict['date'] = datetime.datetime.now().date()
                res_dict['name'] = html_config[i]['NAME']
                df = pd.DataFrame([res_dict])
                df = df.set_index(['symbol', 'name', 'date'])
                details.append(df)
            logger.info("Done for {}".format(ticker))
            return details
        except Exception as e:
            logger.info("Error {} for {}".format(str(e), ticker))

    return []


if __name__ == '__main__':
    ticker_list = get_etf_symbols_nasdaq()[1:5]
    etf_profile = download_etf_profile(ticker_list)
    print('#### ETF PROFILE ####')
    print(etf_profile)

    print('#### ETF COMPOSITION ####')
    etf_details = download_etf_holdings(ticker_list)
    print(etf_details)