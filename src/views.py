import pandas as pd
import requests
import json
import datetime
import finnhub
import logging
import os
from dotenv import load_dotenv
from src.utils import get_now_time, import_data_from_file, get_user_settings, get_distance_date

data_for_processing = import_data_from_file()
user_settings : dict = get_user_settings()
date_range = get_distance_date()


def greeting(time: int) -> str:
    """
    Функция выбирает приветствие в зависимости от времени суток.
    На вход функция получает текущий час в виде целого числа,
    на выходе строка с приветствием.
    """

    answer = ""
    if 5 <= time < 12:
        answer = "Доброе утро"
    elif 12 <= time < 18:
        answer = "Добрый день"
    elif 18 <= time <= 22:
        answer = "Добрый вечер"
    elif  time in [23, 24, 0, 1, 2, 3, 4]:
        answer = "Доброй ночи"
    return answer




def get_card_info(df, list_date):

    result = []
    result.append({
        "last_digits": last_digits,
        "total_spent": round(total_spent, 2),
        "cashback": cashback
    })

    return result


def get_top_five_transactions(df, list_date):





def get_currency_course(settings: dict) -> list[dict]:

    user_currencies = settings['user_currencies']
    result : list = []

    for currency in user_currencies:
        load_dotenv()
        api_key = os.getenv("API_KEY_1")
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}'
        response = requests.get(url)
        data = response.json()
        course = data.get("conversion_rates",{}).get('RUB')
        result.append({"currency": currency, "rate": round(course, 2) })

    return result


def get_stock_price(settings: dict) -> list[dict]:

    user_stocks = settings['user_stocks']
    result: list = []
    for stock in user_stocks:
        load_dotenv()
        api_key = os.getenv("API_KEY_2")
        finnhub_client = finnhub.Client(api_key=api_key)
        data = finnhub_client.quote(stock)
        price = data.get("c")
        result.append({"stock": stock, "price": price})

    return result



def get_main_web_json_answer():
    """
    Функция формирования json-ответа для главной вэб страницы.
    """
    answer = {
        "greeting": f"{greeting(get_now_time())}",
        "cards": "",
        "top_transactions": [
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
            {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары", "description": "Ozon.ru"},
            {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
            {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы", "description": "Кешбэк за обычные покупки"},
        ],
        "currency_rates": get_currency_course(user_settings),
        "stock_prices": get_stock_price(user_settings),

    }

    return json.dumps(answer)



print(get_top_five_transactions(data_for_processing, date_range))

