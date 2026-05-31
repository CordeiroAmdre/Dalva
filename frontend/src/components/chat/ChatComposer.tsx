import type { KeyboardEvent, Ref } from "react";
import { Button, Input } from "antd";

import { MESSAGE_MAX_LENGTH } from "../../types/chat";
import { MaterialIcon } from "./MaterialIcon";

const { TextArea } = Input;

interface ChatComposerProps {
  variant: "idle" | "active";
  draft: string;
  onDraftChange: (value: string) => void;
  onSend: () => void;
  isLoading: boolean;
  inputError: string | null;
  inputRef?: Ref<HTMLTextAreaElement>;
}

export function ChatComposer({
  variant,
  draft,
  onDraftChange,
  onSend,
  isLoading,
  inputError,
  inputRef,
}: ChatComposerProps) {
  const charCount = draft.length;
  const isNearLimit = charCount >= MESSAGE_MAX_LENGTH * 0.9;
  const counterText = `${charCount}/${MESSAGE_MAX_LENGTH}`;

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (!event.shiftKey && event.key === "Enter") {
      event.preventDefault();
      void onSend();
    }
  };

  if (variant === "idle") {
    return (
      <div className="chat-composer chat-composer--idle-home" data-testid="chat-composer-idle">
        <div className="chat-composer__idle-row">
          <div className="chat-composer__idle-input-wrap">
            <TextArea
              id="chat-composer-idle"
              ref={inputRef}
              value={draft}
              onChange={(event) => onDraftChange(event.target.value)}
              placeholder="Ex.: Qual foi o valor total de vendas ontem?"
              aria-label="Digite sua pergunta"
              autoSize={{ minRows: 1, maxRows: 5 }}
              maxLength={MESSAGE_MAX_LENGTH}
              disabled={isLoading}
              onKeyDown={handleKeyDown}
              className="chat-composer__textarea chat-composer__textarea--idle-home"
            />
            <span
              className={`chat-composer__counter-inline ${isNearLimit ? "chat-composer__counter--warning" : ""}`}
              data-testid="char-counter"
            >
              {inputError ?? counterText}
            </span>
          </div>
          <Button
            type="primary"
            shape="circle"
            size="large"
            aria-label="Enviar mensagem"
            loading={isLoading}
            onClick={() => void onSend()}
            className="chat-composer__send-btn--gradient"
            icon={<MaterialIcon name="send" filled size={22} aria-hidden={false} />}
          />
        </div>
        <p className="chat-composer__disclaimer">
          A inteligência artificial pode cometer erros. Verifique informações importantes.
        </p>
      </div>
    );
  }

  return (
    <div className="chat-composer chat-composer--active" data-testid="chat-composer-active">
      <div className="chat-composer__input-wrap">
        <TextArea
          ref={inputRef}
          value={draft}
          onChange={(event) => onDraftChange(event.target.value)}
          placeholder="Pergunte sobre suas vendas, estoque ou desempenho..."
          aria-label="Mensagem do chat"
          autoSize={{ minRows: 1, maxRows: 5 }}
          maxLength={MESSAGE_MAX_LENGTH}
          disabled={isLoading}
          onKeyDown={handleKeyDown}
          className="chat-composer__textarea chat-composer__textarea--active"
        />
        {inputError ? (
          <span className="chat-composer__input-error" data-testid="composer-input-error">
            {inputError}
          </span>
        ) : null}
      </div>
      <Button
        type="primary"
        aria-label="Enviar mensagem"
        loading={isLoading}
        onClick={() => void onSend()}
        icon={<MaterialIcon name="send" filled size={20} aria-hidden={false} />}
        className="chat-composer__send-btn"
      />
    </div>
  );
}
