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
      <h2 className="chat-idle__title">Envie uma pergunta para iniciar a conversa.</h2>
      <p className="chat-idle__subtitle">
        Dalva analisa seus dados em tempo real para fornecer respostas precisas e insights
        valiosos para o seu negócio.
      </p>
      <button
        type="button"
        className="chat-idle__cta"
        data-testid="chat-idle-cta"
        onClick={onStartAnalysis}
      >
        <MaterialIcon name="auto_awesome" size={18} filled />
        <span>Começar nova análise</span>
      </button>
    </div>
  );
}
