from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_builder import ChartBuilder


def test_from_result_preview_builds_pie_option() -> None:
    preview = "('Bebidas', 1200.5)\n('Laticínios', 980.0)\n('Padaria', 750.25)"

    chart = ChartBuilder.from_result_preview(preview)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "pie"


def test_from_result_preview_parses_decimal_strings() -> None:
    preview = (
        "('Bebidas', Decimal('1200.5'))\n"
        "('Laticínios', Decimal('980.0'))"
    )

    chart = ChartBuilder.from_result_preview(preview)

    assert chart is not None
    series = chart.option["series"][0]
    assert series["type"] == "pie"


def test_from_result_preview_builds_line_option_for_dates() -> None:
    preview = (
        "('2026-05-01', 100.0)\n"
        "('2026-05-02', 150.0)\n"
        "('2026-05-03', 120.0)"
    )

    chart = ChartBuilder.from_result_preview(preview)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "line"


def test_from_result_preview_builds_boxplot_option() -> None:
    preview = "\n".join(f"({value},)" for value in [10, 12, 14, 11, 16, 9, 13])

    chart = ChartBuilder.from_result_preview(preview)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "boxplot"


def test_from_result_preview_returns_none_for_insufficient_rows() -> None:
    preview = "('Bebidas', 1200.5)"

    assert ChartBuilder.from_result_preview(preview) is None


def test_from_result_preview_builds_bar_option_from_three_columns() -> None:
    preview = (
        "('Mini Mercado Sul', 'Café Expresso', 225)\n"
        "('Mini Mercado Sul', 'Bolo de Chocolate', 202)\n"
        "('Super PDV Norte', 'Bolo de Chocolate', 185)"
    )

    chart = ChartBuilder.from_result_preview(preview)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "bar"
    assert chart.option["xAxis"]["data"][0] == "Mini Mercado Sul — Café Expresso"


def test_from_query_log_skips_non_chartable_last_query() -> None:
    entries = [
        QueryExecution(
            sql="SELECT loja, produto, qty FROM sales",
            status=QueryStatus.SUCCESS,
            row_count=3,
            result_preview=(
                "('Loja A', 'Produto 1', 10)\n"
                "('Loja B', 'Produto 2', 20)"
            ),
        ),
        QueryExecution(
            sql="SELECT COUNT(*) FROM sales",
            status=QueryStatus.SUCCESS,
            row_count=1,
            result_preview="(1,)",
        ),
    ]

    chart = ChartBuilder.from_query_log(entries)

    assert chart is not None
    assert chart.option["series"][0]["type"] == "bar"
