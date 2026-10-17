const fs = require('fs');
let html = fs.readFileSync('stitch_raw.html', 'utf8');

const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
if (bodyMatch) {
  html = bodyMatch[1];
}

const appCode = `export function DossierContent() {
  return (
    <div dangerouslySetInnerHTML={{ __html: \`${html.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\` }} />
  );
}
`;
fs.writeFileSync('src/DossierContent.tsx', appCode);
console.log('DossierContent.tsx generated');
