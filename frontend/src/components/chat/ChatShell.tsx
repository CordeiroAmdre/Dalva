import type { ReactNode } from "react";

import type { ChatThreadItem } from "../../types/chat";
import { ChatDashboardCard } from "./ChatDashboardCard";
import { ChatIdleHero } from "./ChatIdleHero";
import { ChatIdleState } from "./ChatIdleState";
import { ChatThread } from "./ChatThread";

type ChatShellHomeProps = {
  layout: "home";
  onStartConversation: () => void;
  onOpenDashboard?: () => void;
};

type ChatShellConversationProps = {
  layout: "conversation";
  mode: "idle" | "active";
  composer: ReactNode;
  messages: ChatThreadItem[];
  isLoading: boolean;
  errorAlert?: ReactNode;
};

export type ChatShellProps = ChatShellHomeProps | ChatShellConversationProps;

export function ChatShell(props: ChatShellProps) {
  if (props.layout === "home") {
    return (
      <div
        className="chat-shell chat-shell--unified chat-shell--idle chat-shell--idle-home"
        data-testid="chat-shell"
        data-mode="idle"
        data-layout="home"
      >
        <div className="chat-shell__orb chat-shell__orb--top" aria-hidden="true" />
        <div className="chat-shell__orb chat-shell__orb--bottom" aria-hidden="true" />

        <div className="chat-shell__inner chat-shell__inner--unified">
          <ChatIdleHero variant="expanded" />

          <div className="chat-shell__body">
            <div className="chat-shell__content-slot">
              <div className="chat-shell__welcome-layer" data-testid="chat-idle-welcome-card">
                <div className="chat-shell__welcome-cards">
                  <div className="chat-shell__card chat-shell__card--dashboard">
                    <ChatDashboardCard onOpenDashboard={props.onOpenDashboard} />
                  </div>
                  <div className="chat-shell__card">
                    <ChatIdleState onStartAnalysis={props.onStartConversation} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

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
