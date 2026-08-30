/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          950: "#0B0E11",
          900: "#12161B",
          800: "#1A1F26",
          700: "#242B34",
          600: "#333C48",
          400: "#8A94A3",
          200: "#D3D8E0",
        },
        signal: {
          allow: "#3FBF7F",
          verify: "#4AA8E0",
          review: "#E0A73F",
          block: "#E05B4A",
        },
      },
      fontFamily: {
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
