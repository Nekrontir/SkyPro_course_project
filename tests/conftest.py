from typing import Any, Dict, Generator
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Фикстура с тестовыми данными. Возвращает DataFrame."""
    return pd.DataFrame(
        {
            "Категория": ["Супермаркеты", "Транспорт", "Супермаркеты", "Кафе"],
            "Описание": ["Пятерочка", "Такси", "Магнит", "Старбакс"],
            "Сумма операции": [-500, -300, -200, -150],
            "Дата операции": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        }
    )


@pytest.fixture
def mock_dependencies() -> Generator[tuple[MagicMock | AsyncMock, MagicMock | AsyncMock], Any, None]:
    """
    Фикстура для мока зависимостей.
    Возвращает кортеж из двух мок-объектов.
    """
    with (
        patch("src.services.import_data_from_file") as mock_import,
        patch("src.services.logger_services_mod") as mock_logger,
    ):
        yield mock_import, mock_logger


@pytest.fixture
def mock_logger() -> Generator[MagicMock | AsyncMock, Any, None]:
    """Фикстура для мока логгера utils_module"""
    with patch("src.utils.logger_utils_mod") as mock_logger:
        yield mock_logger


@pytest.fixture
def mock_paths() -> Dict[str, str]:
    """Фикстура с моком путей"""
    return {"get_data": "test_data.xlsx", "user_settings": "test_settings.json", "logs": "test_logs"}


@pytest.fixture
def sample_excel_data() -> pd.DataFrame:
    """Фикстура с тестовыми данными Excel"""
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.05.2024 10:00:00",
                "15.05.2024 14:30:00",
                "20.05.2024 09:15:00",
                "31.05.2024 23:59:59",
            ],
            "Категория": ["Супермаркеты", "Транспорт", "Кафе", "Супермаркеты"],
            "Сумма операции": [-1000, -500, -300, -200],
        }
    )


@pytest.fixture
def mock_reports_logger() -> Generator[Mock, Any, None]:
    """Фикстура для мока логгера reports_module"""
    with patch("src.reports.logger_reports_mod") as mock_logger:
        yield mock_logger


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    """
    Фикстура с тестовыми транзакциями за разные даты.
    Специально для тестирования spending_by_category.
    """
    return pd.DataFrame(
        {
            "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт", "Кафе", "Супермаркеты"],
            "Описание": ["Пятерочка", "Магнит", "Такси", "Старбакс", "Перекресток"],
            "Сумма операции": [-500, -300, -200, -150, -400],
            "Дата операции": [
                "01.01.2024 10:00:00",  # Более 90 дней назад от 15.04.2024
                "16.01.2024 14:30:00",  # Ровно 90 дней назад от 15.04.2024 (включая границу)
                "15.02.2024 09:15:00",  # В пределах 90 дней
                "10.03.2024 12:00:00",  # В пределах 90 дней
                "05.04.2024 18:00:00",  # В пределах 90 дней
            ],
        }
    )


# @pytest.fixture(autouse=True)
# def mock_decorator() -> Generator[None, Any, None]:
#     """
#     Фикстура для мока декоратора data_copy.
#     Автоматически применяется ко всем тестам, чтобы избежать создания файлов.
#     """
#     with patch('src.reports.data_copy', lambda x: x):
#         yield

# @pytest.fixture(scope='session', autouse=True)
# def patch_decorators_import():
#     """Глобальная фикстура для подмены модуля decorators"""
#     original_sys_modules = sys.modules.copy()
#     sys.modules['decorators'] = Mock()
#     yield
#     # Восстанавливаем оригинальные модули
#     sys.modules.clear()
#     sys.modules.update(original_sys_modules)


@pytest.fixture
def mock_decorator_paths() -> dict:
    """Фикстура с моком путей для тестирования декоратора"""
    return {"data": "/fake/path/data", "logs": "/fake/path/logs"}


@pytest.fixture
def sample_result_dataframe() -> pd.DataFrame:
    """Фикстура с тестовым DataFrame для декоратора"""
    return pd.DataFrame(
        {
            "Категория": ["Супермаркеты", "Транспорт", "Кафе"],
            "Сумма операции": [-1500.50, -750.30, -450.20],
            "Дата операции": ["2024-05-01", "2024-05-02", "2024-05-03"],
        }
    )


# @pytest.fixture
# def mock_excel_writer_context() -> Mock:
#     """Фикстура для мока контекстного менеджера pd.ExcelWriter"""
#     # Создаем мок для writer, который возвращается из __enter__
#     mock_writer = Mock()
#     # Настраиваем контекстный менеджер
#     mock_context = Mock()
#     mock_context.__enter__ = Mock(return_value=mock_writer)
#     mock_context.__exit__ = Mock(return_value=None)
#     return mock_context


@pytest.fixture
def mock_views_logger() -> Generator[Mock, Any, None]:
    """Фикстура для мока логгера views_module"""
    with patch("src.views.logger_views_mod") as mock_logger:
        yield mock_logger


@pytest.fixture
def sample_processing_dataframe() -> pd.DataFrame:
    """Фикстура с тестовыми данными. Возвращает DataFrame."""
    return pd.DataFrame(
        {
            "Номер карты": ["*1111", "*2222", "*1111", "*3333"],
            "Сумма операции с округлением": [100.50, 200.75, 150.00, 300.25],
            "Сумма платежа": [100.50, 200.75, 150.00, 300.25],
            "Сумма операции": [100.50, 200.75, 150.00, 300.25],  # ← ДОБАВИТЬ ЭТОТ СТОЛБЕЦ
            "Дата платежа": ["2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04"],
            "Категория": ["Супермаркеты", "Транспорт", "Супермаркеты", "Кафе"],
            "Описание": ["Пятерочка", "Такси", "Магнит", "Старбакс"],
        }
    )


@pytest.fixture
def mock_env_vars() -> Generator[None, Any, None]:
    """Фикстура для мока переменных окружения"""
    with patch.dict("os.environ", {"API_KEY_1": "fake_api_key_1", "API_KEY_2": "fake_api_key_2"}):
        yield
