import type { ThemeConfig } from "antd";

export const dalvaTheme: ThemeConfig = {
  token: {
    colorPrimary: "#6b38d4",
    colorInfo: "#6b38d4",
    colorBgLayout: "#f8f9ff",
    colorBgContainer: "#ffffff",
    colorText: "#121c2a",
    colorTextSecondary: "#494454",
    colorBorder: "#cbc3d7",
    borderRadius: 12,
    fontFamily: "Manrope, -apple-system, BlinkMacSystemFont, sans-serif",
  },
  components: {
    Button: {
      primaryColor: "#ffffff",
    },
    Input: {
      activeBorderColor: "#6b38d4",
      hoverBorderColor: "#8455ef",
    },
    Card: {
      borderRadiusLG: 24,
    },
    Tag: {
      borderRadiusSM: 999,
    },
  },
};
