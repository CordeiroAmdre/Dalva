import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse, delay } from "msw";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { API_BASE_URL } from "../config/api";
import { MESSAGE_MAX_LENGTH } from "../types/chat";
import { renderConversationPage } from "./renderWithRouter";
import { server } from "./mswServer";

vi.mock("echarts-for-react", () => ({
  default: () => <div data-testid="mock-chart" />,
}));

function getComposerInput() {
  return screen.getByRole("textbox");
}

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("ConversationPage", () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockImplementation((query: string) => ({
      matches: query.includes("max-width: 991px") ? false : false,
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));
  });

  it("shows composer on entry without welcome cards", () => {
    renderConversationPage();

    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-layout", "conversation");
    expect(screen.getByTestId("conversation-back-link")).toBeInTheDocument();
    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-mode", "idle");
    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-idle-phase", "entry");
    expect(screen.getByTestId("chat-composer-idle")).toBeVisible();
    expect(screen.getByTestId("char-counter")).toHaveTextContent(`0/${MESSAGE_MAX_LENGTH}`);
    expect(screen.queryByTestId("chat-idle-state")).not.toBeInTheDocument();
    expect(screen.getByTestId("chat-idle-hero")).toBeInTheDocument();
  });

  it("navigates back to home when clicking back link", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.click(screen.getByTestId("conversation-back-link"));

    expect(screen.getByTestId("home-shell")).toBeInTheDocument();
    expect(screen.queryByTestId("chat-shell")).not.toBeInTheDocument();
  });

  describe("unified shell transition (US6)", () => {
    it("keeps a single ChatShell and morphs hero after first message", async () => {
      const user = userEvent.setup();
      renderConversationPage();

      await user.type(getComposerInput(), "Olá Dalva");
      await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

      await waitFor(() => {
        expect(screen.getByText("Olá Dalva")).toBeInTheDocument();
      });

      expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-mode", "active");
      expect(screen.queryByTestId("chat-idle-hero")).not.toBeInTheDocument();
      expect(screen.getByTestId("chat-composer-active")).toBeInTheDocument();
    });

    it("starts conversation via composer", async () => {
      const user = userEvent.setup();
      renderConversationPage();

      await user.type(getComposerInput(), "Primeira pergunta");
      await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

      await waitFor(() => {
        expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
      });
    });
  });

  it("sends a message and shows assistant reply in order", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.type(getComposerInput(), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Olá Dalva")).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.getByText(/Um PDV é um ponto de venda/i)).toBeInTheDocument();
    });
    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-mode", "active");
    expect(screen.getByTestId("chat-composer-active")).toBeInTheDocument();
  });

  it("shows database transparency tags for data-backed answers", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.type(getComposerInput(), "Vendas pdv hoje");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Dados do PDV")).toBeInTheDocument();
    });
    expect(screen.getByText("pdv.vendas")).toBeInTheDocument();
    expect(screen.queryByText("Resposta geral")).not.toBeInTheDocument();
  });

  it("renders a chart when chart payload is present", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.type(getComposerInput(), "Vendas pdv por categoria");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByTestId("mock-chart")).toBeInTheDocument();
    });
    expect(screen.getByTestId("embedded-chart")).toBeInTheDocument();
  });

  it("shows validation feedback for empty messages", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    expect(screen.getByText("Digite uma mensagem antes de enviar.")).toBeInTheDocument();
  });

  it("shows error alert and preserves thread on API failure", async () => {
    const user = userEvent.setup();
    renderConversationPage();

    await user.type(getComposerInput(), "Primeira pergunta");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
    });

    await user.type(getComposerInput(), "Simular erro 502");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Model provider error")).toBeInTheDocument();
    });
    expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
  });

  it("shows loading indicator while awaiting reply", async () => {
    server.use(
      http.post(`${API_BASE_URL}/dalva/chat`, async () => {
        await delay(200);
        return HttpResponse.json({
          reply: "Um PDV é um ponto de venda.",
          model: "gpt-4o-mini",
          used_database: false,
          data_sources: [],
          chart: null,
        });
      }),
    );

    const user = userEvent.setup();
    renderConversationPage();

    await user.type(getComposerInput(), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    expect(await screen.findByTestId("chat-loading")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.queryByTestId("chat-loading")).not.toBeInTheDocument();
    });
  });
});
