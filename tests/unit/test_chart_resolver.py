from unittest.mock import MagicMock

from dalva_backend.models.chat import ChartSpec
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_resolver import resolve_chart


def test_resolve_chart_uses_heuristic_without_llm() -> None:
    query_log = [
        QueryExecution(
            sql="SELECT a, b FROM t",
            status=QueryStatus.SUCCESS,
            row_count=2,
            result_preview="('A', 10)\n('B', 20)",
        )
    ]
    repository = MagicMock()

    chart = resolve_chart("Quais totais por categoria?", query_log, repository)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "pie"
    repository.generate.assert_not_called()


def test_resolve_chart_calls_llm_when_user_requests_boxplot_on_categorical_data() -> None:
    query_log = [
        QueryExecution(
            sql="SELECT cat, total FROM sales",
            status=QueryStatus.SUCCESS,
            row_count=2,
            result_preview="('A', 10)\n('B', 20)",
        )
    ]
    repository = MagicMock()
    repository.generate.return_value = ChartSpec(
        option={"series": [{"type": "boxplot", "data": [[1, 2, 3, 4, 5]]}]},
    )

    chart = resolve_chart("Faça um boxplot das vendas", query_log, repository)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "boxplot"
    repository.generate.assert_called_once()


def test_resolve_chart_calls_llm_when_user_requests_scatter_in_portuguese() -> None:
    query_log = [
        QueryExecution(
            sql="SELECT preco, qty FROM sales",
            status=QueryStatus.SUCCESS,
            row_count=2,
            result_preview="('14.5', 3.0)\n('7.45', 3.0)",
        )
    ]
    repository = MagicMock()
    repository.generate.return_value = ChartSpec(
        option={
            "xAxis": {"type": "value"},
            "yAxis": {"type": "value"},
            "series": [{"type": "scatter", "data": [[14.5, 3.0], [7.45, 3.0]]}],
        },
    )

    chart = resolve_chart(
        "Visualize um gráfico de dispersão: preço unitário vs quantidade vendida",
        query_log,
        repository,
    )

    assert chart is not None
    assert chart.option["series"][0]["type"] == "scatter"
    repository.generate.assert_called_once()
