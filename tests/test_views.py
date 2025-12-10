import json
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

# Импортируем функции из views
from src.views import (get_card_info, get_currency_course, get_main_web_json_answer, get_stock_price,
                       get_top_five_transactions, greeting)


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (5, "Доброе утро"),
        (12, "Добрый день"),
        (18, "Добрый вечер"),
        (23, "Доброй ночи"),
        (25, "Доброго времени суток"),
    ],
)
def test_greeting_returns_correct_message(hour: int, expected_greeting: str, mock_views_logger: Mock) -> None:
    result = greeting(hour)
    assert result == expected_greeting
    mock_views_logger.info.assert_called()


def test_get_card_info_returns_correct_structure(
    sample_processing_dataframe: pd.DataFrame, mock_views_logger: Mock
) -> None:
    result = get_card_info(sample_processing_dataframe)
    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert "last_digits" in item
        assert "total_spent" in item
        assert "cashback" in item
        expected_cashback = round(item["total_spent"] / 100, 2)
        assert item["cashback"] == expected_cashback
    mock_views_logger.info.assert_called()


def test_get_top_five_transactions_returns_top_five(mock_views_logger: Mock) -> None:
    test_df = pd.DataFrame(
        {
            "Сумма платежа": [500.00, 400.00, 300.00, 200.00, 100.00],
            "Сумма операции": [500.00, 400.00, 300.00, 200.00, 100.00],
            "Дата платежа": ["2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05"],
            "Категория": ["Супермаркеты", "Транспорт", "Кафе", "Супермаркеты", "Транспорт"],
            "Описание": ["Магнит", "Такси", "Кофейня", "Пятерочка", "Метро"],
        }
    )
    result = get_top_five_transactions(test_df)
    assert isinstance(result, list)
    assert len(result) == 5
    amounts = [item["amount"] for item in result]
    assert amounts == [500.00, 400.00, 300.00, 200.00, 100.00]
    for item in result:
        assert "date" in item
        assert "amount" in item
        assert "category" in item
        assert "description" in item
    mock_views_logger.info.assert_called()


@patch("src.views.requests.get")
def test_get_currency_course_calls_api_correctly(
    mock_requests_get: Mock, mock_views_logger: Mock, mock_env_vars: None
) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rates": {"RUB": 75.50}}
    mock_requests_get.return_value = mock_response
    test_settings = {"user_currencies": ["USD", "EUR"]}
    result = get_currency_course(test_settings)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 75.50
    assert result[1]["currency"] == "EUR"
    assert result[1]["rate"] == 75.50
    assert mock_requests_get.call_count == 2
    mock_views_logger.info.assert_called()


@patch("src.views.finnhub.Client")
def test_get_stock_price_calls_api_correctly(
    mock_finnhub_client: Mock, mock_views_logger: Mock, mock_env_vars: None
) -> None:
    mock_client_instance = Mock()
    mock_client_instance.quote.return_value = {"c": 150.75}
    mock_finnhub_client.return_value = mock_client_instance
    test_settings = {"user_stocks": ["AAPL", "TSLA"]}
    result = get_stock_price(test_settings)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.75
    assert result[1]["stock"] == "TSLA"
    assert result[1]["price"] == 150.75
    assert mock_client_instance.quote.call_count == 2
    mock_views_logger.info.assert_called()


def test_get_main_web_json_answer_returns_valid_json(mock_views_logger: Mock) -> None:
    with (
        patch("src.views.greeting") as mock_greeting,
        patch("src.views.get_card_info") as mock_cards,
        patch("src.views.get_top_five_transactions") as mock_top,
        patch("src.views.get_currency_course") as mock_currency,
        patch("src.views.get_stock_price") as mock_stock,
    ):
        mock_greeting.return_value = "Добрый день"
        mock_cards.return_value = [{"last_digits": "*1111", "total_spent": 100.0, "cashback": 1.0}]
        mock_top.return_value = [{"date": "2024-05-01", "amount": 100.0, "category": "test", "description": "test"}]
        mock_currency.return_value = [{"currency": "USD", "rate": 75.5}]
        mock_stock.return_value = [{"stock": "AAPL", "price": 150.75}]
        time_str = "2024-05-01 12:00:00"
        result = get_main_web_json_answer(time_str)
        parsed_result = json.loads(result)
        assert "greeting" in parsed_result
        assert "cards" in parsed_result
        assert "top_transactions" in parsed_result
        assert "currency_rates" in parsed_result
        assert "stock_prices" in parsed_result
        hour = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").hour
        mock_greeting.assert_called_once_with(hour)
        mock_views_logger.info.assert_called()
