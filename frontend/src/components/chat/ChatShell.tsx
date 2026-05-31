import type { ReactNode } from "react";

interface ChatShellProps {
  children: ReactNode;
  composer: ReactNode;
  errorAlert?: ReactNode;
}

export function ChatShell({ children, composer, errorAlert }: ChatShellProps) {
  return (
    <div className="chat-shell">
      <div className="chat-shell__inner">
        {children}
        {errorAlert}
        <div className="chat-composer-wrap">
          <div className="chat-composer-wrap__inner">{composer}</div>
        </div>
      </div>
    </div>
  );
}
