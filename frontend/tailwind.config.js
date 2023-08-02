/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,ts}'],
  theme: {
    container: {
      center: true
    },
    extend: {},
  },
  daisyui: {
    themes: [
      {
        mytheme: {

          "primary": "#109382",
          "secondary": "#ce27af",
          "accent": "#f998f6",
          "neutral": "#253341",
          "base-100": "#ffffff",
          "info": "#5c7cf0",
          "success": "#1c9282",
          "warning": "#bc7f06",
          "error": "#e1376d",
        },
      },
      {
        dark: {
          ...require("daisyui/src/theming/themes")["[data-theme=dark]"],
          "primary": "#dd7cb3",
          "secondary": "#9ebc31",
        },
      },
    ],
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("daisyui")
  ],
}

