from dalva_backend.prompts.chart_option import chart_option_prompt


def test_chart_option_prompt_formats_without_extra_variables() -> None:
    messages = chart_option_prompt.format_messages(
        message="radar de vendas",
        query_data="('A', 10)",
        requested_chart_type="radar",
    )
    assert len(messages) == 2
    assert "radar" in messages[1].content
