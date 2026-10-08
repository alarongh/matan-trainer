import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json; charset=utf-8','.css':'text/css','.woff2':'font/woff2','.pdf':'application/pdf','.svg':'image/svg+xml'};
http.createServer(async(req,res)=>{
 try {
  const requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=path.resolve(root,'.'+(requested.endsWith('/')?requested+'index.html':requested));
  if(!file.startsWith(root+path.sep)) throw new Error();
  const body=await readFile(file);
  res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});res.end(body);
 }catch{res.writeHead(404);res.end('Not found');}
}).listen(4173,'127.0.0.1',()=>console.log('http://127.0.0.1:4173'));
