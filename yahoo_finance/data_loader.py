import logging

import pandas as pd
import yfinance as yf

from common.db_utils import TickerDB
from config.config import DATABASE_CONFIG, LOGGING_CONFIG

logger = logging.getLogger(__name__)


class YahooFinanceETL():
    """
    Read the Yfin data for specific ticker, transforms and write the transformed data to PostgreSQL DB
    """

    def __init__(
            self,
            symbol,
            start_date,
            end_date
    ):
        """
        Constructor for YahooFinanceETL
        :param symbol: Stock ticker name
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_db = TickerDB()

    def extract(self):
        """
        Download daily ticker market data from yahoo finance
        """
        try:
            logger.info('Process started for function: extract..')
            logger.info('Extracting data from Date: {} to Date: {} for ticker: {}'.format(self.start_date, self.end_date, self.symbol))
            ticker_df = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval='1d', threads=True).reset_index()
            ticker_df.columns = ticker_df.columns.str.strip().str.lower()
            ticker_df['ticker'] = self.symbol
            return ticker_df
        except Exception as error:
            logger.error('Error occured while extracting data')
            logger.error(error)
            return False
        finally:
            logger.info('Process completed for function: extract..')

    def transform(self, data_frame: pd.DataFrame):
        """
        Applies the necessary transformation to create report 1
        :param data_frame: Pandas DataFrame as Input
        :returns:
            data_frame: Transformed Pandas DataFrame as Output
        """
        logger.info('Process started for function: transform..')
        if data_frame.empty:
            logger.debug('The dataframe is empty. No transformations will be applied.')
            return data_frame
        logger.info('Applying transformations to yfin source data')
        data_frame['% change'] = round(data_frame['adj close'] / data_frame['adj close'].shift(1) - 1, 4)
        logger.info('Process completed for function: transform..')
        return data_frame

    def load(self, data_frame: pd.DataFrame) -> None:
        """
        Saves transform DataFrame to target DB
        :param data_frame: Pandas DataFrame as a Input
        """
        # Connection to PostgreSQL DB
        logger.info('Process started for function: load..')
        if data_frame.empty:
            logger.debug('The dataframe is empty. Skipping data load operation')
        else:
            try:
                logger.info('Loading {} data into DB.'.format(self.symbol))
                self.ticker_db.insert_market_data(data_frame)
                logger.info('Ticker: {} data inserted successfully!'.format(self.symbol))
            except Exception as error:
                logger.debug('Error occured while performing load operation')
                logger.error(error)
            finally:
                logger.info('Process completed for function: load..')

    def run_etl_pipeline(self):
        """
        Call the extract, transform, and load method for ticker
        """
        try:
            logger.info('Process started for function: etl_report..')
            logger.info('extract function called!')
            data_frame = self.extract()
            logger.info('transform function called!')
            data_frame = self.transform(data_frame=data_frame)
            logger.info('load function called!')
            self.load(data_frame=data_frame)
            return True
        except Exception as error:
            logger.error('Error occured in function: etl_report')
            logger.error(error)
            return False
        finally:
            logger.info('Process completed for function: etl_report..')
