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


def get_now_time() -> int:
    """
    Функция для получения времени в данный момент, возвращает текущий час
    """
    now_date_time = datetime.datetime.now()
    now_time = now_date_time.strftime("%H")
    return int(now_time)


def get_distance_date() -> list:
    current_date = datetime.datetime.now()
    start_date = current_date.strftime("01.%m.%Y 00:00:00")
    today_date = current_date.strftime("%d.%m.%Y %H:%M:%S")
    return [start_date, today_date]


def import_data_from_file():
    """
    Получение данных из excel-файла при помощи библиотеки "pandas".
    Возвращает dataframe
    """
    logger_utils_mod.info("Получение данных из excel-файла")
    excel_data = pd.read_excel(PATHS["get_data"])
    return excel_data


def get_user_settings() -> dict:
    """
    Функция считывает json-file с настройками пользователя,
    возвращает словарь с настройками
    """
    with open(PATHS["user_settings"]) as f:
        settings = json.load(f)
        return settings
