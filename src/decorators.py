from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

from config import PATHS


def data_copy(filename: Optional[str] = None) -> Callable:
    """
    Декоратор с параметром для записи копии данных генерируемых функцией.
    По умолчанию данные записываются в excel-файл
    Параметром декоратора является наименование файла, куда будет вестись запись данных.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if filename is None:
                file_path = f'{PATHS["data"]}\\data_spending_by_category.xlsx'
            else:
                file_path = f'{PATHS["data"]}\\{filename}.xlsx'
            result = func(*args, **kwargs)
            with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
                result.to_excel(writer, sheet_name="Данные по категориям")
            return result

        return wrapper

    return decorator
