import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import ChatPage from "../pages/ChatPage";
import { MESSAGE_MAX_LENGTH } from "../types/chat";

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
    it("shows empty state, hero, and char counter", () => {
      render(<ChatPage />);

      expect(screen.getByTestId("chat-idle-home")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-hero")).toBeInTheDocument();
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
      expect(screen.getByTestId("char-counter")).toHaveTextContent(
        `0/${MESSAGE_MAX_LENGTH}`,
      );
      expect(screen.getByTestId("chat-idle-welcome-card")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-composer-card")).toBeInTheDocument();
      expect(screen.getByTestId("chat-composer-idle")).toBeInTheDocument();
      expect(screen.getByTestId("chat-idle-cta")).toBeInTheDocument();
    });
  });

  it("sends a message and shows assistant reply in order", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await user.type(getComposerInput(), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Olá Dalva")).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.getByText(/Um PDV é um ponto de venda/i)).toBeInTheDocument();
    });
    expect(screen.queryByTestId("chat-idle-home")).not.toBeInTheDocument();
    expect(screen.getByTestId("chat-composer-active")).toBeInTheDocument();
  });

  it("shows database transparency tags for data-backed answers", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

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

    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    expect(
      screen.getByText("Digite uma mensagem antes de enviar."),
    ).toBeInTheDocument();
  });

  it("shows error alert and preserves thread on API failure", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

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
    const user = userEvent.setup();
    render(<ChatPage />);

    await user.type(getComposerInput(), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByTestId("chat-loading")).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.queryByTestId("chat-loading")).not.toBeInTheDocument();
    });
  });
});
