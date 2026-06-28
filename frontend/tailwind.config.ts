import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#070b10",
        panel: "#101820",
        line: "#22313d",
        mint: "#2dd4bf",
      },
    },
  },
  plugins: [],
};

export default config;
