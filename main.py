import os
import logging
from sqlalchemy import create_engine
from src.db_client import PostgresDBClient
from src.api_client import AirportApiClient
from src.report_generator import generate_report


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("===== Запуск пайплайна =====")


    # 1. Инициализация БД
    db_client = PostgresDBClient()
    db_client.create_table()

    # 2. Загрузка данных из API
    api_client = AirportApiClient()
    raw_data = api_client.fetch_airports()
    if not raw_data:
        logger.error("Не удалось получить данные из API. Работа прервана.")
        return
    logger.info(f"Загружено {len(raw_data)} записей.")

    # 3. Запись в БД (вызываем метод напрямую, без 'with')
    db_client.insert_data(raw_data)

    # 4. Генерация отчёта
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL не найден в environment. Проверьте настройки окружения.")
        return

    engine = create_engine(db_url)
    try:
        generate_report(engine)
        logger.info("Отчёт успешно сгенерирован.")
    except Exception as e:
        logger.error(f"Ошибка при генерации отчёта: {e}")
        return

    logger.info("4. Пайплайн завершён. Файл в папке reports.")
    logger.info("РАБОТА ЗАВЕРШЕНА")

if __name__ == "__main__":
    main()