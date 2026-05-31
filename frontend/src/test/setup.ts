import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll } from "vitest";

import "../theme/dalvaTokens.css";
import { server } from "./mswServer";

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => undefined,
    removeListener: () => undefined,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    dispatchEvent: () => false,
  }),
});

HTMLElement.prototype.scrollIntoView = () => undefined;

class ResizeObserverMock {
  observe() {
    return undefined;
  }
  unobserve() {
    return undefined;
  }
  disconnect() {
    return undefined;
  }
}

window.ResizeObserver = ResizeObserverMock;

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
