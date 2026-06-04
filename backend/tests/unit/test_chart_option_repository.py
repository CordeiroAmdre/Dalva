from dalva_backend.repositories.chart_option_repository import _format_query_log
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus


def test_format_query_log_uses_last_success_only() -> None:
    query_log = [
        QueryExecution(
            sql="SELECT old FROM t",
            status=QueryStatus.SUCCESS,
            row_count=1,
            result_preview="('old', 1)",
        ),
        QueryExecution(
            sql="SELECT new FROM t",
            status=QueryStatus.ERROR,
            row_count=0,
            result_preview="",
        ),
        QueryExecution(
            sql="SELECT latest FROM t",
            status=QueryStatus.SUCCESS,
            row_count=2,
            result_preview="('A', 10)\n('B', 20)",
        ),
    ]

    formatted = _format_query_log(query_log)

    assert "SELECT latest FROM t" in formatted
    assert "SELECT old FROM t" not in formatted
    assert "---" not in formatted
