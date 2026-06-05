import { CommentOutlined, ThunderboltOutlined } from "@ant-design/icons";
import { Avatar, Button, Flex, Typography } from "antd";

interface ChatIdleStateProps {
  onStartAnalysis?: () => void;
}

export function ChatIdleState({ onStartAnalysis }: ChatIdleStateProps) {
  return (
    <Flex className="chat-idle" data-testid="chat-idle-state" vertical align="center">
      <Avatar
        className="chat-idle__icon-wrap"
        icon={<CommentOutlined className="chat-idle__forum-icon" />}
      />
      <Typography.Title level={2} className="chat-idle__title">
        Converse com seus dados
      </Typography.Title>
      <Typography.Paragraph className="chat-idle__subtitle">
        Pergunte em linguagem natural e receba respostas e insights sobre o seu negócio.
      </Typography.Paragraph>
      <Button
        type="primary"
        data-testid="chat-idle-cta"
        aria-label="Iniciar conversa"
        icon={<ThunderboltOutlined />}
        onClick={onStartAnalysis}
      >
        Iniciar conversa
      </Button>
    </Flex>
  );
}
