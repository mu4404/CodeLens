import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ["var(--font-mono)", "monospace"],
      },
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        accent: { DEFAULT: "#1f8a5b", soft: "#e8f4ed", border: "#bfe1cd" },
        crit: { DEFAULT: "#d23a40", soft: "#fcebec", border: "#f1c7c9" },
        warn: { DEFAULT: "#bd7a0a", soft: "#fbf1da", border: "#ecd6a1" },
        info: { DEFAULT: "#2f6fd6", soft: "#e9f1fd", border: "#c4d9f6" },
        muted: { DEFAULT: "#697079", 2: "#a2a9b2" },
        surface: { DEFAULT: "#ffffff", 2: "#f1f3f5" },
        border: "#e5e7eb",
      },
    },
  },
  plugins: [],
};
export default config;
