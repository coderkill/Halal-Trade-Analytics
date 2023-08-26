import logging

import pandas as pd
import yahoo_fin.stock_info as si

logger = logging.getLogger(__name__)

class FundamentalRatios:

    def __init__(self, tickers, ratios):
        self.tickers = tickers
        self.ratios = ratios

    def get_fundamental_ratios(self):

        try:
            df_fundamentals = pd.DataFrame()

            for ticker in self.tickers:
                stock_name = ticker
                fundamental_ratio = si.get_stats_valuation(stock_name)
                fundamental_ratio.index = fundamental_ratio[0]
                fundamental_ratio = fundamental_ratio.drop(labels=0, axis=1)
                tmp_table = fundamental_ratio.T
                tmp_table = tmp_table[self.ratios]
                df_fundamentals = pd.concat([df_fundamentals, tmp_table])

            df_fundamentals.index = self.tickers
            df_fundamentals = df_fundamentals.astype('float')
            df_fundamentals.dropna(inplace=True)
            return df_fundamentals
        except Exception as e:
            logger.info(f'An exception occurred while executing get_fundamental: {e}')

if __name__ == "__main__":

    tickers = ['AAPL', 'IBM', 'MSFT', 'WMT', 'AMGN', 'AXP', 'BA', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']

    ratios = ['Trailing P/E', 'Forward P/E', 'PEG Ratio (5 yr expected)', 'Price/Book (mrq)',
              'Price/Sales (ttm)', 'Enterprise Value/EBITDA', 'Enterprise Value/Revenue']

    fundamentals = FundamentalRatios(tickers, ratios)
    fundamental_data = fundamentals.get_fundamental_ratios()
    logger.info('Fetched fundamental data {}'.format(len(fundamental_data)))