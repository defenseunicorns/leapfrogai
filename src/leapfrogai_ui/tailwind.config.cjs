import flowbitePlugin from 'flowbite/plugin';

export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      height: {
        header: '3rem'
      },
      inset: {
        header: '3rem' // Extend the `top` utility to include the header height
      },
      colors: {
        // flowbite-svelte
        primary: {
          50: '#D7D7D7',
          100: '#B8B8B8',
          200: '#989898',
          300: '#787878',
          400: '#595959',
          500: '#393939',
          600: '#323232',
          700: '#2B2B2B',
          800: '#242424',
          900: '#1D1D1D'
        },
        secondary: {
          50: '#D0D0D0',
          100: '#ABABAB',
          200: '#868686',
          300: '#616161',
          400: '#3B3B3B',
          500: '#161616',
          600: '#131313',
          700: '#111111',
          800: '#0E0E0E',
          900: '#0B0B0B'
        }
      }
    }
  },

  plugins: [flowbitePlugin]
};
