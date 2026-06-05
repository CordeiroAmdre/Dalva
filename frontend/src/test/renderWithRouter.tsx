import { render, type RenderOptions } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import type { ReactElement } from "react";

import { PageTransitionLayout } from "../components/layout/PageTransitionLayout";
import { ROUTES } from "../config/routes";
import ConversationPage from "../pages/ConversationPage";
import DashboardPage from "../pages/DashboardPage";
import HomePage from "../pages/HomePage";

interface RenderWithRouterOptions extends Omit<RenderOptions, "wrapper"> {
  initialEntries?: string[];
}

export function renderWithRouter(
  ui?: ReactElement,
  { initialEntries = [ROUTES.home], ...options }: RenderWithRouterOptions = {},
) {
  const routes = (
    <Routes>
      <Route element={<PageTransitionLayout />}>
        <Route path={ROUTES.home} element={<HomePage />} />
        <Route path={ROUTES.conversation} element={<ConversationPage />} />
        <Route path={ROUTES.dashboard} element={<DashboardPage />} />
      </Route>
      {ui ? <Route path="*" element={ui} /> : null}
    </Routes>
  );

  return render(
    <MemoryRouter initialEntries={initialEntries}>{routes}</MemoryRouter>,
    options,
  );
}

export function renderHomePage(options?: RenderWithRouterOptions) {
  return renderWithRouter(undefined, options);
}

export function renderConversationPage(options?: RenderWithRouterOptions) {
  return renderWithRouter(undefined, {
    initialEntries: [ROUTES.conversation],
    ...options,
  });
}
