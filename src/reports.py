import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from config import PATHS
from src.decorators import data_copy

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\reports_module.log",
    encoding="utf-8",
    filemode="w",
)
logger_reports_mod = logging.getLogger("reports_module")


@data_copy()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает на вход:
    :param transactions: датафрейм с транзакциями
    :param category: название категории
    :param date: опциональная дата, если дата не передана, то берется текущая дата
    :return: функция возвращает траты по заданной категории за последние три месяца (от переданной даты)
    """
    logger_reports_mod.info("Функция spending_by_category запущена c декоратором")
    if date:
        end_date = pd.to_datetime(date, dayfirst=True)
    else:
        end_date = pd.to_datetime(datetime.now())
    logger_reports_mod.info("Выбрана дата с которой будут браться транзакции")
    start_date = end_date - timedelta(days=90)
    transactions = transactions.copy()
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    mask = (
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    )
    result: pd.DataFrame = transactions[mask]
    logger_reports_mod.info("Функция завершила работу")
    return result
