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
            typography: {
                DEFAULT: {
                    css: {
                        maxWidth: 'none',
                        color: 'rgb(var(--text-primary))',
                        a: {
                            color: 'rgb(var(--space-indigo-bright))',
                            textDecoration: 'underline',
                            fontWeight: '500',
                        },
                        'a:hover': {
                            color: 'rgb(var(--cta))',
                        },
                        h1: {
                            color: 'rgb(var(--text-primary))',
                            fontWeight: '700',
                        },
                        h2: {
                            color: 'rgb(var(--text-primary))',
                            fontWeight: '700',
                        },
                        h3: {
                            color: 'rgb(var(--text-primary))',
                            fontWeight: '600',
                        },
                        h4: {
                            color: 'rgb(var(--text-primary))',
                            fontWeight: '600',
                        },
                        code: {
                            color: 'rgb(var(--text-primary))',
                            backgroundColor: 'rgb(var(--bg-secondary))',
                            borderRadius: '0.25rem',
                            padding: '0.125rem 0.25rem',
                            fontWeight: '400',
                        },
                        'code::before': {
                            content: '""',
                        },
                        'code::after': {
                            content: '""',
                        },
                        pre: {
                            backgroundColor: 'rgb(var(--bg-secondary))',
                            color: 'rgb(var(--text-primary))',
                            borderRadius: '0.5rem',
                        },
                        'pre code': {
                            backgroundColor: 'transparent',
                            padding: '0',
                        },
                        strong: {
                            color: 'rgb(var(--text-primary))',
                            fontWeight: '600',
                        },
                        blockquote: {
                            color: 'rgb(var(--text-secondary))',
                            borderLeftColor: 'rgb(var(--border-color))',
                        },
                    },
                },
            },
        },
    },
    plugins: [require('@tailwindcss/typography')],
};
