import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

import { API_BASE_URL } from "../config/api";

export const server = setupServer(
  http.post(`${API_BASE_URL}/dalva/chat`, async ({ request }) => {
    const body = (await request.json()) as { message: string };

    if (body.message.toLowerCase().includes("erro 502")) {
      return HttpResponse.json({ detail: "Model provider error" }, { status: 502 });
    }

    if (body.message.toLowerCase().includes("erro 503")) {
      return HttpResponse.json({ detail: "Database unavailable" }, { status: 503 });
    }

    if (body.message.toLowerCase().includes("pdv")) {
      return HttpResponse.json({
        reply: "Total de vendas: R$ 1.200,00",
        model: "gpt-4o-mini",
        used_database: true,
        data_sources: ["pdv.vendas", "pdv.categorias"],
        chart: {
          option: {
            tooltip: { trigger: "axis" },
            xAxis: { type: "category", data: ["Bebidas", "Laticínios"] },
            yAxis: { type: "value" },
            series: [{ name: "Valor", type: "bar", data: [1200, 980] }],
          },
        },
      });
    }

    return HttpResponse.json({
      reply: "Um PDV é um ponto de venda.",
      model: "gpt-4o-mini",
      used_database: false,
      data_sources: [],
      chart: null,
    });
  }),
);
