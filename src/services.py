import json
import logging

import pandas as pd

from config import PATHS
from src.utils import import_data_from_file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\services_module.log",
    encoding="utf-8",
    filemode="w",
)
logger_services_mod = logging.getLogger("services_module")


def searching(word_to_find: str) -> str:
    """
    Функция принимает строку для поиска,
    возвращает JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории
    """
    logger_services_mod.info("Функция searching запущена")
    df: pd.DataFrame = import_data_from_file()
    logger_services_mod.info("Получены данные для поиска")
    logger_services_mod.info(f"Поиск слова {word_to_find} в описании или категории")
    mask = (df["Категория"].str.contains(word_to_find, case=False, na=False)) | (
        df["Описание"].str.contains(word_to_find, case=False, na=False)
    )
    result_df = df[mask].copy()
    result = result_df.to_dict("records")
    logger_services_mod.info("Поиск завершён")
    return json.dumps(result)
