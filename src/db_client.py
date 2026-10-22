import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresDBClient:
    def __init__(self):
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        host = os.getenv("DB_HOST", "db")  # Важно: 'db', а не localhost
        port = os.getenv("DB_PORT", "5432")
        dbname = os.getenv("DB_NAME", "airports_db")
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(url)

    def __enter__(self):
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


    def create_table(self):
        from sqlalchemy import Table, Column, String, Integer, Float, MetaData
        metadata = MetaData()
        Table(
            'airports',
            metadata,
            Column('id', String, primary_key=True),
            Column('name'),
            Column('city'),
            Column('country'),
            Column('iata'),
            Column('icao'),
            Column('latitude', Float),
            Column('longitude', Float),
            Column('altitude', Integer),
            Column('timezone'),
            Column('dst'),
            Column('tz_type')
        )
        metadata.create_all(self.engine)

    def insert_data(self, raw_data):
        if not raw_data:
            return
        df = pd.DataFrame(raw_data)
        df.to_sql('airports', con=self.engine, if_exists='replace', index=False)