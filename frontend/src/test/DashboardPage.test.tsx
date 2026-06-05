import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { ROUTES } from "../config/routes";
import { renderWithRouter } from "./renderWithRouter";

afterEach(() => {
  cleanup();
});

describe("DashboardPage", () => {
  it("renders dashboard placeholder and back link to chat", async () => {
    const user = userEvent.setup();

    renderWithRouter(undefined, { initialEntries: [ROUTES.dashboard] });

    expect(screen.getByTestId("dashboard-page")).toBeInTheDocument();
    expect(screen.getByText(/gráficos do painel serão exibidos aqui/i)).toBeInTheDocument();

    await user.click(screen.getByTestId("dashboard-back-link"));

    expect(screen.getByTestId("chat-shell")).toHaveAttribute("data-layout", "home");
  });
});
