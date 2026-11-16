import http from 'node:http';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
const root=join(process.cwd(),'src');
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json'};
http.createServer((req,res)=>{let path=decodeURIComponent((req.url||'/').split('?')[0]);if(path==='/')path='/index.html';const file=normalize(join(root,path));if(!file.startsWith(root)||!existsSync(file)||!statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}res.writeHead(200,{'Content-Type':types[extname(file)]||'application/octet-stream'});createReadStream(file).pipe(res);}).listen(Number(process.env.PORT)||4173,'0.0.0.0',()=>console.log(`Practice Quiz Bank running at http://localhost:${Number(process.env.PORT)||4173}`));
