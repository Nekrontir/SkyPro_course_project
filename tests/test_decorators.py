from pathlib import Path
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.decorators import data_copy


@pytest.mark.parametrize(
    "filename_param, expected_filename",
    [
        (None, "data_spending_by_category.xlsx"),  # По умолчанию
        ("custom_report", "custom_report.xlsx"),  # С кастомным именем
    ],
)
def test_data_copy_creates_file(
    filename_param: Any,
    expected_filename: str,
    mock_decorator_paths: dict,
    sample_result_dataframe: pd.DataFrame,
    tmp_path: Path,  # Временная директория pytest
) -> None:
    """
    Тест проверяет только создание файла декоратором data_copy.
    """
    # 1. Настраиваем временную директорию для теста
    # Создаем временную папку для данных и подменяем PATHS['data']
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()

    # Создаем мок PATHS, указывающий на временную директорию
    test_paths = mock_decorator_paths.copy()
    test_paths["data"] = str(temp_data_dir)

    def t_function() -> pd.DataFrame:
        return sample_result_dataframe

    # Применяем декоратор
    decorated_function = data_copy(filename_param)(t_function)

    # 2. Мокаем зависимости и вызываем функцию
    with patch("src.decorators.PATHS", test_paths):
        # НЕ мокаем ExcelWriter - пусть создает реальный файл
        decorated_function()

    # 3. Проверяем создание файла
    expected_file_path = temp_data_dir / expected_filename

    # Файл должен существовать
    assert expected_file_path.exists(), f"Файл {expected_file_path} не создан"

    # Файл должен быть не пустым
    assert expected_file_path.stat().st_size > 0, f"Файл {expected_file_path} пустой"

    # 4. Проверяем, что файл можно прочитать как Excel
    try:
        # Пытаемся прочитать файл
        read_df = pd.read_excel(expected_file_path, sheet_name="Данные по категориям")
        # Проверяем, что прочитано хоть что-то
        assert len(read_df) > 0, f"Файл {expected_file_path} не содержит данных"
    except Exception as e:
        pytest.fail(f"Не удалось прочитать Excel файл {expected_file_path}: {e}")
