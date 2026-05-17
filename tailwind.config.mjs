/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#3b82f6',
          cyan: '#06b6d4',
          green: '#10b981',
        },
        surface: {
          dark: {
            base: '#09090b',
            card: '#111318',
            border: '#1e2330',
            'border-hover': '#2d3548',
          },
          light: {
            base: '#f8f9fb',
            card: '#ffffff',
            border: '#e8eaef',
            'border-hover': '#d1d5db',
          },
        },
        text: {
          dark: {
            primary: '#e8eaef',
            secondary: '#8b919e',
            muted: '#5c6370',
          },
          light: {
            primary: '#1a1f2b',
            secondary: '#4b5563',
            muted: '#9ca3af',
          },
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(135deg, #3b82f6, #06b6d4)',
        'gradient-accent-green': 'linear-gradient(135deg, #3b82f6, #06b6d4, #10b981)',
      },
    },
  },
  plugins: [],
};
