import datetime
import json
import logging
import os

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv

from config import PATHS
from src.utils import get_date_range, get_user_settings, import_data_from_file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\views_module.log",
    encoding="utf-8",
    filemode="w",
)
logger_views_mod = logging.getLogger("views_module")

data_for_processing: pd.DataFrame = import_data_from_file()
logger_views_mod.info("Получены данные из excel-файла")
user_settings: dict = get_user_settings()
logger_views_mod.info("Получены настройки пользователя из json-файла")
date_range: list = get_date_range()


def greeting(time: int) -> str:
    """
    Функция выбирает приветствие в зависимости от времени суток.
    На вход функция получает текущий час в виде целого числа,
    на выходе строка с приветствием.
    """
    logger_views_mod.info("Функция greeting запущена")
    if 5 <= time < 12:
        answer = "Доброе утро"
    elif 12 <= time < 18:
        answer = "Добрый день"
    elif 18 <= time <= 22:
        answer = "Добрый вечер"
    elif time in [23, 24, 0, 1, 2, 3, 4]:
        answer = "Доброй ночи"
    else:
        answer = "Доброго времени суток"
    logger_views_mod.info("Функция greeting завершила работу")
    return answer


def get_card_info(df: pd.DataFrame) -> list[dict]:
    """
    Функция принимает на вход dataframe,
    возвращает лист словарей. Словарь состоит из номера карты,
    суммы трат по карте, кэшбэка в размере 1р на каждые 100р
    """
    logger_views_mod.info("Функция get_card_info запущена")
    work_df = df.copy()
    logger_views_mod.info("Получен dataframe для обработки")
    group_df = work_df.groupby("Номер карты").agg({"Сумма операции с округлением": "sum"})
    card_info = group_df["Сумма операции с округлением"].to_dict()
    result = []
    for card, total in card_info.items():
        last_digits = card
        total_spent = total
        cashback = total / 100
        (
            result.append(
                {"last_digits": last_digits, "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)}
            )
        )
    logger_views_mod.info("Получена информация по картам")
    return result


def get_top_five_transactions(df: pd.DataFrame) -> list[dict]:
    logger_views_mod.info("Функция get_top_five_transactions запущена")
    work_df = df.copy()
    logger_views_mod.info("Получен dataframe для обработки")
    sort_df = work_df.sort_values(by=["Сумма платежа"], ascending=False)  # получили сортировку от большего к меньшему
    slice_df = sort_df[0:5]
    transactions = slice_df.to_dict("records")
    result: list = []
    for data in transactions:
        date = data.get("Дата платежа")
        amount = data.get("Сумма операции")
        category = data.get("Категория")
        description = data.get("Описание")
        result.append({"date": date, "amount": amount, "category": category, "description": description})
    logger_views_mod.info("Получен топ 5 транзакций")
    return result


def get_currency_course(settings: dict) -> list[dict]:
    """
    Функция получает на вход настройки задаваемые пользователем в виде запрашиваемых валют,
    возвращает словарь с указанием валюты и стоимости в рублях
    """
    logger_views_mod.info("Функция get_currency_course запущена")
    user_currencies = settings["user_currencies"]
    result: list = []
    logger_views_mod.info("Получение курса валют по API начато")
    for currency in user_currencies:
        load_dotenv()
        api_key = os.getenv("API_KEY_1")
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
        response = requests.get(url)
        data = response.json()
        course = data.get("conversion_rates", {}).get("RUB")
        result.append({"currency": currency, "rate": round(course, 2)})
    logger_views_mod.info("Получение курса валют по API закончено")
    return result


def get_stock_price(settings: dict) -> list[dict]:
    """
    Функция получает на вход биржевые лейблы компаний стоимость акций которых интересует пользователя,
    возвращает словарь с указанием акции и ёё стоимости в рублях
    """
    logger_views_mod.info("Функция get_stock_price запущена")
    user_stocks = settings["user_stocks"]
    result: list = []
    logger_views_mod.info("Получение стоимости указанных в настройках пользователя акций по API начато")
    for stock in user_stocks:
        load_dotenv()
        api_key = os.getenv("API_KEY_2")
        finnhub_client = finnhub.Client(api_key=api_key)
        data = finnhub_client.quote(stock)
        price = data.get("c")
        result.append({"stock": stock, "price": price})
    logger_views_mod.info("Получение стоимости акций по API закончено")
    return result


def get_main_web_json_answer(time: str):
    """
    Функция формирования json-ответа для главной вэб страницы.
    На вход функция получает строку времени формата YYYY-MM-DD HH:MM:SS,
    на выход подаётся сформированный ответ
    """
    logger_views_mod.info("Функция get_main_web_json_answer запущена")
    date_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    now_hour = int(date_obj.strftime("%H"))
    logger_views_mod.info("Получен текущий час")
    answer = {
        "greeting": f"{greeting(now_hour)}",
        "cards": get_card_info(data_for_processing),
        "top_transactions": get_top_five_transactions(data_for_processing),
        "currency_rates": get_currency_course(user_settings),
        "stock_prices": get_stock_price(user_settings),
    }
    logger_views_mod.info("Формирование словаря для json-ответа завершено")
    return json.dumps(answer)
