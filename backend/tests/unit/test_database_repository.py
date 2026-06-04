from unittest.mock import MagicMock, patch

from dalva_backend.repositories.database_repository import DatabaseRepository, QueryStatus

DUCKDB_URL = "duckdb:///./data/pdv_ai.duckdb"


def test_execute_readonly_blocks_insert() -> None:
    repo = DatabaseRepository(
        database_url=DUCKDB_URL,
        schema="pdv",
    )
    result = repo.execute_readonly("INSERT INTO pdv.produtos (nome) VALUES ('x')")
    assert "Error" in result
    assert repo.query_log[0].status == QueryStatus.BLOCKED


@patch("dalva_backend.repositories.database_repository.create_engine")
def test_execute_readonly_returns_rows(mock_create_engine: MagicMock) -> None:
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchmany.return_value = [(1, "Leite")]
    mock_conn.execute.return_value = mock_result
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_conn
    mock_create_engine.return_value = mock_engine

    repo = DatabaseRepository(
        database_url=DUCKDB_URL,
        schema="pdv",
        max_rows=10,
    )
    output = repo.execute_readonly("SELECT id, nome FROM pdv.produtos LIMIT 1")

    assert "Leite" in output
    assert repo.query_log[0].status == QueryStatus.SUCCESS
    assert repo.query_log[0].row_count == 1
    assert "pdv.produtos" in repo.data_sources()


def test_data_sources_empty_without_success() -> None:
    repo = DatabaseRepository(database_url=DUCKDB_URL)
    repo.execute_readonly("DELETE FROM pdv.vendas")
    assert repo.data_sources() == []


@patch("dalva_backend.repositories.database_repository.create_engine")
def test_execute_readonly_times_out(mock_create_engine: MagicMock) -> None:
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(side_effect=lambda: (_ for _ in ()).throw(TimeoutError()))
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_engine.connect.return_value = mock_conn
    mock_create_engine.return_value = mock_engine

    repo = DatabaseRepository(
        database_url=DUCKDB_URL,
        query_timeout_sec=1,
    )
    with patch(
        "dalva_backend.repositories.database_repository.ThreadPoolExecutor"
    ) as mock_executor:
        mock_future = MagicMock()
        mock_future.result.side_effect = __import__(
            "concurrent.futures", fromlist=["TimeoutError"]
        ).TimeoutError()
        mock_executor.return_value.__enter__.return_value.submit.return_value = (
            mock_future
        )
        result = repo.execute_readonly("SELECT 1")

    assert "timed out" in result.lower()
    assert repo.query_log[-1].status == QueryStatus.TIMEOUT
