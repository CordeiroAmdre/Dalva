import os
from pathlib import Path

import pytest

# Required before Settings is instantiated in tests
os.environ.setdefault("OPENAI_API_KEY", "test-key-for-pytest")
os.environ.setdefault("OPENAI_MODEL", "gpt-4o-mini")
os.environ.setdefault("DATABASE_QUERIES_ENABLED", "false")


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    from dalva_backend.controllers.dependencies import get_chat_service
    from dalva_backend.config import get_settings

    get_settings.cache_clear()
    get_chat_service.cache_clear()
    yield
    get_settings.cache_clear()
    get_chat_service.cache_clear()


@pytest.fixture
def duckdb_file(tmp_path: Path) -> Path:
    """Optional live DuckDB file for @pytest.mark.db tests."""
    from dalva_backend.scripts import init_db

    db_path = tmp_path / "pdv_ai.duckdb"
    init_db.init_database(db_path)
    return db_path
