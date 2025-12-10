from pathlib import Path
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.decorators import data_copy


@pytest.mark.parametrize(
    "filename_param, expected_filename",
    [
        (None, "data_spending_by_category.xlsx"),
        ("custom_report", "custom_report.xlsx"),
    ],
)
def test_data_copy_creates_file(
    filename_param: Any,
    expected_filename: str,
    mock_decorator_paths: dict,
    sample_result_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()
    test_paths = mock_decorator_paths.copy()
    test_paths["data"] = str(temp_data_dir)

    def t_function() -> pd.DataFrame:
        return sample_result_dataframe

    decorated_function = data_copy(filename_param)(t_function)
    with patch("src.decorators.PATHS", test_paths):
        decorated_function()
    expected_file_path = temp_data_dir / expected_filename
    assert expected_file_path.exists(), f"Файл {expected_file_path} не создан"
    assert expected_file_path.stat().st_size > 0, f"Файл {expected_file_path} пустой"
    try:
        read_df = pd.read_excel(expected_file_path, sheet_name="Данные по категориям")
        assert len(read_df) > 0, f"Файл {expected_file_path} не содержит данных"
    except Exception as e:
        pytest.fail(f"Не удалось прочитать Excel файл {expected_file_path}: {e}")
