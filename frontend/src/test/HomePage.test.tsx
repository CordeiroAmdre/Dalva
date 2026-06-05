import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { renderHomePage } from "./renderWithRouter";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("HomePage", () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockImplementation((query: string) => ({
      matches: query.includes("max-width: 991px") ? false : false,
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));
  });

  it("shows landing with hero, cards, and no composer", () => {
    renderHomePage();

    expect(screen.getByTestId("home-shell")).toBeInTheDocument();
    expect(screen.queryByTestId("chat-shell")).not.toBeInTheDocument();
    expect(screen.getByTestId("chat-idle-hero")).toHaveAttribute("data-variant", "expanded");
    expect(screen.getByText("Painel + assistente")).toBeInTheDocument();
    expect(screen.getByTestId("chat-idle-state")).toBeInTheDocument();
    expect(screen.getByText("Converse com seus dados")).toBeInTheDocument();
    expect(
      screen.getByText(/Acompanhe indicadores no painel ou pergunte sobre produtos/i),
    ).toBeInTheDocument();
    expect(screen.getByTestId("chat-dashboard-card")).toBeInTheDocument();
    expect(screen.getByTestId("chat-idle-cta")).toBeInTheDocument();
    expect(screen.queryByTestId("chat-composer-idle")).not.toBeInTheDocument();
    const homeShell = screen.getByTestId("home-shell");
    expect(homeShell.children).toHaveLength(1);
    expect(homeShell.firstElementChild).toHaveClass("home-shell__inner");
  });

  it("navigates to dashboard page when clicking Abrir painel", async () => {
    const user = userEvent.setup();
    renderHomePage();

    await user.click(screen.getByTestId("chat-dashboard-cta"));

    expect(screen.getByTestId("dashboard-page")).toBeInTheDocument();
    expect(screen.queryByTestId("home-shell")).not.toBeInTheDocument();
  });

  it("navigates to conversation page when clicking Iniciar conversa", async () => {
    const user = userEvent.setup();
    renderHomePage();

    await user.click(screen.getByTestId("chat-idle-cta"));

    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-layout", "conversation");
    expect(screen.getByTestId("chat-composer-idle")).toBeVisible();
    expect(screen.queryByTestId("chat-idle-state")).not.toBeInTheDocument();
    expect(screen.queryByTestId("home-shell")).not.toBeInTheDocument();
  });
});
