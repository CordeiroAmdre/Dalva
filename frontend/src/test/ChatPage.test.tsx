import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import ChatPage from "../pages/ChatPage";

vi.mock("echarts-for-react", () => ({
  default: () => <div data-testid="mock-chart" />,
}));

afterEach(() => {
  cleanup();
});

describe("ChatPage", () => {
  it("sends a message and shows assistant reply in order", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await user.type(screen.getByLabelText("Mensagem do chat"), "Olá Dalva");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Olá Dalva")).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.getByText(/Um PDV é um ponto de venda/i)).toBeInTheDocument();
    });
  });

  it("shows database transparency tags for data-backed answers", async () => {
    const user = userEvent.setup();
    render(<ChatPage />);

    await user.type(screen.getByLabelText("Mensagem do chat"), "Vendas pdv hoje");
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

    await user.type(
      screen.getByLabelText("Mensagem do chat"),
      "Vendas pdv por categoria",
    );
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByTestId("mock-chart")).toBeInTheDocument();
    });
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

    await user.type(screen.getByLabelText("Mensagem do chat"), "Primeira pergunta");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText("Mensagem do chat"), "Simular erro 502");
    await user.click(screen.getByRole("button", { name: /enviar mensagem/i }));

    await waitFor(() => {
      expect(screen.getByText("Model provider error")).toBeInTheDocument();
    });
    expect(screen.getByText("Primeira pergunta")).toBeInTheDocument();
  });
});
