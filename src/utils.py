import datetime
import json
import logging

import pandas as pd

from config import PATHS

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\utils_module.log",
    encoding="utf-8",
    filemode="w",
)

logger_utils_mod = logging.getLogger("utils_module")


def get_date_range() -> list[str]:
    """
    Функция ничего не принимает на вход.
    Возвращает лист с датами [начало месяца, сейчас]. Время в виде строки формата DD.MM.YYYY HH:MM:SS
    """
    current_date = datetime.datetime.now()
    start_date = current_date.strftime("01.%m.%Y 00:00:00")
    today_date = current_date.strftime("%d.%m.%Y %H:%M:%S")
    return [start_date, today_date]


def import_data_from_file(time_range: list = None) -> pd.DataFrame:
    """
    Получение данных из excel-файла при помощи библиотеки "pandas".
    Возвращает dataframe. Если указан временной промежуток,
    то возвращает dataframe с операциями за указанный период
    """
    logger_utils_mod.info("Получение данных из excel-файла")
    excel_data = pd.read_excel(PATHS["get_data"])
    if time_range:
        excel_data["Дата операции"] = pd.to_datetime(excel_data["Дата операции"], dayfirst=True)
        mask = (excel_data["Дата операции"] >= pd.to_datetime(time_range[0], dayfirst=True)) & (
            excel_data["Дата операции"] <= pd.to_datetime(time_range[1], dayfirst=True)
        )
        return excel_data[mask].copy()
    else:
        return excel_data


def get_user_settings() -> dict:
    """
    Функция считывает json-file с настройками пользователя,
    возвращает словарь с настройками
    """
    with open(PATHS["user_settings"]) as f:
        settings = json.load(f)
        return settings

print(get_date_range())