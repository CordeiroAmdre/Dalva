import ReactECharts from "echarts-for-react";

import type { ChartSpec } from "../../types/chat";

interface EmbeddedChartProps {
  chart: ChartSpec;
  title?: string;
}

function extractTitle(chart: ChartSpec): string {
  const optionTitle = chart.option.title;
  if (Array.isArray(optionTitle) && optionTitle[0] && typeof optionTitle[0] === "object") {
    const text = (optionTitle[0] as { text?: string }).text;
    if (text) return text;
  }
  if (optionTitle && typeof optionTitle === "object" && !Array.isArray(optionTitle)) {
    const text = (optionTitle as { text?: string }).text;
    if (text) return text;
  }
  return "Vendas Semanais";
}

export function EmbeddedChart({ chart, title }: EmbeddedChartProps) {
  const displayTitle = title ?? extractTitle(chart);

  const themedOption = {
    ...chart.option,
    color: ["#8a00de", "#a635fb", "#6cf8bb", "#4648d4"],
  };

  return (
    <div className="embedded-chart" data-testid="embedded-chart">
      <h3 className="embedded-chart__title">{displayTitle}</h3>
      <ReactECharts
        option={themedOption}
        style={{ height: 240, width: "100%" }}
        opts={{ renderer: "canvas" }}
        notMerge
        lazyUpdate
      />
    </div>
  );
}
