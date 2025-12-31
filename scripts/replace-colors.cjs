const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const exts = new Set(['.astro', '.html', '.js', '.jsx', '.ts', '.tsx', '.css', '.md', '.mdx']);

function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    let files = [];
    for (const e of entries) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) {
            if (e.name === 'node_modules' || e.name === '.git') continue;
            files = files.concat(walk(p));
        } else {
            if (exts.has(path.extname(e.name).toLowerCase())) files.push(p);
        }
    }
    return files;
}

function replaceContent(content) {
    let out = content;
    // Replace bg-slate-* -> bg-surface
    out = out.replace(/\bbg-slate-\d+\b/g, 'bg-surface');
    out = out.replace(/\bdark:bg-slate-\d+\b/g, 'dark:bg-surface');
    out = out.replace(/\bhover:bg-slate-\d+\b/g, 'hover:bg-surface');
    out = out.replace(/\bdark:hover:bg-slate-\d+\b/g, 'dark:hover:bg-surface');

    // Replace text-slate-* -> text-muted
    out = out.replace(/\btext-slate-\d+\b/g, 'text-muted');
    out = out.replace(/\bdark:text-slate-\d+\b/g, 'dark:text-muted');

    // Replace text-white -> text-on-brand, dark:text-white -> dark:text-on-brand
    out = out.replace(/\bdark:text-white\b/g, 'dark:text-on-brand');
    out = out.replace(/\btext-white\b/g, 'text-on-brand');

    // Replace border-slate-* -> border-border
    out = out.replace(/\bborder-slate-\d+\b/g, 'border-border');
    out = out.replace(/\bdark:border-slate-\d+\b/g, 'dark:border-border');

    // Replace bg-white -> bg-surface (map white surfaces to brand surface)
    out = out.replace(/\bbg-white\b/g, 'bg-surface');
    out = out.replace(/\bdark:bg-white\b/g, 'dark:bg-surface');

    // Replace hover:text-white -> hover:text-on-brand
    out = out.replace(/\bhover:text-white\b/g, 'hover:text-on-brand');

    return out;
}

function main() {
    const files = walk(root);
    const changed = [];

    for (const f of files) {
        const rel = path.relative(root, f);
        // Skip the script itself
        if (rel.startsWith('scripts')) continue;
        let content = fs.readFileSync(f, 'utf8');
        const newContent = replaceContent(content);
        if (newContent !== content) {
            fs.writeFileSync(f, newContent, 'utf8');
            changed.push(rel);
        }
    }

    console.log('Files changed:', changed.length);
    changed.slice(0, 200).forEach(x => console.log(' -', x));
}

main();
