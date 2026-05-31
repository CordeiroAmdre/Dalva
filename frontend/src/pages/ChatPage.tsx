import { useState } from "react";
import { Alert } from "antd";

import { useChatSession } from "../hooks/useChatSession";
import { ChatComposer } from "../components/chat/ChatComposer";
import { ChatHeader } from "../components/chat/ChatHeader";
import { ChatIdleState } from "../components/chat/ChatIdleState";
import { ChatShell } from "../components/chat/ChatShell";
import { ChatThread } from "../components/chat/ChatThread";

export default function ChatPage() {
  const { messages, isLoading, error, inputError, sendMessage } = useChatSession();
  const [draft, setDraft] = useState("");
  const isIdle = messages.length === 0;
  const mode = isIdle ? "idle" : "active";

  const handleSend = async () => {
    const currentDraft = draft;
    setDraft("");
    await sendMessage(currentDraft);
  };

  return (
    <ChatShell
      composer={
        <ChatComposer
          variant={mode}
          draft={draft}
          onDraftChange={setDraft}
          onSend={handleSend}
          isLoading={isLoading}
          inputError={inputError}
        />
      }
      errorAlert={
        error ? (
          <Alert
            type="error"
            showIcon
            message={error.message}
            className="chat-error-alert"
          />
        ) : null
      }
    >
      <ChatHeader mode={mode} />
      <main
        className={`chat-main ${isIdle ? "chat-main--idle" : "chat-main--active"}`}
        data-testid="chat-main"
      >
        {isIdle ? <ChatIdleState /> : <ChatThread messages={messages} isLoading={isLoading} />}
      </main>
    </ChatShell>
  );
}
