/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
    './app/**/*.{js,jsx}',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "var(--color-gray-light)",
        input: "var(--color-gray-light)",
        ring: "var(--color-primary-light)",
        background: "var(--color-white)",
        foreground: "var(--color-gray-dark)",
        primary: {
          DEFAULT: "var(--color-primary)",
          hover: "var(--color-primary-hover)",
          light: "var(--color-primary-light)",
        },
        success: "var(--color-success)",
        error: "var(--color-error)",
        gray: {
          dark: "var(--color-gray-dark)",
          medium: "var(--color-gray-medium)",
          light: "var(--color-gray-light)",
        },
      },
      borderRadius: {
        DEFAULT: "5px",
      },
      boxShadow: {
        DEFAULT: "var(--shadow-default)",
      },
      fontFamily: {
        inter: ["var(--font-inter)"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}