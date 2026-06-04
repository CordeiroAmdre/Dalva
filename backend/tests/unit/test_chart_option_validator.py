from dalva_backend.services.chart_option_validator import validate_echarts_option


def test_validate_echarts_option_accepts_boxplot() -> None:
    option = {
        "series": [{"type": "boxplot", "data": [[1, 2, 3, 4, 5]]}],
    }

    assert validate_echarts_option(option) == option


def test_validate_echarts_option_rejects_missing_series() -> None:
    assert validate_echarts_option({"title": {"text": "x"}}) is None


def test_validate_echarts_option_rejects_javascript() -> None:
    option = {
        "series": [{"type": "bar", "data": [1, 2]}],
        "tooltip": {"formatter": "javascript:alert(1)"},
    }

    assert validate_echarts_option(option) is None
