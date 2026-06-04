import json
from pathlib import Path
from unittest.mock import MagicMock

from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_resolver import resolve_chart

_BASELINE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "chart_regression_baseline.json"


def test_regression_no_extra_charts_vs_baseline() -> None:
    baseline = json.loads(_BASELINE_PATH.read_text(encoding="utf-8"))
    repository = MagicMock()

    for case in baseline["cases"]:
        query_log = [
            QueryExecution(
                sql="SELECT 1",
                status=QueryStatus.SUCCESS,
                row_count=2,
                result_preview=case["query_preview"],
            )
        ]
        chart = resolve_chart(case["message"], query_log, repository)
        has_chart = chart is not None
        assert has_chart == case["expect_chart"], (
            f"message={case['message']!r} expected has_chart={case['expect_chart']}, got {has_chart}"
        )
