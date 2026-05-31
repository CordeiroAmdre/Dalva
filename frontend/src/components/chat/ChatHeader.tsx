const TITLE = "Dalva — Chat com seus dados";

export function ChatHeader() {
  return (
    <header className="chat-header chat-header--active">
      <div className="chat-header__inner">
        <h1 className="chat-header__title">{TITLE}</h1>
      </div>
    </header>
  );
}
