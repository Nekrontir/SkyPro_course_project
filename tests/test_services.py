import json
from typing import Tuple
from unittest.mock import Mock

import pandas as pd
import pytest

from src.services import searching


@pytest.mark.parametrize(
    "search_word,expected_count",
    [
        ("супермаркеты", 2),
        ("магнит", 1),
        ("транспорт", 1),
        ("несуществующее", 0),
    ],
)
def test_searching_finds_transactions(
    search_word: str, expected_count: int, sample_dataframe: pd.DataFrame, mock_dependencies: Tuple[Mock, Mock]
) -> None:
    mock_import, mock_logger = mock_dependencies
    mock_import.return_value = sample_dataframe
    result_json: str = searching(search_word)
    result: list = json.loads(result_json)
    assert len(result) == expected_count
    mock_import.assert_called_once()
    if expected_count > 0:
        for item in result:
            word_lower: str = search_word.lower()
            category: str = item["Категория"].lower()
            description: str = item["Описание"].lower()
            assert word_lower in category or word_lower in description


def test_searching_empty_result(mock_dependencies: Tuple[Mock, Mock], sample_dataframe: pd.DataFrame) -> None:
    mock_import, mock_logger = mock_dependencies
    mock_import.return_value = sample_dataframe
    result_json: str = searching("абсолютно_несуществующее_слово_123")
    result: list = json.loads(result_json)
    assert isinstance(result, list)
    assert len(result) == 0
    assert mock_logger.info.called
