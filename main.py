import os
from dotenv import load_dotenv
from src.api_client import AirportApiClient
from src.db_client import PostgresDBClient
from src.report_generator import generate_report

load_dotenv()

def main():
    print("Запуск")

    # 1. Получаю данные
    print("1. Загрузка данных из API...")
    api_client = AirportApiClient()
    raw_data = api_client.fetch_airports()
    print(f" Загружено {len(raw_data)} записей.")

    # 2. Работа с БД
    print("2. Запись данных в PostgreSQL...")
    with PostgresDBClient() as db:
        db.create_table()
        db.insert_data(raw_data)
    print(" Запись завершена.")

    # 3. Генерация отчета
    print("3. Генерация отчета...")
    from sqlalchemy import create_engine

    # Использую имя сервиса 'db' из docker-compose как хост
    engine = create_engine("postgresql://postgres:postgres@db:5432/airports_db")
    generate_report(engine)

    print("4. Готово. Файл в папке reports.")
    print(" РАБОТА ЗАВЕРШЕНА ")


if __name__ == "__main__":
    main()