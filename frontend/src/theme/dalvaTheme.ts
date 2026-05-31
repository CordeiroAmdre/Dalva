import type { ThemeConfig } from "antd";

export const dalvaTheme: ThemeConfig = {
  token: {
    colorPrimary: "#8a00de",
    colorInfo: "#8a00de",
    colorBgLayout: "#f8f9ff",
    colorBgContainer: "#ffffff",
    colorText: "#0b1c30",
    colorTextSecondary: "#4e4355",
    colorBorder: "#d1c1d7",
    borderRadius: 8,
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
  },
  components: {
    Button: {
      primaryColor: "#ffffff",
    },
    Input: {
      activeBorderColor: "#8a00de",
      hoverBorderColor: "#a635fb",
    },
  },
};
