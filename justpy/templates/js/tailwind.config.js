const production = !process.env.ROLLUP_WATCH;

module.exports = {
    future: {
    purgeLayersByDefault: true,
    removeDeprecatedGapUtilities: true,
    },
    
  content: [],
  theme: {
    extend: {},
  },
    plugins: [],
     purge: {
    content: [
     "./svelte/**/*.svelte",

    ],
    enabled: production // disable purge in dev
     },
    
}
