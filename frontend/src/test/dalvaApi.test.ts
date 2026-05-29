import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { API_BASE_URL } from "../config/api";
import { postChat } from "../services/dalvaApi";
import { server } from "./mswServer";

describe("postChat", () => {
  it("returns parsed response on success", async () => {
    const response = await postChat("Olá");
    expect(response.reply).toContain("PDV");
    expect(response.used_database).toBe(false);
  });

  it("maps 502 to model error", async () => {
    server.use(
      http.post(`${API_BASE_URL}/dalva/chat`, () =>
        HttpResponse.json({ detail: "Model provider error" }, { status: 502 }),
      ),
    );

    await expect(postChat("teste")).rejects.toMatchObject({
      kind: "model",
      httpStatus: 502,
    });
  });

  it("maps 503 to database error", async () => {
    server.use(
      http.post(`${API_BASE_URL}/dalva/chat`, () =>
        HttpResponse.json({ detail: "Database unavailable" }, { status: 503 }),
      ),
    );

    await expect(postChat("teste")).rejects.toMatchObject({
      kind: "database",
      httpStatus: 503,
    });
  });

  it("sanitizes secret-like error details", async () => {
    server.use(
      http.post(`${API_BASE_URL}/dalva/chat`, () =>
        HttpResponse.json(
          { detail: "Failed: postgresql+psycopg://user:pass@localhost/db" },
          { status: 502 },
        ),
      ),
    );

    await expect(postChat("teste")).rejects.toMatchObject({
      kind: "model",
      message: "Ocorreu um erro inesperado. Tente novamente.",
    });
  });
});
