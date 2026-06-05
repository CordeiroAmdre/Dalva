import type { ReactNode } from "react";

import { ROUTES } from "../../config/routes";
import type { ChatThreadItem } from "../../types/chat";
import { PageBackLink } from "../layout/PageBackLink";
import { ChatIdleHero } from "./ChatIdleHero";
import { ChatThread } from "./ChatThread";

export type ChatShellProps = {
  mode: "idle" | "active";
  composer: ReactNode;
  messages: ChatThreadItem[];
  isLoading: boolean;
  errorAlert?: ReactNode;
};

export function ChatShell(props: ChatShellProps) {
  const { mode, composer, messages, isLoading, errorAlert } = props;
  const isIdle = mode === "idle";
  const shellPhaseClass = isIdle ? "chat-shell--idle-entry" : "chat-shell--active";

  return (
    <div
      className={`chat-shell chat-shell--unified chat-shell--${mode} ${shellPhaseClass}`}
      data-testid="chat-shell"
      data-mode={mode}
      data-layout="conversation"
      data-idle-phase={isIdle ? "entry" : undefined}
    >
      <div className="chat-shell__orb chat-shell__orb--top" aria-hidden="true" />
      <div className="chat-shell__orb chat-shell__orb--bottom" aria-hidden="true" />

      <header className="dashboard-page__header">
        <PageBackLink to={ROUTES.home} label="Voltar ao início" testId="conversation-back-link" />
      </header>

      <div className="chat-shell__inner chat-shell__inner--unified">
        {errorAlert}

        {isIdle ? <ChatIdleHero variant="expanded" /> : null}

        <div className="chat-shell__body">
          <div className="chat-shell__content-slot">
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

      <div
        className={`chat-composer-wrap${isIdle ? " chat-composer-wrap--idle-entry" : ""}`}
        data-testid="chat-idle-composer-card"
      >
        <div className="chat-composer-wrap__inner">{composer}</div>
      </div>
    </div>
  );
}
