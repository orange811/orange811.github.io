import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        description: z.string(),
        date: z.date().optional(),
        tags: z.array(z.string()).default([]),
        repo: z.string().url().optional(),
        link: z.string().url().optional(),
    }),
});

const publications = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        venue: z.string().optional(),
        date: z.date().optional(),
        authors: z.array(z.string()).default([]),
        link: z.string().url().optional(),
    }),
});

const art = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        medium: z.string().optional(),
        date: z.date().optional(),
        tags: z.array(z.string()).default([]),
        image: z.string().optional(),
        link: z.string().url().optional(),
    }),
});

export const collections = {
    projects,
    publications,
    art,
};
