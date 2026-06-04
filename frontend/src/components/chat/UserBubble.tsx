import { MaterialIcon } from "./MaterialIcon";

interface UserBubbleProps {
  id: string;
  text: string;
}

export function UserBubble({ id, text }: UserBubbleProps) {
  return (
    <div className="user-bubble-wrap" data-testid="user-bubble-wrap">
      <div className="user-bubble" id={`user-bubble-${id}`} data-testid={`user-bubble-${id}`}>
        {text}
      </div>
    </div>
  );
}
