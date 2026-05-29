export interface ChartSpec {
  option: Record<string, unknown>;
}

export interface ChatDalvaResponse {
  reply: string;
  model: string;
  used_database: boolean;
  data_sources?: string[];
  chart?: ChartSpec | null;
}

export interface UserChatMessage {
  kind: "user";
  id: string;
  text: string;
  sentAt: string;
}

export interface AssistantChatMessage {
  kind: "assistant";
  id: string;
  reply: string;
  model: string;
  usedDatabase: boolean;
  dataSources: string[];
  chart: ChartSpec | null;
  receivedAt: string;
}

export type ChatThreadItem = UserChatMessage | AssistantChatMessage;

export type ChatErrorKind =
  | "validation"
  | "network"
  | "model"
  | "database"
  | "unknown";

export interface ChatError {
  kind: ChatErrorKind;
  message: string;
  httpStatus?: number;
}

export const MESSAGE_MAX_LENGTH = 2000;

function hasSeries(value: unknown): value is { series: unknown[] } {
  return (
    typeof value === "object" &&
    value !== null &&
    Array.isArray((value as { series?: unknown[] }).series) &&
    ((value as { series: unknown[] }).series?.length ?? 0) > 0
  );
}

export function isRenderableChart(chart: ChartSpec | null): chart is ChartSpec {
  return chart !== null && hasSeries(chart.option);
}
