import {checkAnswer as checkMath,numeric,normalize} from './answer.js';
const close=(a,b)=>Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b));
const pair=(a,b)=>[a,b];
const add=(a,b)=>pair(a[0]+b[0],a[1]+b[1]);
const mul=(a,b)=>pair(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]);
const div=(a,b)=>{const d=b[0]**2+b[1]**2;if(!d)throw Error('Деление на ноль.');return pair((a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d);};
const equal=(a,b)=>close(a[0],b[0])&&close(a[1],b[1]);
const argument=a=>Math.atan2(a[1]===0?0:a[1],a[0]);
export function complex(input){
 const s=normalize(input),tokens=s.match(/(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?|[a-z]+|[()+\-*/^]/g)||[];
 if(!s||s.length>256||tokens.join('')!==s||tokens.length>128)throw Error('Комплексное число: 2-3i, sqrt(2)*(1+i), 1/(1+i).');
 let i=0;const peek=()=>tokens[i],take=()=>tokens[i++];
 function atom(){
  const t=take();if(t==='('){const a=sum();if(take()!==')')throw Error('Проверь скобки.');return a;}
  if(t==='i')return pair(0,1);if(t==='pi')return pair(Math.PI,0);if(t==='e')return pair(Math.E,0);
  if(['sqrt','sin','cos','exp'].includes(t)){
   if(take()!=='(')throw Error('После функции нужны скобки.');const a=sum();if(take()!==')')throw Error('Проверь скобки.');
   if(t==='sqrt'){const r=Math.hypot(...a),angle=argument(a)/2;return pair(Math.sqrt(r)*Math.cos(angle),Math.sqrt(r)*Math.sin(angle));}
   if(t==='exp')return pair(Math.exp(a[0])*Math.cos(a[1]),Math.exp(a[0])*Math.sin(a[1]));
   if(!close(a[1],0))throw Error('В sin и cos здесь нужен действительный угол.');
   return pair(Math[t](a[0]),0);
  }
  if(t&&/^(?:\d|\.)/.test(t))return pair(Number(t),0);
  throw Error('Разрешены числа, i, pi, sqrt, sin, cos и exp.');
 }
 function power(){let a=atom();if(peek()==='^'){take();const b=unary();if(!close(b[1],0))throw Error('Показатель должен быть действительным.');const r=Math.hypot(...a)**b[0],angle=argument(a)*b[0];a=pair(r*Math.cos(angle),r*Math.sin(angle));}return a;}
 function unary(){if(peek()==='+'){take();return unary();}if(peek()==='-'){take();return unary().map(v=>-v);}return power();}
 function product(){let a=unary();while(i<tokens.length){const t=peek();if(t==='*'||t==='/'){take();a=t==='*'?mul(a,unary()):div(a,unary());}else if(t==='('||/^[a-z\d.]/.test(t))a=mul(a,unary());else break;}return a;}
 function sum(){let a=product();while(peek()==='+'||peek()==='-'){const t=take(),b=product();a=add(a,t==='+'?b:b.map(v=>-v));}return a;}
 const value=sum();if(i!==tokens.length||!value.every(Number.isFinite))throw Error('Проверь запись комплексного числа.');return value;
}
function matrix(text){
 let rows;
 if(text.trim().startsWith('[[')){try{rows=JSON.parse(text);}catch{throw Error('Матрица: 1 2; 3 4.');}}
 else rows=text.trim().split(/[;\n]+/).map(row=>row.trim().replace(/^\[|\]$/g,'').split(/\s+|,/).filter(Boolean));
 if(!Array.isArray(rows)||!rows.length||rows.some(r=>!Array.isArray(r)||r.length!==rows[0].length)||!rows[0].length)throw Error('Строки матрицы разделяй ;, элементы строки пробелом.');
 return rows.map(r=>r.map(v=>numeric(v)));
}
const coordinates=text=>text.trim().replace(/^\(|\)$/g,'').split(';').map(v=>v.trim());
function coefficients(text,variables){
 const sides=text.split('=');if(sides.length!==2||!sides.every(s=>s.trim()))throw Error('Уравнение записывай со знаком =, например 2x-y+4z+3=0.');
 const f=scope=>numeric(sides[0],scope)-numeric(sides[1],scope),zero=Object.fromEntries(variables.map(v=>[v,0])),c=f(zero),linear=[],square=[],cross=[];
 for(const v of variables){const p=f({...zero,[v]:1}),m=f({...zero,[v]:-1});linear.push((p-m)/2);square.push((p+m)/2-c);}
 for(let i=0;i<variables.length;i++)for(let j=i+1;j<variables.length;j++)cross.push([i,j,f({...zero,[variables[i]]:1,[variables[j]]:1})-c-linear[i]-linear[j]-square[i]-square[j]]);
 const coeff=[c,...linear,...square,...cross.map(v=>v[2])];
 for(let k=0;k<7;k++){
  const values=variables.map((_,j)=>[.37,-2,1.29,3.41,-.83,2.17,-3][(k+j)%7]),scope=Object.fromEntries(variables.map((v,j)=>[v,values[j]]));
  const predicted=c+values.reduce((a,v,j)=>a+linear[j]*v+square[j]*v*v,0)+cross.reduce((a,[i,j,b])=>a+b*values[i]*values[j],0);
  if(!close(f(scope),predicted))throw Error('Здесь нужно уравнение первой или второй степени.');
 }
 return coeff;
}
function proportional(a,b){const index=b.reduce((best,v,j)=>Math.abs(v)>Math.abs(b[best])?j:best,0),ma=Math.max(...a.map(Math.abs)),mb=Math.abs(b[index]);if(!ma||!mb)return false;const sign=Math.sign(a[index]*b[index]);return a.every((v,j)=>close(v/ma,sign*b[j]/mb));}
function affine(text){
 let expressions;
 if(/^[xyz]\s*=/.test(text.trim())){
  const parts=text.split(';').map(v=>v.trim().match(/^([xyz])\s*=\s*(.+)$/));
  if(parts.length!==3||parts.some(v=>!v)||new Set(parts.map(v=>v[1])).size!==3)throw Error('Параметрически: x=1+2t; y=3-t; z=4t.');
  expressions=['x','y','z'].map(v=>parts.find(p=>p[1]===v)[2]);
 }else if(text.includes('=')){
  const parts=text.split('=');if(parts.length!==3)throw Error('Канонически: (x-1)/2=(y-3)/(-1)=z/4.');
  expressions=['x','y','z'].map((axis,i)=>{
   const f=parts[i],zero={x:0,y:0,z:0},b=numeric(f,zero),a=numeric(f,{...zero,[axis]:1})-b;
   if(close(a,0))throw Error('Проверь каноническую запись.');
   for(const k of [-2,.37,2])for(const other of ['x','y','z'])if(!close(numeric(f,{...zero,[other]:k}),b+(other===axis?a*k:0)))throw Error('Каждая дробь должна содержать одну координату.');
   return `(t-(${b}))/(${a})`;
  });
 }else expressions=coordinates(text);
 if(expressions.length!==3)throw Error('Общее решение: (11-14t;6-4t;t).');
 const p=expressions.map(v=>numeric(v,{t:0})),d=expressions.map((v,j)=>numeric(v,{t:1})-p[j]);
 for(const t of [-2,.37,2.71])if(expressions.some((v,j)=>!close(numeric(v,{t}),p[j]+t*d[j])))throw Error('Координаты должны быть линейными по t.');
 if(d.every(v=>close(v,0)))throw Error('Нужен ненулевой направляющий вектор при параметре t.');return {p,d};
}
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const parallel=(a,b)=>{const na=Math.hypot(...a),nb=Math.hypot(...b);return !na||!nb||cross(a.map(v=>v/na),b.map(v=>v/nb)).every(v=>close(v,0));};
export function checkLinearAnswer(task,input){
 const text=String(input).trim();if(!text)return {valid:false,message:'Сначала введи ответ.'};
 try{
  if(task.kind==='fields'){
   const values=JSON.parse(text),results=task.fields.map(f=>({label:f.label,...checkLinearAnswer(f,values[f.id]??'')})),invalid=results.find(v=>!v.valid);
   if(invalid)return {valid:false,message:`${invalid.label}: ${invalid.message}`};
   return {valid:true,correct:results.every(v=>v.correct),incorrect:results.filter(v=>!v.correct).map(v=>v.label)};
  }
  let correct;
  if(task.kind==='matrix'){
   const a=matrix(text),b=matrix(task.answer);correct=a.length===b.length&&a.every((r,i)=>r.length===b[i].length&&r.every((v,j)=>close(v,b[i][j])));
  }else if(task.kind==='complex')correct=equal(complex(text),complex(task.answer));
  else if(task.kind==='complex-set'){
   const a=text.split(/[;|]/).map(complex),b=task.answer.split(';').map(complex);correct=a.length===b.length;
   for(const v of a){const i=b.findIndex(w=>equal(v,w));if(i<0){correct=false;break;}b.splice(i,1);}
  }else if(task.kind==='vector'||task.kind==='direction'){
   const a=coordinates(text).map(v=>numeric(v)),b=coordinates(task.answer).map(v=>numeric(v));
   correct=a.length===b.length&&(task.kind==='direction'?a.some(v=>!close(v,0))&&proportional(a,b):a.every((v,j)=>close(v,b[j])));
  }else if(task.kind==='equation')correct=proportional(coefficients(text,task.variables||['x','y','z']),coefficients(task.answer,task.variables||['x','y','z']));
  else if(task.kind==='line3'||task.kind==='affine'){
   const a=affine(text),b=affine(task.answer);correct=parallel(a.d,b.d)&&parallel(a.p.map((v,j)=>v-b.p[j]),b.d);
  }else if(task.kind==='system-point'){
   const a=coordinates(text).map(v=>numeric(v));correct=a.length===task.matrix[0].length&&task.matrix.every((row,i)=>close(row.reduce((sum,v,j)=>sum+v*a[j],0),task.rhs[i]));
  }else return checkMath(task,text);
  return {valid:true,correct};
 }catch(e){return {valid:false,message:e.message==='Unexpected token'? 'Проверь запись ответа.':e.message};}
}
