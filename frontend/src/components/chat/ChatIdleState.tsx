import { MaterialIcon } from "./MaterialIcon";

export function ChatIdleState() {
  return (
    <div className="chat-idle" data-testid="chat-idle-state">
      <div className="chat-idle__icon-wrap">
        <MaterialIcon name="forum" filled size={48} className="" />
        <div className="chat-idle__badge">
          <MaterialIcon name="insights" filled size={16} />
        </div>
      </div>
      <h2 className="chat-idle__title">Envie uma pergunta para iniciar a conversa.</h2>
      <p className="chat-idle__subtitle">Sua assistente analítica está pronta para ajudar.</p>
    </div>
  );
}
