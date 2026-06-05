import { MaterialIcon } from "./MaterialIcon";

interface ChatIdleStateProps {
  onStartAnalysis?: () => void;
}

export function ChatIdleState({ onStartAnalysis }: ChatIdleStateProps) {
  return (
    <div className="chat-idle" data-testid="chat-idle-state">
      <div className="chat-idle__icon-wrap">
        <MaterialIcon name="forum" size={48} className="chat-idle__forum-icon" />
      </div>
      <h2 className="chat-idle__title">Converse com seus dados</h2>
      <p className="chat-idle__subtitle">
        Pergunte em linguagem natural e receba respostas e insights sobre o seu negócio.
      </p>
      <button
        type="button"
        className="chat-idle__cta"
        data-testid="chat-idle-cta"
        aria-label="Iniciar conversa"
        onClick={onStartAnalysis}
      >
        <MaterialIcon name="auto_awesome" size={18} filled />
        <span>Iniciar conversa</span>
      </button>
    </div>
  );
}
