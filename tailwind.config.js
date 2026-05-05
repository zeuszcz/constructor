/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter Variable"', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      colors: {
        // Linear-inspired achromatic palette
        canvas: '#08090a',
        panel: '#0f1011',
        elev1: '#141518',
        elev2: '#1a1b1f',
        line: 'rgba(255,255,255,0.08)',
        lineSoft: 'rgba(255,255,255,0.05)',
        ink: {
          DEFAULT: '#f7f8f8',
          muted: '#a8aab1',
          dim: '#62666d',
        },
        accent: {
          DEFAULT: '#7170ff',
          deep: '#5e6ad2',
          glow: '#8b8aff',
        },
        success: '#27a644',
        warn: '#f5a524',
        danger: '#ef4444',
      },
      letterSpacing: {
        tight2: '-0.022em',
        tight3: '-0.032em',
      },
      boxShadow: {
        glow: '0 0 60px -10px rgba(113,112,255,0.45)',
        cardLift: '0 1px 0 rgba(255,255,255,0.04) inset, 0 20px 60px -20px rgba(0,0,0,0.6)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2.4s linear infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
    },
  },
  plugins: [],
}
