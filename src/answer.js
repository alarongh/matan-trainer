// A small arithmetic parser. No eval, Function, assignment or property access.
export function normalize(input) {
 let s=String(input).trim().toLowerCase().replace(/[её]/g,'e').replace(/[−–—]/g,'-').replace(/×/g,'*').replace(/÷/g,'/').replace(/π/g,'pi').replace(/²/g,'^2').replace(/³/g,'^3');
 s=s.replace(/\\(?:left|right)|\$/g,'').replace(/\\(?:cdot|times)/g,'*').replace(/\\pi/g,'pi').replace(/\\infty/g,'infinity').replace(/\\,/g,'');
 for(let i=0;i<10;i++){
  const next=s.replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g,'(($1)/($2))').replace(/\\sqrt\{([^{}]*)\}/g,'sqrt($1)');
  if(next===s) break; s=next;
 }
 return s.replace(/[{}]/g,c=>c==='{'?'(':')').replace(/(\d),(?=\d)/g,'$1.').replace(/\s+/g,'').replace(/pi(?=[xykatlc])/g,'pi*');
}
export function numeric(input,scope={}) {
 const s=normalize(input);
 if(!s||s.length>256) throw new Error('Введите число или выражение.');
 if(['infinity','+infinity','inf','+inf','∞','+∞','бeсконeчность','+бeсконeчность'].includes(s)) return Infinity;
 if(['-infinity','-inf','-∞','-бeсконeчность'].includes(s)) return -Infinity;
 const tokens=s.match(/(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?|[a-z]+|[()+\-*/^]/g)||[];
 if(tokens.join('')!==s||tokens.length>128) throw new Error('Не удалось прочитать выражение. Пример: e^(-3), 2/3, sqrt(2).');
 let i=0;
 const peek=()=>tokens[i]; const take=()=>tokens[i++];
 const functions={sqrt:Math.sqrt,exp:Math.exp,ln:Math.log,log:Math.log,abs:Math.abs,sin:Math.sin,cos:Math.cos,tan:Math.tan,arcsin:Math.asin,arccos:Math.acos,arctan:Math.atan,arccot:x=>Math.PI/2-Math.atan(x)};
 function atom(){
  const t=take();
  if(t==='('){const n=sum();if(take()!==')')throw new Error('Проверьте скобки.');return n;}
  if(t==='e') return Math.E;if(t==='pi')return Math.PI;
  if(Object.hasOwn(scope,t))return scope[t];
  if(Object.hasOwn(functions,t)) {if(take()!=='(')throw new Error('После функции нужны скобки.');const v=sum();if(take()!==')')throw new Error('Проверьте скобки.');return functions[t](v);}
  if(t && /^(?:\d|\.)/.test(t))return Number(t);
  throw new Error('Разрешены числа, e, pi и математические функции.');
 }
 function power(){let a=atom();if(peek()==='^'){take();a=a**unary();}return a;}
 function unary(){if(peek()==='+'){take();return unary();}if(peek()==='-'){take();return -unary();}return power();}
 function product(){let a=unary();while(i<tokens.length){let p=peek();if(p==='*'||p==='/'){take();const b=unary();a=p==='*'?a*b:a/b;}else if(p==='('||/^[a-z\d.]/.test(p)){a*=unary();}else break;}return a;}
 function sum(){let a=product();while(peek()==='+'||peek()==='-'){const op=take();const b=product();a=op==='+'?a+b:a-b;}return a;}
 const result=sum();if(i!==tokens.length||!Number.isFinite(result))throw new Error('Выражение не даёт конечное число. Для бесконечности введите ∞ или -∞.');
 return result;
}
export function checkAnswer(task,input){
 const text=String(input).trim();
 if(!text)return {valid:false,message:'Сначала введите ответ.'};
 if(task.kind==='choice'){
  const labels={'чётная':'1','четная':'1','нечётная':'2','нечетная':'2','ни та ни другая':'3','никакая':'3','ни чётная, ни нечётная':'3'};
  const v=labels[text.toLowerCase()]||text;
  return (task.options?.map(o=>o.value)||['1','2','3']).includes(v)?{valid:true,correct:v===task.answer}:{valid:false,message:'Выберите один вариант.'};
 }
 if(task.kind==='multi'){
  const values=[...new Set(text.split(/[;,\s]+/).filter(Boolean))].sort();
  const allowed=task.options.map(o=>o.value);
  return values.length&&values.every(v=>allowed.includes(v))?{valid:true,correct:values.join(';')===task.answer.split(';').sort().join(';')}:{valid:false,message:'Отметь все подходящие утверждения.'};
 }
 if(task.kind==='fields'){
  try{
   const values=JSON.parse(text);const results=task.fields.map(f=>({label:f.label,...checkAnswer(f,values[f.id]??'')}));
   const invalid=results.find(r=>!r.valid);
   if(invalid)return {valid:false,message:`${invalid.label}: ${invalid.message}`};
   return {valid:true,correct:results.every(r=>r.correct),incorrect:results.filter(r=>!r.correct).map(r=>r.label)};
  }catch{return {valid:false,message:'Заполни поля ответа.'};}
 }
 if(['expression','set','points','lines'].includes(task.kind)){
  try{return {valid:true,correct:compareStructured(task,text)};}catch(e){return {valid:false,message:e.message};}
 }
 if(task.answer==='DNE')return {valid:true,correct:/^(не существует|нет|dne|не существует предела)$/i.test(text)};
 try{
  const v=numeric(text),target=numeric(task.answer);
  return {valid:true,correct:!Number.isFinite(target)?v===target:Number.isFinite(v)&&Math.abs(v-target)<= (target===0?1e-10:Math.abs(target)*1e-6)};
 }catch(e){return {valid:false,message:e.message};}
}

const close=(a,b)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b));
const none=s=>/^(нет|none|∅|пусто)$/i.test(s.trim());
function unordered(a,b,equal){
 if(a.length!==b.length)return false;
 const remaining=[...b];for(const item of a){const i=remaining.findIndex(v=>equal(item,v));if(i<0)return false;remaining.splice(i,1);}return true;
}
function expressionEqual(input,target,variables=[]){
 // Numerical equivalence at varied fixed samples, not a symbolic proof. No arbitrary code.
 const samples=[.37,.83,1.29,2.17,3.41,4.73,6.19];
 let compared=0;
 for(let i=0;i<samples.length;i++){
  const scope=Object.fromEntries(variables.map((v,j)=>[v,v==='k'?[-3,-1,0,1,2,4,7][i]:samples[(i+j)%samples.length]]));
  let expected;try{expected=numeric(target,scope);}catch{continue;}
  const actual=numeric(input,scope);compared++;
  if(!close(actual,expected))return false;
 }
 if(!compared)throw Error('Не удалось проверить выражение.');
 return true;
}
function pointList(text){
 return text.split('|').map(v=>{
  v=v.trim();if(v.startsWith('(')&&v.endsWith(')'))v=v.slice(1,-1);
  const coordinates=v.split(';').map(c=>c.trim());
  if(coordinates.length<2||coordinates.some(c=>!c))throw Error('Координаты: (x;y), несколько точек: (x;y) | (x;y).');
  return coordinates;
 });
}
function lineList(text){
 return text.split(';').map(line=>{
  const m=line.trim().match(/^([xy])\s*=\s*(.+)$/i);
  if(!m)throw Error('Прямые записывай как x=2; y=3x+1.');
  if(m[1].toLowerCase()==='x')return {axis:'x',v:numeric(m[2])};
  const c=numeric(m[2],{x:0}),k=numeric(m[2],{x:1})-c;
  for(const x of [-2,.43,2.71])if(!close(numeric(m[2],{x}),k*x+c))throw Error('Здесь нужны уравнения прямых y=kx+b.');
  return {axis:'y',k,c};
 });
}
function compareStructured(task,text){
 const target=task.answer;
 if(none(text)||none(target))return none(text)&&none(target);
 if(task.kind==='expression')return expressionEqual(text,target,task.variables);
 if(task.kind==='set')return unordered(text.split(';').map(v=>numeric(v)),target.split(';').map(v=>numeric(v)),close);
 if(task.kind==='points')return unordered(pointList(text),pointList(target),(a,b)=>a.length===b.length&&a.every((v,i)=>expressionEqual(v,b[i],task.variables)));
 return unordered(lineList(text),lineList(target),(a,b)=>a.axis===b.axis&&(a.axis==='x'?close(a.v,b.v):close(a.k,b.k)&&close(a.c,b.c)));
}
