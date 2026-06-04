import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse, delay } from "msw";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { API_BASE_URL } from "../config/api";
import ChatPage from "../pages/ChatPage";
import { MESSAGE_MAX_LENGTH } from "../types/chat";
import { server } from "./mswServer";

vi.mock("echarts-for-react", () => ({
  default: () => <div data-testid="mock-chart" />,
}));

function getComposerInput() {
  return screen.getByRole("textbox");
}

async function revealComposer(user: ReturnType<typeof userEvent.setup>) {
  await user.click(screen.getByTestId("chat-idle-cta"));
  expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-idle-phase", "entry");
}

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("ChatPage", () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockImplementation((query: string) => ({
      matches: query.includes("max-width: 991px") ? false : false,
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));
  });

  describe("idle state (US1)", () => {
    it("shows home phase with hero, welcome card, and CTA without composer", () => {
      render(<ChatPage />);

      expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-mode", "idle");
      expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-idle-phase", "home");
      expect(screen.getByTestId("chat-idle-hero")).toHaveAttribute("data-variant", "expanded");
      expect(screen.getByText("Assistente IA")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-state")).toBeInTheDocument();
      expect(
        screen.getByText("Envie uma pergunta para iniciar a conversa."),
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Faça perguntas sobre produtos, vendas, lojas e pagamentos/i),
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Dalva analisa seus dados em tempo real/i),
      ).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-welcome-card")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-cta")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-composer-card")).toHaveAttribute("aria-hidden", "true");
      expect(screen.queryByTestId("chat-composer-idle")).not.toBeVisible();
      expect(document.querySelector(".chat-shell__orb")).toBeInTheDocument();
    });

    it("reveals composer after clicking Começar nova análise", async () => {
      const user = userEvent.setup();
      render(<ChatPage />);

      await revealComposer(user);

      expect(screen.getByTestId("chat-composer-idle")).toBeVisible();
      expect(screen.getByTestId("char-counter")).toHaveTextContent(`0/${MESSAGE_MAX_LENGTH}`);
    });
  });

  describe("unified shell transition (US6)", () => {
    it("keeps a single ChatShell and morphs hero after first message", async () => {
      const user = userEvent.setup();
      render(<ChatPage />);

      await revealComposer(user);
      await user.type(getComposerInput(), "Olá Dalva");
      await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

      await waitFor(() => {
        expect(screen.getByText("Olá Dalva")).toBeInTheDocument();
      });

      expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-mode", "active");
      expect(screen.queryByTestId("chat-idle-hero")).not.toBeInTheDocument();
      expect(screen.getByTestId("chat-composer-active")).toBeInTheDocument();
      expect(document.querySelector(".chat-shell__orb")).toBeInTheDocument();
    });

    it("starts conversation via composer after CTA transition", async () => {
      const user = userEvent.setup();
      render(<ChatPage />);

      await revealComposer(user);
      await user.type(getComposerInput(), "Primeira pergunta");
      await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

      await waitFor(() => {
        expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
      });
    });
  });

  it("sends a message and shows assistant reply in order", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await revealComposer(user);
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
    render(<ChatPage />);

    await revealComposer(user);
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
    render(<ChatPage />);

    await revealComposer(user);
    await user.type(getComposerInput(), "Vendas pdv por categoria");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByTestId("mock-chart")).toBeInTheDocument();
    });
    expect(screen.getByTestId("embedded-chart")).toBeInTheDocument();
  });

  it("shows validation feedback for empty messages", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await revealComposer(user);
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    expect(
      screen.getByText("Digite uma mensagem antes de enviar."),
    ).toBeInTheDocument();
  });

  it("shows error alert and preserves thread on API failure", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await revealComposer(user);
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
    render(<ChatPage />);

    await revealComposer(user);
    await user.type(getComposerInput(), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    expect(await screen.findByTestId("chat-loading")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.queryByTestId("chat-loading")).not.toBeInTheDocument();
    });
  });
});
