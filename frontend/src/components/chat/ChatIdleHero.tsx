import { MaterialIcon } from "./MaterialIcon";

export function ChatIdleHero() {
  return (
    <div className="chat-idle-hero" data-testid="chat-idle-hero">
      <div className="chat-idle-hero__badge">
        <MaterialIcon name="auto_awesome" filled size={14} className="chat-idle-hero__badge-icon" />
        <span>Assistente IA</span>
      </div>
      <h1 className="chat-idle-hero__title">Dalva — Chat com seus dados</h1>
      <p className="chat-idle-hero__subtitle">
        Faça perguntas sobre produtos, vendas, lojas e pagamentos.
      </p>
    </div>
  );
}
