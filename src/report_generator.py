import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sqlalchemy import create_engine


def generate_report():
    #  подключение к БД
    engine_str = "postgresql://postgres:postgres@db:5432/airports_db"
    engine = create_engine(engine_str)


    try:
        # Загружаю данные из бд
        df = pd.read_sql(
            "SELECT * FROM airports ORDER BY name ASC LIMIT 20;",
            con=engine
        )

        # Создаю папку для отчётов
        Path("reports").mkdir(exist_ok=True)

        # Настраиваю график
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')


        # Создаю таблицу
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            loc='center',
            cellLoc='left',
            # внешний вид таблицы
            colWidths=[0.15] * len(df.columns)
        )
        # Настраиваю таблицу
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)  # Масштабируем таблицу

        # Сохраняю отчёт
        plt.savefig("reports/airports.png", bbox_inches='tight', dpi=150)
        plt.close(fig)
        print("Отчёт успешно создан: reports/airports.png")

    except Exception as e:
        print(f"Ошибка при генерации отчёта: {e}")
        raise