import datetime
import logging
import re

import pandas as pd

from config import PATHS
from src.reports import spending_by_category
from src.services import searching
from src.utils import import_data_from_file
from src.views import get_main_web_json_answer

data_for_processing: pd.DataFrame = import_data_from_file()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\main_module.log",
    encoding="utf-8",
    filemode="w",
)
logger_main_mod = logging.getLogger("main_module")


if __name__ == "__main__":
    print("Здравствуйте! Вас приветствует приложение для анализа транзакций")
    logger_main_mod.info("Получение времени (сейчас)")
    time = datetime.datetime.now()
    date_today = time.strftime("%d.%m.%Y")
    today = time.strftime("%Y-%m-%d %H:%M:%S")
    print(get_main_web_json_answer(today))
    print("Желаете воспользоваться поиском ? Да/Нет")
    answer1 = input("Ввод: ")
    logger_main_mod.info(f"Ответ {answer1}")
    if answer1.lower() in ["yes", "y", "да"]:
        print("Введите ключевое слово для поиска в описании или категории транзакции")
        key_word = input("Ключевое слово: ")
        print(searching(key_word))
        logger_main_mod.info("Результат сформирован")
    print("Желаете получить отчёт по категории транзакций за последние 3 месяца ? Да/Нет")
    answer2 = input("Ввод: ")
    logger_main_mod.info(f"Ответ {answer2}")
    if answer2.lower() in ["yes", "y", "да"]:
        print("Введите категорию по которой будет произведён отчёт")
        category = input("Категория: ")
        logger_main_mod.info(f"Введённая категория {category}")
        print(
            "Введите дату с котрой будет отсчитываться поиск в формате ДД.ММ.ГГГГ.\n"
            "Или автоматически будет взята сегодняшняя дата за начало отсчёта."
        )
        date = input("Введите дату: ")
        logger_main_mod.info(f"Введённая дата {date}")
        pattern = re.compile(r"(\d{2}).(\d{2}).(\d{4})$")
        logger_main_mod.info("Сравнение с паттерном времени")
        if pattern.match(date):
            report = spending_by_category(data_for_processing, category, date)
            json_result = report.to_json(orient="records", date_format="iso", force_ascii=False, indent=4)
            logger_main_mod.info("Результат сформирован")
            print(json_result)
        else:
            report = spending_by_category(data_for_processing, category, date_today)
            json_result = report.to_json(orient="records", date_format="iso", force_ascii=False, indent=4)
            logger_main_mod.info("Результат сформирован")
            print(json_result)
