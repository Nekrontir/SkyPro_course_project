import datetime
import json
from typing import Any, Dict, List
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import get_date_range, get_user_settings, import_data_from_file


@patch("src.utils.datetime")
def test_get_date_range_returns_correct_format(mock_datetime: Mock) -> None:
    fixed_now = datetime.datetime(2024, 5, 15, 14, 30, 45)
    mock_datetime.datetime.now.return_value = fixed_now
    result: List[str] = get_date_range()
    assert len(result) == 2
    assert result[0] == "01.05.2024 00:00:00"
    assert result[1] == "15.05.2024 14:30:45"
    assert all(isinstance(date_str, str) for date_str in result)


@patch("src.utils.datetime")
def test_get_date_range_calls_logger(mock_datetime: Mock, mock_logger: Mock) -> None:
    fixed_now = datetime.datetime(2024, 5, 15, 14, 30, 45)
    mock_datetime.datetime.now.return_value = fixed_now
    get_date_range()
    assert mock_logger.info.called
    assert mock_logger.info.call_count >= 2


@pytest.mark.parametrize(
    "time_range,expected_count",
    [
        (None, 4),
        (["01.05.2024 00:00:00", "31.05.2024 23:59:59"], 4),
        (["01.05.2024 00:00:00", "15.05.2024 15:00:00"], 2),
        (["20.05.2024 00:00:00", "31.05.2024 23:59:59"], 2),
    ],
)
@patch("src.utils.PATHS")
def test_import_data_from_file_time_filter(
    mock_paths: Mock, sample_excel_data: pd.DataFrame, time_range: List[str], expected_count: int, mock_logger: Mock
) -> None:
    mock_paths.__getitem__.return_value = "test_data.xlsx"
    with patch("src.utils.pd.read_excel") as mock_read_excel:
        mock_read_excel.return_value = sample_excel_data.copy()
        result: pd.DataFrame = import_data_from_file(time_range)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == expected_count
        if time_range:
            result_dates = pd.to_datetime(result["Дата операции"], dayfirst=True)
            start = pd.to_datetime(time_range[0], dayfirst=True)
            end = pd.to_datetime(time_range[1], dayfirst=True)
            assert all((result_dates >= start) & (result_dates <= end))


@patch("src.utils.PATHS")
def test_import_data_from_file_return_types(mock_paths: Mock, mock_logger: Mock) -> None:
    test_data = pd.DataFrame({"Дата операции": ["15.05.2024 14:30:00"], "Категория": ["Тест"]})
    mock_paths.__getitem__.return_value = "test_data.xlsx"
    with patch("src.utils.pd.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_data.copy()
        result_without = import_data_from_file()
        assert result_without is mock_read_excel.return_value
        result_with = import_data_from_file(["01.05.2024", "31.05.2024"])
        assert result_with is not mock_read_excel.return_value
        original_value = mock_read_excel.return_value["Категория"].iloc[0]
        result_with["Категория"] = "Изменено"
        assert mock_read_excel.return_value["Категория"].iloc[0] == original_value


@pytest.mark.parametrize(
    "settings_data,expected_keys",
    [
        (
            {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]},
            ["user_currencies", "user_stocks"],
        ),
        ({"user_currencies": ["RUB"], "user_stocks": []}, ["user_currencies", "user_stocks"]),
        ({}, []),
    ],
)
@patch("src.utils.PATHS")
def test_get_user_settings_returns_correct_structure(
    mock_paths: Mock, settings_data: Dict[str, Any], expected_keys: List[str], mock_logger: Mock
) -> None:
    mock_paths.__getitem__.return_value = "test_settings.json"
    mock_file = mock_open(read_data=json.dumps(settings_data))
    with patch("src.utils.open", mock_file):
        with patch("src.utils.json.load") as mock_json_load:
            mock_json_load.return_value = settings_data
            result: Dict[str, Any] = get_user_settings()
            assert isinstance(result, dict)
            assert list(result.keys()) == expected_keys
            if "user_currencies" in result:
                assert isinstance(result["user_currencies"], list)
            if "user_stocks" in result:
                assert isinstance(result["user_stocks"], list)


@patch("src.utils.PATHS")
def test_get_user_settings_with_real_example(mock_paths: Mock, mock_logger: Mock) -> None:
    real_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    mock_paths.__getitem__.return_value = "test_settings.json"
    mock_file = mock_open(read_data=json.dumps(real_settings))
    with patch("src.utils.open", mock_file):
        with patch("src.utils.json.load", return_value=real_settings):
            result = get_user_settings()
            assert "user_currencies" in result
            assert "user_stocks" in result
            assert result["user_currencies"] == ["USD", "EUR"]
            assert len(result["user_stocks"]) == 5
            assert "AAPL" in result["user_stocks"]
            assert "TSLA" in result["user_stocks"]
            assert all(isinstance(currency, str) for currency in result["user_currencies"])
            assert all(isinstance(stock, str) for stock in result["user_stocks"])
