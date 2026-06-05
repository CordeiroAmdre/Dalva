import { Card, Space } from "antd";

import { ChatDashboardCard } from "../chat/ChatDashboardCard";
import { ChatIdleState } from "../chat/ChatIdleState";
import { HomeShell } from "./HomeShell";

interface HomePageViewProps {
  onStartConversation: () => void;
  onOpenDashboard?: () => void;
}

export function HomePageView({ onStartConversation, onOpenDashboard }: HomePageViewProps) {
  return (
    <HomeShell
      cards={
        <Space
          direction="vertical"
          size={10}
          className="home-shell__card-list"
          style={{ width: "100%" }}
        >
          <Card
            className="home-shell__card home-shell__card--dashboard"
            bordered={false}
            styles={{ body: { padding: 0 } }}
          >
            <ChatDashboardCard onOpenDashboard={onOpenDashboard} />
          </Card>
          <Card className="home-shell__card" bordered={false} styles={{ body: { padding: 0 } }}>
            <ChatIdleState onStartAnalysis={onStartConversation} />
          </Card>
        </Space>
      }
    />
  );
}
