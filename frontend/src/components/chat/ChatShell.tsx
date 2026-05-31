import type { ReactNode } from "react";

import type { ChatThreadItem } from "../../types/chat";
import { ChatIdleHero } from "./ChatIdleHero";
import { ChatIdleState } from "./ChatIdleState";
import { ChatThread } from "./ChatThread";

export type IdlePhase = "home" | "entry";

interface ChatShellProps {
  mode: "idle" | "active";
  idlePhase: IdlePhase;
  onStartAnalysis: () => void;
  composer: ReactNode;
  errorAlert?: ReactNode;
  messages: ChatThreadItem[];
  isLoading: boolean;
}

export function ChatShell({
  mode,
  idlePhase,
  onStartAnalysis,
  composer,
  errorAlert,
  messages,
  isLoading,
}: ChatShellProps) {
  const isIdle = mode === "idle";
  const isHome = isIdle && idlePhase === "home";

  return (
    <div
      className={`chat-shell chat-shell--unified chat-shell--${mode}${isIdle ? ` chat-shell--idle-${idlePhase}` : ""}`}
      data-testid="chat-shell"
      data-mode={mode}
      data-idle-phase={isIdle ? idlePhase : undefined}
    >
      <div className="chat-shell__orb chat-shell__orb--top" aria-hidden="true" />
      <div className="chat-shell__orb chat-shell__orb--bottom" aria-hidden="true" />

      <div className="chat-shell__inner chat-shell__inner--unified">
        {errorAlert}

        {isIdle ? <ChatIdleHero variant="expanded" /> : null}

        <div className="chat-shell__body">
          <div className="chat-shell__content-slot">
            <div
              className="chat-shell__welcome-layer"
              data-testid="chat-idle-welcome-card"
              aria-hidden={!isHome}
            >
              <div className="chat-shell__card">
                <ChatIdleState onStartAnalysis={onStartAnalysis} />
              </div>
            </div>

            <main
              className="chat-shell__thread-layer chat-main chat-main--active"
              data-testid="chat-main"
              aria-hidden={isIdle}
            >
              <ChatThread messages={messages} isLoading={isLoading} />
            </main>
          </div>
        </div>
      </div>

      {isIdle ? (
        <div
          className="chat-composer-wrap chat-composer-wrap--idle-entry"
          data-testid="chat-idle-composer-card"
          aria-hidden={isHome}
        >
          <div className="chat-composer-wrap__inner">{composer}</div>
        </div>
      ) : (
        <div className="chat-composer-wrap">
          <div className="chat-composer-wrap__inner">{composer}</div>
        </div>
      )}
    </div>
  );
}
