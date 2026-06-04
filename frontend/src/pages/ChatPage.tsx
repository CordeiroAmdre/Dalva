import { useRef, useState } from "react";
import { Alert } from "antd";

import { ChatComposer } from "../components/chat/ChatComposer";
import type { IdlePhase } from "../components/chat/ChatShell";
import { ChatShell } from "../components/chat/ChatShell";
import { useChatSession } from "../hooks/useChatSession";

export default function ChatPage() {
  const { messages, isLoading, error, inputError, sendMessage } = useChatSession();
  const [draft, setDraft] = useState("");
  const [idlePhase, setIdlePhase] = useState<IdlePhase>("home");
  const composerRef = useRef<HTMLTextAreaElement>(null);
  const isIdle = messages.length === 0;

  const handleSend = async () => {
    const currentDraft = draft;
    setDraft("");
    await sendMessage(currentDraft);
  };

  const handleStartAnalysis = () => {
    setIdlePhase("entry");
    window.requestAnimationFrame(() => {
      composerRef.current?.focus();
      document.getElementById("chat-composer-idle")?.focus();
    });
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

  return (
    <ChatShell
      mode={isIdle ? "idle" : "active"}
      idlePhase={idlePhase}
      onStartAnalysis={handleStartAnalysis}
      composer={composer}
      messages={messages}
      isLoading={isLoading}
      errorAlert={
        error ? (
          <Alert
            type="error"
            showIcon
            message={error.message}
            className={isIdle ? "chat-error-alert chat-error-alert--idle-home" : "chat-error-alert"}
          />
        ) : null
      }
    />
  );
}
