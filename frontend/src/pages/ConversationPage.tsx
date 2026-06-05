import { useEffect, useRef, useState } from "react";
import { Alert } from "antd";

import { ChatComposer } from "../components/chat/ChatComposer";
import { ChatShell } from "../components/chat/ChatShell";
import { useChatSession } from "../hooks/useChatSession";

export default function ConversationPage() {
  const { messages, isLoading, error, inputError, sendMessage } = useChatSession();
  const [draft, setDraft] = useState("");
  const composerRef = useRef<HTMLTextAreaElement>(null);
  const isIdle = messages.length === 0;

  useEffect(() => {
    window.requestAnimationFrame(() => {
      composerRef.current?.focus();
    });
  }, []);

  const handleSend = async () => {
    const currentDraft = draft;
    setDraft("");
    await sendMessage(currentDraft);
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
      layout="conversation"
      mode={isIdle ? "idle" : "active"}
      composer={composer}
      messages={messages}
      isLoading={isLoading}
      errorAlert={
        error ? (
          <Alert type="error" showIcon message={error.message} className="chat-error-alert" />
        ) : null
      }
    />
  );
}
