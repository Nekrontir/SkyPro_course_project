import sys
import types
from datetime import datetime, timedelta
from typing import Callable
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from mypy.types import AnyType

from src.reports import spending_by_category

decorators_module = types.ModuleType("decorators")


def mock_data_copy() -> Callable:
    def decorator(func: Callable) -> Callable[..., AnyType]:
        return func

    return decorator


decorators_module.data_copy = mock_data_copy

sys.modules["decorators"] = decorators_module


@pytest.mark.parametrize(
    "category, date, expected_count",
    [
        ("Супермаркеты", "15.04.2024", 2),
        ("Транспорт", "15.04.2024", 1),
        ("Кафе", "15.04.2024", 1),
    ],
)
def test_spending_by_category_filters_correctly(
    transactions_df: pd.DataFrame, category: str, date: str, expected_count: int, mock_reports_logger: Mock
) -> None:
    result: pd.DataFrame = spending_by_category(transactions_df, category, date)
    assert len(result) == expected_count
    assert all(result["Категория"] == category)
    end_date = pd.to_datetime(date, dayfirst=True)
    start_date = end_date - timedelta(days=90)
    result_dates = pd.to_datetime(result["Дата операции"], dayfirst=True)
    assert all((result_dates >= start_date) & (result_dates <= end_date))


def test_spending_by_category_edge_cases(transactions_df: pd.DataFrame, mock_reports_logger: Mock) -> None:
    fixed_now = datetime(2024, 4, 15, 12, 0, 0)
    with patch("src.reports.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        result_none = spending_by_category(transactions_df, "Супермаркеты", None)
    assert len(result_none) == 2
    end_date = pd.to_datetime(fixed_now)
    start_date = end_date - timedelta(days=90)
    result_dates = pd.to_datetime(result_none["Дата операции"], dayfirst=True)
    assert all((result_dates >= start_date) & (result_dates <= end_date))
    result_empty = spending_by_category(transactions_df, "Несуществующая", "15.04.2024")
    assert len(result_empty) == 0
    assert isinstance(result_empty, pd.DataFrame)
    assert list(result_empty.columns) == list(transactions_df.columns)
