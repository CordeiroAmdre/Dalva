import { useNavigate } from "react-router-dom";

import { ChatShell } from "../components/chat/ChatShell";
import { ROUTES } from "../config/routes";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <ChatShell
      layout="home"
      onStartConversation={() => navigate(ROUTES.conversation)}
      onOpenDashboard={() => navigate(ROUTES.dashboard)}
    />
  );
}
