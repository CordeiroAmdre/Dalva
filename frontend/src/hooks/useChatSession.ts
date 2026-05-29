import { useCallback, useState } from "react";

import { isChatError, postChat } from "../services/dalvaApi";
import type {
  AssistantChatMessage,
  ChatError,
  ChatThreadItem,
  UserChatMessage,
} from "../types/chat";
import { MESSAGE_MAX_LENGTH } from "../types/chat";

function createId(): string {
  return crypto.randomUUID();
}

export interface UseChatSessionResult {
  messages: ChatThreadItem[];
  isLoading: boolean;
  error: ChatError | null;
  inputError: string | null;
  sendMessage: (text: string) => Promise<void>;
}

export function useChatSession(): UseChatSessionResult {
  const [messages, setMessages] = useState<ChatThreadItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ChatError | null>(null);
  const [inputError, setInputError] = useState<string | null>(null);

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) {
      setInputError("Digite uma mensagem antes de enviar.");
      return;
    }
    if (trimmed.length > MESSAGE_MAX_LENGTH) {
      setInputError(
        `A mensagem deve ter no máximo ${MESSAGE_MAX_LENGTH} caracteres.`,
      );
      return;
    }

    setInputError(null);
    setError(null);

    const userMessage: UserChatMessage = {
      kind: "user",
      id: createId(),
      text: trimmed,
      sentAt: new Date().toISOString(),
    };
    setMessages((current) => [...current, userMessage]);
    setIsLoading(true);

    try {
      const response = await postChat(trimmed);
      const assistantMessage: AssistantChatMessage = {
        kind: "assistant",
        id: createId(),
        reply: response.reply,
        model: response.model,
        usedDatabase: response.used_database,
        dataSources: response.data_sources ?? [],
        chart: response.chart ?? null,
        receivedAt: new Date().toISOString(),
      };
      setMessages((current) => [...current, assistantMessage]);
    } catch (caught) {
      if (isChatError(caught)) {
        setError(caught);
      } else {
        setError({
          kind: "unknown",
          message: "Erro inesperado. Tente novamente.",
        });
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { messages, isLoading, error, inputError, sendMessage };
}
