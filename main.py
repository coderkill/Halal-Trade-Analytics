import logging
from datetime import datetime, timedelta

from yahoo_finance.data_loader import YahooFinanceETL

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info('Process Started for function: main ')

        ticker = 'AAPL'
        start_date = datetime.now().date() - timedelta(days=5)
        end_date = datetime.now().date()

        data = YahooFinanceETL(ticker, start_date=start_date, end_date=end_date)
        data.run_etl_pipeline()
        logger.info('Process Completed for funtion: main')

    except Exception as error:
        logger.error('Error occured in function: etl_report')
        logger.error(error)

if __name__ == "__main__":
    main()