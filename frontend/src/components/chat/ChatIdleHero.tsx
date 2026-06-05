import { MaterialIcon } from "./MaterialIcon";

interface ChatIdleHeroProps {
  variant?: "expanded" | "compact";
}

export function ChatIdleHero({ variant = "expanded" }: ChatIdleHeroProps) {
  return (
    <header
      className={`chat-idle-hero chat-idle-hero--${variant}`}
      data-testid="chat-idle-hero"
      data-variant={variant}
    >
      <div className="chat-idle-hero__badge">
        <MaterialIcon name="auto_awesome" filled size={14} className="chat-idle-hero__badge-icon" />
        <span>Painel + assistente</span>
      </div>
      <h1 className="chat-idle-hero__title">Dalva</h1>
      <p className="chat-idle-hero__subtitle">KPIs e chat com seus dados</p>
      <p className="chat-idle-hero__description">
        Acompanhe indicadores no painel ou pergunte sobre produtos, vendas, lojas e pagamentos.
      </p>
    </header>
  );
}
