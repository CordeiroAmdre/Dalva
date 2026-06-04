import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ConfigProvider } from "antd";
import ptBR from "antd/locale/pt_BR";

import App from "./App.tsx";
import { dalvaTheme } from "./theme/dalvaTheme";
import "antd/dist/reset.css";
import "./theme/dalvaTokens.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConfigProvider locale={ptBR} theme={dalvaTheme}>
      <App />
    </ConfigProvider>
  </StrictMode>,
);
