import { ThunderboltOutlined } from "@ant-design/icons";
import { Flex, Tag, Typography } from "antd";

interface ChatIdleHeroProps {
  variant?: "expanded" | "compact";
}

export function ChatIdleHero({ variant = "expanded" }: ChatIdleHeroProps) {
  return (
    <Flex
      component="header"
      className={`chat-idle-hero chat-idle-hero--${variant}`}
      data-testid="chat-idle-hero"
      data-variant={variant}
      vertical
      align="center"
    >
      <Tag icon={<ThunderboltOutlined />} className="chat-idle-hero__badge">
        Painel + assistente
      </Tag>
      <Typography.Title level={1} className="chat-idle-hero__title">
        Dalva
      </Typography.Title>
      <Typography.Text className="chat-idle-hero__subtitle">
        KPIs e chat com seus dados
      </Typography.Text>
      <Typography.Paragraph className="chat-idle-hero__description">
        Acompanhe indicadores no painel ou pergunte sobre produtos, vendas, lojas e pagamentos.
      </Typography.Paragraph>
    </Flex>
  );
}
