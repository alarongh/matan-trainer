import { cp, mkdir, rm, copyFile, readFile, writeFile, readdir } from 'node:fs/promises';
import {createHash} from 'node:crypto';
const hash=createHash('sha256');
for(const path of [...(await readdir('src')).sort().map(f=>'src/'+f),'data/tasks.json','data/coverage.json','data/linear-tasks.json','data/linear-coverage.json'])hash.update((await readFile(path,'utf8')).replace(/\r\n/g,'\n'));
const version=hash.digest('hex').slice(0,12);
await rm('dist', {recursive:true, force:true});
await mkdir('dist/vendor', {recursive:true});
await cp('src', 'dist', {recursive:true});
await cp('node_modules/katex/dist', 'dist/vendor/katex', {recursive:true});
await cp('node_modules/@fontsource-variable/onest/files', 'dist/fonts', {recursive:true});
await copyFile('node_modules/katex/LICENSE','dist/vendor/katex/LICENSE');
await copyFile('node_modules/@fontsource-variable/onest/LICENSE','dist/fonts/LICENSE');
await cp('sources', 'dist/sources', {recursive:true});
await copyFile('data/tasks.json','dist/tasks.json');
await copyFile('data/coverage.json','dist/coverage.json');
await copyFile('data/linear-tasks.json','dist/linear-tasks.json');
await copyFile('data/linear-coverage.json','dist/linear-coverage.json');
for(const file of ['index.html',...(await readdir('src')).filter(f=>f.endsWith('.js'))]){
 let content=(await readFile('dist/'+file,'utf8')).replace(/\r\n/g,'\n');
 content=content.replace(/(\.\/(?:[a-z-]+\.js|styles\.css|(?:linear-)?tasks\.json|(?:linear-)?coverage\.json))(?=['"])/g,`$1?v=${version}`);
 await writeFile('dist/'+file,content);
}
console.log('Built self-contained static site in dist/');
