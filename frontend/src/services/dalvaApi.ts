import type { ChatDalvaResponse, ChatError, ChatErrorKind } from "../types/chat";
import { API_BASE_URL } from "../config/api";

const SECRET_PATTERNS = [
  /sk-[a-zA-Z0-9]+/,
  /postgresql/i,
  /duckdb:\/\//i,
  /Traceback \(most recent call last\)/,
];

function getBaseUrl(): string {
  return API_BASE_URL;
}

function sanitizeDetail(detail: string): string {
  for (const pattern of SECRET_PATTERNS) {
    if (pattern.test(detail)) {
      return "Ocorreu um erro inesperado. Tente novamente.";
    }
  }
  return detail;
}

function mapStatusToError(status: number, detail: string): ChatError {
  const safeDetail = sanitizeDetail(detail);
  if (status === 422) {
    return {
      kind: "validation",
      message: safeDetail || "Mensagem inválida.",
      httpStatus: status,
    };
  }
  if (status === 502) {
    return {
      kind: "model",
      message: safeDetail || "Erro no provedor do modelo. Tente novamente.",
      httpStatus: status,
    };
  }
  if (status === 503) {
    return {
      kind: "database",
      message:
        safeDetail ||
        "Banco de dados indisponível. Verifique se o DuckDB foi inicializado.",
      httpStatus: status,
    };
  }
  return {
    kind: "unknown",
    message: safeDetail || "Erro inesperado. Tente novamente.",
    httpStatus: status,
  };
}

export async function postChat(message: string): Promise<ChatDalvaResponse> {
  let response: Response;
  try {
    response = await fetch(`${getBaseUrl()}/dalva/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
  } catch {
    const error: ChatError = {
      kind: "network",
      message:
        "Não foi possível conectar ao servidor. Verifique se a API está rodando em http://127.0.0.1:8000.",
    };
    throw error;
  }

  if (!response.ok) {
    let detail = "";
    try {
      const payload = (await response.json()) as { detail?: string };
      detail = payload.detail ?? "";
    } catch {
      detail = "";
    }
    throw mapStatusToError(response.status, detail);
  }

  return (await response.json()) as ChatDalvaResponse;
}

export function isChatError(value: unknown): value is ChatError {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const candidate = value as ChatError;
  const kinds: ChatErrorKind[] = [
    "validation",
    "network",
    "model",
    "database",
    "unknown",
  ];
  return kinds.includes(candidate.kind) && typeof candidate.message === "string";
}
