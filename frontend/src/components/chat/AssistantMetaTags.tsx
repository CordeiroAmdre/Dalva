import { MaterialIcon } from "./MaterialIcon";

interface AssistantMetaTagsProps {
  usedDatabase: boolean;
  dataSources: string[];
  model: string;
}

export function AssistantMetaTags({
  usedDatabase,
  dataSources,
  model,
}: AssistantMetaTagsProps) {
  return (
    <div className="assistant-meta" data-testid="assistant-meta">
      {usedDatabase ? (
        <span className="assistant-meta__tag assistant-meta__tag--db">
          <MaterialIcon name="check_circle" filled size={14} />
          Dados do PDV
        </span>
      ) : null}
      {dataSources.map((source) => (
        <span key={source} className="assistant-meta__tag assistant-meta__tag--source">
          {source}
        </span>
      ))}
      {model ? <span className="assistant-meta__model">{model}</span> : null}
    </div>
  );
}
