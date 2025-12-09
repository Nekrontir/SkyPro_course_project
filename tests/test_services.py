import json
from typing import Tuple
from unittest.mock import Mock

import pandas as pd
import pytest

from src.services import searching


@pytest.mark.parametrize(
    "search_word,expected_count",
    [
        ("супермаркеты", 2),  # Регистронезависимый поиск в категории
        ("магнит", 1),  # Поиск в описании
        ("транспорт", 1),  # Точное совпадение
        ("несуществующее", 0),  # Ничего не найдено
    ],
)
def test_searching_finds_transactions(
    search_word: str, expected_count: int, sample_dataframe: pd.DataFrame, mock_dependencies: Tuple[Mock, Mock]
) -> None:
    """
    Тест 1: Проверяем корректность поиска транзакций.
    Возвращает None.
    """
    # Распаковываем моки
    mock_import, mock_logger = mock_dependencies

    # Настраиваем мок для import_data_from_file
    mock_import.return_value = sample_dataframe

    # Вызываем тестируемую функцию
    result_json: str = searching(search_word)
    result: list = json.loads(result_json)

    # Проверки
    assert len(result) == expected_count
    mock_import.assert_called_once()

    # Если ожидаем результаты, проверяем их содержимое
    if expected_count > 0:
        for item in result:
            word_lower: str = search_word.lower()
            category: str = item["Категория"].lower()
            description: str = item["Описание"].lower()
            assert word_lower in category or word_lower in description


def test_searching_empty_result(mock_dependencies: Tuple[Mock, Mock], sample_dataframe: pd.DataFrame) -> None:
    """
    Тест 2: Проверяем структуру ответа при отсутствии результатов.
    Возвращает None.
    """
    # Распаковываем моки
    mock_import, mock_logger = mock_dependencies

    # Настраиваем мок
    mock_import.return_value = sample_dataframe

    # Ищем заведомо несуществующее слово
    result_json: str = searching("абсолютно_несуществующее_слово_123")
    result: list = json.loads(result_json)

    # Проверки
    assert isinstance(result, list)
    assert len(result) == 0

    # Проверяем, что логгер вызывался
    assert mock_logger.info.called
