const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..', 'src');
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
    out = out.replace(/text-\[rgb\(var\(--text-secondary\)\)\]/g, 'text-muted');
    out = out.replace(/text-\[rgb\(var\(--text-primary\)\)\]/g, 'text-text');
    // also handle dark: and hover: prefixes
    out = out.replace(/dark:text-\[rgb\(var\(--text-secondary\)\)\]/g, 'dark:text-muted');
    out = out.replace(/dark:text-\[rgb\(var\(--text-primary\)\)\]/g, 'dark:text-text');
    out = out.replace(/hover:text-\[rgb\(var\(--text-secondary\)\)\]/g, 'hover:text-muted');
    out = out.replace(/hover:text-\[rgb\(var\(--text-primary\)\)\]/g, 'hover:text-text');
    return out;
}

function main() {
    const files = walk(root);
    const changed = [];
    for (const f of files) {
        const rel = path.relative(path.resolve(__dirname, '..'), f);
        let content = fs.readFileSync(f, 'utf8');
        const newContent = replaceContent(content);
        if (newContent !== content) {
            fs.writeFileSync(f, newContent, 'utf8');
            changed.push(rel);
        }
    }
    console.log('Files changed:', changed.length);
    changed.forEach(x => console.log(' -', x));
}

main();
