import pytest

from dalva_backend.scripts import init_db


def test_load_parquet_seed_requires_files(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    missing_dir = tmp_path / "empty_parquet"
    missing_dir.mkdir()
    monkeypatch.setattr(init_db, "PARQUET_DIR", missing_dir)

    with pytest.raises(FileNotFoundError, match="Missing Parquet seed"):
        init_db.init_database(tmp_path / "test.duckdb")
