from langchain_core.prompts import ChatPromptTemplate

chart_option_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You generate Apache ECharts configuration objects as JSON.\n"
            "Return ONLY valid JSON (no markdown fences, no commentary).\n"
            "The JSON must be a single ECharts `option` object with a `series` array.\n"
            "Use any ECharts series type required by the user (boxplot, bar, line, pie, "
            "scatter, heatmap, etc.).\n"
            "Do not include JavaScript functions, callbacks, or formatter strings with code.\n"
            "Prefer Portuguese labels in titles and axis names when the user writes in Portuguese.\n"
            "Keep at most 100 data points per series.",
        ),
        (
            "human",
            "User question:\n{message}\n\n"
            "SQL result rows (from read-only queries):\n{query_data}\n\n"
            "Build the best ECharts option JSON for the requested visualization.",
        ),
    ]
)
