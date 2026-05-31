import { useRef, useState } from "react";
import { Alert } from "antd";

import { useChatSession } from "../hooks/useChatSession";
import { ChatComposer } from "../components/chat/ChatComposer";
import { ChatHeader } from "../components/chat/ChatHeader";
import { ChatIdleHome } from "../components/chat/ChatIdleHome";
import { ChatShell } from "../components/chat/ChatShell";
import { ChatThread } from "../components/chat/ChatThread";

export default function ChatPage() {
  const { messages, isLoading, error, inputError, sendMessage } = useChatSession();
  const [draft, setDraft] = useState("");
  const composerRef = useRef<HTMLTextAreaElement>(null);
  const isIdle = messages.length === 0;

  const handleSend = async () => {
    const currentDraft = draft;
    setDraft("");
    await sendMessage(currentDraft);
  };

  const focusComposer = () => {
    composerRef.current?.focus();
    document.getElementById("chat-composer-idle")?.focus();
  };

  const composer = (
    <ChatComposer
      variant={isIdle ? "idle" : "active"}
      draft={draft}
      onDraftChange={setDraft}
      onSend={handleSend}
      isLoading={isLoading}
      inputError={inputError}
      inputRef={composerRef}
    />
  );

  if (isIdle) {
    return (
      <>
        {error ? (
          <Alert
            type="error"
            showIcon
            message={error.message}
            className="chat-error-alert chat-error-alert--idle-home"
          />
        ) : null}
        <ChatIdleHome composer={composer} onStartAnalysis={focusComposer} />
      </>
    );
  }

  return (
    <ChatShell
      composer={composer}
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
      <ChatHeader />
      <main className="chat-main chat-main--active" data-testid="chat-main">
        <ChatThread messages={messages} isLoading={isLoading} />
      </main>
    </ChatShell>
  );
}
