from langchain_core.prompts import ChatPromptTemplate

chart_option_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You generate Apache ECharts configuration objects as JSON.\n"
            "Return ONLY valid JSON (no markdown fences, no commentary).\n"
            "The JSON must be a single ECharts `option` object with a `series` array.\n"
            "When requested_chart_type is provided, every series[].type MUST match it.\n"
            "Do not include JavaScript functions, callbacks, or formatter strings with code.\n"
            "Prefer Portuguese labels in titles and axis names when the user writes in Portuguese.\n"
            "Keep at most 100 data points per series.\n\n"
            "Minimal valid shapes by type:\n"
            "- scatter: xAxis/yAxis type value, series[].data as [[x,y],...]\n"
            "- heatmap: xAxis/yAxis categories, series type heatmap, data [xIdx,yIdx,value]\n"
            "- radar: radar.indicator array, series type radar with data values\n"
            "- treemap: series type treemap, data tree with name/value/children\n"
            "- sunburst: series type sunburst, hierarchical data with name/value/children\n"
            "- funnel: series type funnel, data [{{name,value}},...]\n"
            "- sankey: series type sankey, nodes [{{name}}], links [{{source,target,value}}]\n"
            "- gauge: series type gauge, data [{{value,name}}]\n"
            "- boxplot: series type boxplot, data [[min,Q1,median,Q3,max]]\n"
            "- bar/line/pie: standard category/value axes as appropriate",
        ),
        (
            "human",
            "User question:\n{message}\n\n"
            "Requested chart type (canonical ECharts series type, or infer from message):\n"
            "{requested_chart_type}\n\n"
            "SQL result rows (from the latest successful read-only query):\n{query_data}\n\n"
            "Build the best ECharts option JSON for the requested visualization.",
        ),
    ]
)
