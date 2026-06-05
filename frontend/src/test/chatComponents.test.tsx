import userEvent from "@testing-library/user-event";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("echarts-for-react", () => ({
  default: () => <div data-testid="mock-chart" />,
}));

import { ChatComposer } from "../components/chat/ChatComposer";
import { ChatIdleHero } from "../components/chat/ChatIdleHero";
import { ChatDashboardCard } from "../components/chat/ChatDashboardCard";
import { ChatIdleState } from "../components/chat/ChatIdleState";
import { ChatThread } from "../components/chat/ChatThread";
import { MESSAGE_MAX_LENGTH } from "../types/chat";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("ChatDashboardCard", () => {
  it("renders dashboard CTA and calls handler on click", async () => {
    const user = userEvent.setup();
    const onOpen = vi.fn();

    render(<ChatDashboardCard onOpenDashboard={onOpen} />);
    expect(screen.getByText("Painel de KPIs")).toBeInTheDocument();
    expect(
      screen.getByText(/Gráficos e indicadores do PDV atualizados em tempo real/i),
    ).toBeInTheDocument();
    expect(screen.getByTestId("chat-dashboard-cta")).toHaveTextContent("Abrir painel");

    await user.click(screen.getByTestId("chat-dashboard-cta"));
    expect(onOpen).toHaveBeenCalledTimes(1);
  });
});

describe("ChatIdleState", () => {
  it("renders start-analysis CTA and calls handler on click", async () => {
    const user = userEvent.setup();
    const onStart = vi.fn();

    render(<ChatIdleState onStartAnalysis={onStart} />);
    expect(screen.getByTestId("chat-idle-cta")).toBeInTheDocument();

    await user.click(screen.getByTestId("chat-idle-cta"));
    expect(onStart).toHaveBeenCalledTimes(1);
  });
});

describe("ChatIdleHero", () => {
  it("renders compact variant with same title", () => {
    render(<ChatIdleHero variant="compact" />);
    expect(screen.getByTestId("chat-idle-hero")).toHaveAttribute("data-variant", "compact");
    expect(screen.getByText("Dalva")).toBeInTheDocument();
    expect(screen.getByText("KPIs e chat com seus dados")).toBeInTheDocument();
    expect(
      screen.getByText(/Acompanhe indicadores no painel ou pergunte sobre produtos/i),
    ).toBeInTheDocument();
  });
});

describe("transition tokens", () => {
  it("defines reduced-motion transition duration override", () => {
    expect(
      getComputedStyle(document.documentElement).getPropertyValue("--chat-transition-duration").trim(),
    ).toBe("300ms");
  });
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

describe("AssistantMarkdown", () => {
  it("renders bold text and bullet lists from markdown", () => {
    render(
      <ChatThread
        messages={[
          {
            kind: "assistant",
            id: "a-md",
            reply: "Ranking:\n\n- **Mini Mercado Sul**\n- **Super PDV Norte**",
            model: "gpt-4o-mini",
            usedDatabase: true,
            dataSources: ["pdv.vendas"],
            chart: null,
            receivedAt: new Date().toISOString(),
          },
        ]}
        isLoading={false}
      />,
    );

    expect(screen.getByTestId("assistant-markdown")).toBeInTheDocument();
    expect(screen.getByText("Mini Mercado Sul").tagName).toBe("STRONG");
    expect(screen.getByText("Super PDV Norte").tagName).toBe("STRONG");
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
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
