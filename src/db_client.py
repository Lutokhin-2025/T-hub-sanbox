import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/airports_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PostgresDBClient:
    def __init__(self):
        self.engine = engine
        self.session = SessionLocal()
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Подключение к PostgreSQL успешно установлено.")
        except Exception as e:
            logger.error(f"Не удалось подключиться к БД. Проверьте docker-compose. Ошибка: {e}")
            exit(1)

    def create_table(self):
        logger.info("Пересоздание таблицы 'airports'...")
        # Подключаемся к БД
        connection = self.engine.connect()
        try:
            # SQLAlchemy сам проверит наличие таблицы и пересоздаст её
            Base.metadata.create_all(self.engine)
            logger.info("Таблица 'airports' успешно создана или уже существует.")
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы: {e}")
            raise
        finally:
            connection.close()

    def insert_data(self, raw_data):
        if not raw_data:
            logger.warning("Попытка вставить пустые данные. Пропускаю.")
            return
        logger.info(f"Начинаю вставку данных. Записей: {len(raw_data)}")
        df = pd.DataFrame(raw_data)
        df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]

        connection = self.engine.connect()
        try:
            df.to_sql(
                'airports',
                con=connection,
                if_exists='replace',
                index=False,
                method='multi'
            )
            logger.info(f"Успешно вставлено {len(df)} новых записей.")
        except Exception as e:
            logger.error(f"Ошибка при вставке данных в БД: {e}")
            raise
        finally:
            connection.close()

if __name__ == "__main__":
    client = PostgresDBClient()
    client.create_table()
    test_data = [
        {"id": "1", "name": "Test 1", "city": "Moscow"},
        {"id": "2", "name": "Test 2", "city": "SPB"}
    ]
    client.insert_data(test_data)
    logger.info("Тестирование завершено.")