import { useEffect, useRef } from "react";
import { Spin } from "antd";

import type { ChatThreadItem } from "../../types/chat";
import { AssistantBubble } from "./AssistantBubble";
import { UserBubble } from "./UserBubble";

interface ChatThreadProps {
  messages: ChatThreadItem[];
  isLoading: boolean;
}

export function ChatThread({ messages, isLoading }: ChatThreadProps) {
  const lastScrolledUserId = useRef<string | null>(null);

  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.kind !== "user") {
      return;
    }
    if (lastScrolledUserId.current === lastMessage.id) {
      return;
    }
    lastScrolledUserId.current = lastMessage.id;
    const element = document.getElementById(`user-bubble-${lastMessage.id}`);
    element?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  return (
    <div className="chat-thread-list" data-testid="chat-thread">
      {messages.map((item) =>
        item.kind === "user" ? (
          <UserBubble key={item.id} id={item.id} text={item.text} />
        ) : (
          <AssistantBubble key={item.id} message={item} />
        ),
      )}
      {isLoading ? (
        <div className="chat-loading" data-testid="chat-loading">
          <Spin tip="Consultando dados..." />
        </div>
      ) : null}
    </div>
  );
}
