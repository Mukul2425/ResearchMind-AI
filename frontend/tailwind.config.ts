import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#f5f1e8",
        ink: "#122620",
        ember: "#d96f32",
        moss: "#2f5d50",
        sand: "#d7c6a1",
      },
      boxShadow: {
        panel: "0 12px 34px rgba(18, 38, 32, 0.15)",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};

export default config;
