from dalva_backend.prompts.sql_agent import SQL_AGENT_PREFIX


def test_sql_agent_prefix_covers_unavailable_chart() -> None:
    assert "two or more chart types" in SQL_AGENT_PREFIX
    assert "could not be displayed" in SQL_AGENT_PREFIX


def test_sql_agent_prefix_no_chart_mention_when_not_requested() -> None:
    assert "did not ask for any visualization" in SQL_AGENT_PREFIX
