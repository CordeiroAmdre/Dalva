import { useNavigate } from "react-router-dom";

import { HomePageView } from "../components/home/HomePageView";
import { ROUTES } from "../config/routes";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <HomePageView
      onStartConversation={() => navigate(ROUTES.conversation)}
      onOpenDashboard={() => navigate(ROUTES.dashboard)}
    />
  );
}
