import type { ReactNode } from "react";

import { ChatIdleHero } from "../chat/ChatIdleHero";

export interface HomeShellProps {
  cards: ReactNode;
}

export function HomeShell({ cards }: HomeShellProps) {
  return (
    <div className="home-shell" data-testid="home-shell">
      <div className="home-shell__inner">
        <ChatIdleHero variant="expanded" />

        <div className="home-shell__body">
          <div className="home-shell__cards" data-testid="home-welcome-cards">
            {cards}
          </div>
        </div>
      </div>
    </div>
  );
}
