import { DashboardOutlined } from "@ant-design/icons";
import { Avatar, Button, Flex, Typography } from "antd";

interface ChatDashboardCardProps {
  onOpenDashboard?: () => void;
}

export function ChatDashboardCard({ onOpenDashboard }: ChatDashboardCardProps) {
  return (
    <Flex
      className="chat-dashboard-card"
      data-testid="chat-dashboard-card"
      vertical
      align="center"
    >
      <Avatar
        className="chat-dashboard-card__icon-wrap"
        icon={<DashboardOutlined className="chat-dashboard-card__icon" />}
      />
      <Typography.Title level={2} className="chat-dashboard-card__title">
        Painel de KPIs
      </Typography.Title>
      <Typography.Paragraph className="chat-dashboard-card__description">
        Gráficos e indicadores do PDV atualizados em tempo real.
      </Typography.Paragraph>
      <Button
        type="default"
        data-testid="chat-dashboard-cta"
        aria-label="Abrir painel de KPIs"
        onClick={onOpenDashboard}
      >
        Abrir painel
      </Button>
    </Flex>
  );
}
