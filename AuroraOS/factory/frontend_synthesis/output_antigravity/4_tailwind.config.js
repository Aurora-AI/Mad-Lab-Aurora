/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {

      "base-surface": "#FFFFFF",
      "text-primary": "#000000",
      "text-secondary": "#45474D",
      "action-primary": "#000000",
      "accent": "#B7BFD9"

      },
      fontFamily: {

      "sans": [
            "Inter",
            "system-ui",
            "sans-serif"
      ],
      "heading": [
            "Inter",
            "system-ui",
            "sans-serif"
      ]

      }
    }
  },
  plugins: [],
};
