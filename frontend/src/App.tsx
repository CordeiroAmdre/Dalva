import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { PageTransitionLayout } from "./components/layout/PageTransitionLayout";
import { ROUTES } from "./config/routes";
import ConversationPage from "./pages/ConversationPage";
import DashboardPage from "./pages/DashboardPage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PageTransitionLayout />}>
          <Route path={ROUTES.home} element={<HomePage />} />
          <Route path={ROUTES.conversation} element={<ConversationPage />} />
          <Route path={ROUTES.dashboard} element={<DashboardPage />} />
        </Route>
        <Route path="*" element={<Navigate to={ROUTES.home} replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
