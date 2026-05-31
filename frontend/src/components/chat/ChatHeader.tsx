const TITLE = "Dalva — Chat com seus dados";
const SUBTITLE =
  "Faça perguntas sobre produtos, vendas, lojas e pagamentos em linguagem natural.";

interface ChatHeaderProps {
  mode: "idle" | "active";
}

export function ChatHeader({ mode }: ChatHeaderProps) {
  return (
    <header
      className={`chat-header ${mode === "idle" ? "chat-header--idle" : "chat-header--active"}`}
    >
      <div className="chat-header__inner">
        <h1 className="chat-header__title">{TITLE}</h1>
        {mode === "idle" ? <p className="chat-header__subtitle">{SUBTITLE}</p> : null}
      </div>
    </header>
  );
}
