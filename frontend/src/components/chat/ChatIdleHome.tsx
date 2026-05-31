import type { ReactNode } from "react";

import { ChatIdleHero } from "./ChatIdleHero";
import { ChatIdleState } from "./ChatIdleState";

interface ChatIdleHomeProps {
  composer: ReactNode;
  onStartAnalysis: () => void;
}

export function ChatIdleHome({ composer, onStartAnalysis }: ChatIdleHomeProps) {
  return (
    <div className="chat-idle-home" data-testid="chat-idle-home">
      <div className="chat-idle-home__orb chat-idle-home__orb--top" aria-hidden="true" />
      <div className="chat-idle-home__orb chat-idle-home__orb--bottom" aria-hidden="true" />
      <main className="chat-idle-home__main">
        <ChatIdleHero />
        <div className="chat-idle-home__cards">
          <div className="chat-idle-home__card" data-testid="chat-idle-welcome-card">
            <ChatIdleState onStartAnalysis={onStartAnalysis} />
          </div>
          <div
            className="chat-idle-home__card chat-idle-home__card--composer"
            data-testid="chat-idle-composer-card"
          >
            {composer}
          </div>
        </div>
      </main>
    </div>
  );
}
