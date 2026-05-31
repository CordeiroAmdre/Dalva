import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface AssistantMarkdownProps {
  content: string;
}

export function AssistantMarkdown({ content }: AssistantMarkdownProps) {
  return (
    <div className="assistant-bubble__markdown" data-testid="assistant-markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
