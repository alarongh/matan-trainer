// A small arithmetic parser. No eval, Function, assignment or property access.
export function normalize(input) {
 let s=String(input).trim().toLowerCase().replace(/[её]/g,'e').replace(/[−–—]/g,'-').replace(/π/g,'pi').replace(/²/g,'^2').replace(/³/g,'^3');
 s=s.replace(/\\(?:left|right)|\$/g,'').replace(/\\(?:cdot|times)/g,'*').replace(/\\pi/g,'pi').replace(/\\infty/g,'infinity').replace(/\\,/g,'');
 for(let i=0;i<10;i++){
  const next=s.replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g,'(($1)/($2))').replace(/\\sqrt\{([^{}]*)\}/g,'sqrt($1)');
  if(next===s) break; s=next;
 }
 return s.replace(/[{}]/g,c=>c==='{'?'(':')').replace(/(\d),(?=\d)/g,'$1.').replace(/\s+/g,'');
}
export function numeric(input) {
 const s=normalize(input);
 if(!s||s.length>256) throw new Error('Введите число или выражение.');
 if(['infinity','+infinity','inf','+inf','∞','+∞','бeсконeчность','+бeсконeчность'].includes(s)) return Infinity;
 if(['-infinity','-inf','-∞','-бeсконeчность'].includes(s)) return -Infinity;
 const tokens=s.match(/(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?|[a-z]+|[()+\-*/^]/g)||[];
 if(tokens.join('')!==s||tokens.length>128) throw new Error('Не удалось прочитать выражение. Пример: e^(-3), 2/3, sqrt(2).');
 let i=0;
 const peek=()=>tokens[i]; const take=()=>tokens[i++];
 const functions={sqrt:Math.sqrt,exp:Math.exp,ln:Math.log,log:Math.log,abs:Math.abs,sin:Math.sin,cos:Math.cos,tan:Math.tan,arctan:Math.atan,arccot:x=>Math.PI/2-Math.atan(x)};
 function atom(){
  const t=take();
  if(t==='('){const n=sum();if(take()!==')')throw new Error('Проверьте скобки.');return n;}
  if(t==='e') return Math.E;if(t==='pi')return Math.PI;
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
  return ['1','2','3'].includes(v)?{valid:true,correct:v===task.answer}:{valid:false,message:'Выберите один из трёх вариантов.'};
 }
 if(task.answer==='DNE')return {valid:true,correct:/^(не существует|нет|dne|не существует предела)$/i.test(text)};
 try{
  const v=numeric(text),target=numeric(task.answer);
  return {valid:true,correct:!Number.isFinite(target)?v===target:Number.isFinite(v)&&Math.abs(v-target)<= (target===0?1e-10:Math.abs(target)*1e-6)};
 }catch(e){return {valid:false,message:e.message};}
}
