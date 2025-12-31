/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Semantic brand tokens mapped to CSS variables (opacity-aware)
                brand: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--brand))'
                    return `rgb(var(--brand) / ${opacityValue})`
                },
                cta: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--cta))'
                    return `rgb(var(--cta) / ${opacityValue})`
                },
                surface: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--surface))'
                    return `rgb(var(--surface) / ${opacityValue})`
                },
                bg: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--bg))'
                    return `rgb(var(--bg) / ${opacityValue})`
                },
                text: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--text))'
                    return `rgb(var(--text) / ${opacityValue})`
                },
                muted: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--muted))'
                    return `rgb(var(--muted) / ${opacityValue})`
                },
                border: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--border))'
                    return `rgb(var(--border) / ${opacityValue})`
                },
                'on-brand': ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--on-brand))'
                    return `rgb(var(--on-brand) / ${opacityValue})`
                },
                accent: ({ opacityValue }) => {
                    if (opacityValue === undefined) return 'rgb(var(--accent))'
                    return `rgb(var(--accent) / ${opacityValue})`
                },
            },
        },
    },
    plugins: [],
};
