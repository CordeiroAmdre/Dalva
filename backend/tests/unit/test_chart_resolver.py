from unittest.mock import MagicMock

import pytest

from dalva_backend.models.chat import ChartSpec
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_resolver import (
    count_distinct_requested_chart_types,
    detect_requested_chart_type,
    iter_requested_chart_types,
    resolve_chart,
    should_attempt_chart,
)

_CATEGORICAL_LOG = [
    QueryExecution(
        sql="SELECT cat, total FROM sales",
        status=QueryStatus.SUCCESS,
        row_count=2,
        result_preview="('A', 10)\n('B', 20)",
    )
]

_SCATTER_LOG = [
    QueryExecution(
        sql="SELECT preco, qty FROM sales",
        status=QueryStatus.SUCCESS,
        row_count=2,
        result_preview="('14.5', 3.0)\n('7.45', 3.0)",
    )
]


def test_count_distinct_requested_chart_types() -> None:
    assert count_distinct_requested_chart_types("radar de vendas") == 1
    assert count_distinct_requested_chart_types("radar e treemap de vendas") == 2
    assert count_distinct_requested_chart_types("qual o total?") == 0


def test_iter_requested_chart_types_includes_heatmap_alias() -> None:
    assert iter_requested_chart_types("mapa de calor por loja") == {"heatmap"}


def test_resolve_chart_returns_none_when_multiple_types() -> None:
    repository = MagicMock()
    chart = resolve_chart(
        "radar e treemap de vendas por categoria",
        _CATEGORICAL_LOG,
        repository,
    )
    assert chart is None
    repository.generate.assert_not_called()


def test_resolve_chart_uses_heuristic_without_llm() -> None:
    repository = MagicMock()

    chart = resolve_chart("Quais totais por categoria?", _CATEGORICAL_LOG, repository)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "pie"
    repository.generate.assert_not_called()


def test_should_attempt_chart_explicit_type_without_generic_keyword() -> None:
    assert should_attempt_chart("mostre um radar de vendas por categoria") is True
    assert should_attempt_chart("qual o total de vendas?") is False


def test_detect_requested_chart_type_single_vs_multiple() -> None:
    assert detect_requested_chart_type("radar de vendas") == "radar"
    assert detect_requested_chart_type("radar e treemap") is None


def test_resolve_chart_llm_for_radar_without_grafico() -> None:
    repository = MagicMock()
    repository.generate.return_value = ChartSpec(
        option={
            "radar": {"indicator": [{"name": "A", "max": 100}]},
            "series": [{"type": "radar", "data": [{"value": [10, 20]}]}],
        },
    )

    chart = resolve_chart(
        "mostre um radar de vendas por categoria",
        _CATEGORICAL_LOG,
        repository,
    )

    assert chart is not None
    assert chart.option["series"][0]["type"] == "radar"
    repository.generate.assert_called_once()
    _, kwargs = repository.generate.call_args
    assert kwargs.get("requested_chart_type") == "radar"


def test_resolve_chart_calls_llm_when_user_requests_boxplot_on_categorical_data() -> None:
    repository = MagicMock()
    repository.generate.return_value = ChartSpec(
        option={"series": [{"type": "boxplot", "data": [[1, 2, 3, 4, 5]]}]},
    )

    chart = resolve_chart("Faça um boxplot das vendas", _CATEGORICAL_LOG, repository)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "boxplot"
    repository.generate.assert_called_once()


def test_resolve_chart_calls_llm_when_user_requests_scatter_in_portuguese() -> None:
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
        _SCATTER_LOG,
        repository,
    )

    assert chart is not None
    assert chart.option["series"][0]["type"] == "scatter"
    repository.generate.assert_called_once()


@pytest.mark.parametrize(
    ("message", "chart_type"),
    [
        ("mostre um heatmap de vendas por loja e dia", "heatmap"),
        ("treemap de faturamento por categoria", "treemap"),
        ("sunburst das vendas por região", "sunburst"),
        ("funil de conversão por etapa", "funnel"),
        ("diagrama sankey de fluxo entre lojas", "sankey"),
        ("gauge do atingimento da meta", "gauge"),
    ],
)
def test_resolve_chart_llm_for_explicit_advanced_type(
    message: str,
    chart_type: str,
) -> None:
    repository = MagicMock()
    repository.generate.return_value = ChartSpec(
        option={"series": [{"type": chart_type, "data": []}]},
    )

    chart = resolve_chart(message, _CATEGORICAL_LOG, repository)

    assert chart is not None
    assert chart.option["series"][0]["type"] == chart_type
    repository.generate.assert_called_once()


def test_resolve_chart_heuristic_on_generic_visualization_request() -> None:
    repository = MagicMock()

    chart = resolve_chart("mostre um gráfico dos totais por categoria", _CATEGORICAL_LOG, repository)

    assert chart is not None
    repository.generate.assert_not_called()


def test_resolve_chart_returns_none_on_invalid_llm_json() -> None:
    repository = MagicMock()
    repository.generate.return_value = None

    chart = resolve_chart("mostre um radar de vendas", _CATEGORICAL_LOG, repository)

    assert chart is None


def test_resolve_chart_returns_none_when_no_successful_query() -> None:
    repository = MagicMock()
    log = [
        QueryExecution(
            sql="SELECT 1",
            status=QueryStatus.ERROR,
            row_count=0,
            result_preview="",
        )
    ]

    chart = resolve_chart("mostre um radar de vendas", log, repository)

    assert chart is None
    repository.generate.assert_not_called()
