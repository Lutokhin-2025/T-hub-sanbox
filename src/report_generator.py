import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def generate_report(engine):
    """
    Генерирует простой график распределения городов по количеству аэропортов
    и сохраняет его в папку reports.
    """
    logger.info("Генерация отчёта...")

    try:
        # Читаем данные, которые мы только что вставили
        df = pd.read_sql('SELECT * FROM airports', con=engine)

        if df.empty:
            logger.warning("База данных пуста. Отчёт не сгенерирован.")
            return

        # Группируем по городам для примера
        city_counts = df['name'].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        city_counts.plot(kind='bar')
        plt.title('Топ-10 городов по количеству аэропортов')
        plt.xlabel('Город')
        plt.ylabel('Количество аэропортов')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Создаём папку, если её нет
        os.makedirs('/app/reports', exist_ok=True)

        # Путь внутри контейнера
        output_path = '/app/reports/airport_report.png'
        plt.savefig(output_path)
        logger.info(f"Отчёт успешно сгенерирован: {output_path}")


    except Exception as e:
        logger.error(f"Ошибка при генерации отчёта: {e}")
        raise