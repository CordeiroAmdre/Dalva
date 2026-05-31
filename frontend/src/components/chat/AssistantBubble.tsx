import type { AssistantChatMessage } from "../../types/chat";
import { isRenderableChart } from "../../types/chat";
import { AssistantMetaTags } from "./AssistantMetaTags";
import { EmbeddedChart } from "./EmbeddedChart";
import { MaterialIcon } from "./MaterialIcon";

interface AssistantBubbleProps {
  message: AssistantChatMessage;
}

export function AssistantBubble({ message }: AssistantBubbleProps) {
  return (
    <div className="assistant-row" data-testid="assistant-bubble-row">
      <div className="assistant-avatar" aria-hidden="true">
        <MaterialIcon name="analytics" filled size={18} />
      </div>
      <div className="assistant-content">
        <div className="assistant-bubble">
          <p className="assistant-bubble__text">{message.reply}</p>
          {isRenderableChart(message.chart) ? (
            <EmbeddedChart chart={message.chart} />
          ) : null}
        </div>
        <AssistantMetaTags
          usedDatabase={message.usedDatabase}
          dataSources={message.dataSources}
          model={message.model}
        />
      </div>
    </div>
  );
}
