import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("echarts-for-react", () => ({
  default: () => <div data-testid="mock-chart" />,
}));

import { ChatComposer } from "../components/chat/ChatComposer";
import { ChatThread } from "../components/chat/ChatThread";
import { MESSAGE_MAX_LENGTH } from "../types/chat";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("ChatComposer", () => {
  it("shows char counter warning at ≥90% length in idle variant", () => {
    const nearLimit = "x".repeat(Math.floor(MESSAGE_MAX_LENGTH * 0.9));

    render(
      <ChatComposer
        variant="idle"
        draft={nearLimit}
        onDraftChange={() => {}}
        onSend={() => {}}
        isLoading={false}
        inputError={null}
      />,
    );

    expect(screen.getByTestId("char-counter")).toHaveClass("chat-composer__counter--warning");
  });

  it("hides char counter in active variant", () => {
    render(
      <ChatComposer
        variant="active"
        draft=""
        onDraftChange={() => {}}
        onSend={() => {}}
        isLoading={false}
        inputError={null}
      />,
    );

    expect(screen.queryByTestId("char-counter")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Anexar")).not.toBeInTheDocument();
  });
});

describe("ChatThread scroll behavior", () => {
  it("scrolls to user bubble on user message append only", () => {
    const scrollIntoView = vi.fn();
    HTMLElement.prototype.scrollIntoView = scrollIntoView;

    const userMessage = {
      kind: "user" as const,
      id: "user-1",
      text: "Hello",
      sentAt: new Date().toISOString(),
    };

    const { rerender } = render(<ChatThread messages={[]} isLoading={false} />);

    rerender(<ChatThread messages={[userMessage]} isLoading={false} />);
    expect(scrollIntoView).toHaveBeenCalledTimes(1);

    const assistantMessage = {
      kind: "assistant" as const,
      id: "asst-1",
      reply: "Hi",
      model: "gpt-4o-mini",
      usedDatabase: false,
      dataSources: [],
      chart: null,
      receivedAt: new Date().toISOString(),
    };

    rerender(
      <ChatThread messages={[userMessage, assistantMessage]} isLoading={false} />,
    );
    expect(scrollIntoView).toHaveBeenCalledTimes(1);
  });
});

describe("EmbeddedChart", () => {
  it("renders chart without action buttons", () => {
    render(
      <ChatThread
        messages={[
          {
            kind: "assistant",
            id: "a1",
            reply: "Chart",
            model: "gpt-4o-mini",
            usedDatabase: true,
            dataSources: [],
            chart: {
              option: {
                series: [{ type: "bar", data: [1, 2] }],
              },
            },
            receivedAt: new Date().toISOString(),
          },
        ]}
        isLoading={false}
      />,
    );

    expect(screen.getByTestId("embedded-chart")).toBeInTheDocument();
    expect(screen.queryByLabelText("Baixar dados")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Expandir gráfico")).not.toBeInTheDocument();
  });
});
