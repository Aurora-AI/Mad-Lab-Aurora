/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {

      "base-surface": "#0A0A0C",
      "text-primary": "#FFFFFF",
      "action-primary": "#818CF8",
      "accent": "#818CF8"

      },
      fontFamily: {

      "sans": [
            "var(--aurora-font-sans)",
            "system-ui",
            "sans-serif"
      ],
      "heading": [
            "var(--aurora-font-heading)",
            "Inter",
            "sans-serif"
      ]

      }
    }
  },
  plugins: [],
};
