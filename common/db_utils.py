import logging
from sqlalchemy import create_engine, DateTime, Column, String, Numeric
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, sessionmaker

from config.config import DATABASE_CONFIG, LOGGING_CONFIG

logger = logging.getLogger(__name__)

Base = declarative_base()

class MarketData(Base):

    __tablename__ = 'market_data'
    __table_args__ = ({"schema": "price"})

    date = Column("date", DateTime, primary_key=True)
    ticker = Column("ticker", String)
    open = Column("open", Numeric)
    high = Column("high", Numeric)
    low = Column("low", Numeric)
    close = Column("close", Numeric)
    adj_close = Column("adj close", Numeric)
    volume = Column("volume", Numeric)
    percent_change = Column("% change", Numeric)

class TickerDB:
    """
    Class to handle all DB related operations
    """

    def __init__(self):
        """
        Initialize
        """
        logger.info('Created connection with DB..')
        self._username = DATABASE_CONFIG['DB_CONFIG'].get('username')
        self._password = DATABASE_CONFIG['DB_CONFIG'].get('password')
        self._host = DATABASE_CONFIG['DB_CONFIG'].get('host')
        self._port = DATABASE_CONFIG['DB_CONFIG'].get('port')
        self._db_name = DATABASE_CONFIG['DB_CONFIG'].get('db_name')
        self._url = 'postgresql://{}:{}@{}:{}/{}'.format(self._username, self._password, self._host, self._port, self._db_name)
        self._engine = create_engine(self._url)

    def insert_market_data(self, data_frame, table_name='market_data'):
        """
        Insert ticker DataFrame to sqlite table
        :param data_frame: Pandas dataframe
        :param table_name: Table name, default = market_data
        """
        try:
            logger.info('Process started for function: insert_ticker_data..')
            values = data_frame.to_dict('records')
            insert_stmt = postgresql.insert(MarketData.__table__).values(values)
            update_columns = {col.name: col for col in insert_stmt.excluded}
            do_update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[MarketData.date, MarketData.ticker],
                set_=update_columns
            )
            session = sessionmaker()
            session.configure(bind=self._engine)
            session = session()
            session.execute(do_update_stmt)
            session.commit()
            session.close()
            logger.info('Data Inserted to {} Table.'.format(table_name))
            return True
        except Exception as error:
            logger.error('Error occured while inserting data')
            logger.error(error)
            return False
        finally:
            logger.info('Process completed for function: connect..')