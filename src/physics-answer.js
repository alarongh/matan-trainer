import {numeric,checkAnswer} from './answer.js';
const constants={g:9.8,r:8.31,k:1.38e-23,na:6.02e23,c:3e8};
const aliases=[
 ['кг','mass',1],['kg','mass',1],['г','mass',.001],['g','mass',.001],
 ['м','length',1],['m','length',1],['см','length',.01],['cm','length',.01],
 ['с','time',1],['s','time',1],['мин','time',60],['min','time',60],
 ['м/с','speed',1],['m/s','speed',1],['км/ч','speed',1/3.6],['km/h','speed',1/3.6],
 ['м/с²','acceleration',1],['м/с^2','acceleration',1],['m/s^2','acceleration',1],
 ['н','force',1],['n','force',1],['кн','force',1000],['kn','force',1000],
 ['н·м','torque',1],['n*m','torque',1],['па','pressure',1],['pa','pressure',1],['кпа','pressure',1000],['kpa','pressure',1000],['мпа','pressure',1e6],['mpa','pressure',1e6],
 ['дж','energy',1],['j','energy',1],['кдж','energy',1000],['kj','energy',1000],['мдж','energy',1e6],['mj','energy',1e6],
 ['к','temperature',1],['k','temperature',1],['м³','volume',1],['м^3','volume',1],['m^3','volume',1],['л','volume',.001],['l','volume',.001],
 ['кг/м³','density',1],['kg/m^3','density',1],['м⁻³','concentration',1],['м^-3','concentration',1],['m^-3','concentration',1],['см⁻³','concentration',1e6],['cm^-3','concentration',1e6],
 ['кг·м/с','momentum',1],['kg*m/s','momentum',1],['кг·м²','inertia',1],['kg*m^2','inertia',1],['кг·м²/с','angular-momentum',1],['kg*m^2/s','angular-momentum',1],
 ['рад/с','angular-speed',1],['rad/s','angular-speed',1],['рад/с²','angular-acceleration',1],['rad/s^2','angular-acceleration',1],
 ['об/мин','frequency-minute',1],['rpm','frequency-minute',1],
 ['°','angle-degrees',1],['град','angle-degrees',1],
 ['%','ratio',.01],['доля','ratio',1],['раз','ratio',1],
 ['моль','amount',1],['mol','amount',1],['атомов','count',1],['молекул','count',1],
 ['дж/к','entropy',1],['j/k','entropy',1],['дж/(кг·к)','specific-heat',1],['j/(kg*k)','specific-heat',1]
].sort((a,b)=>b[0].length-a[0].length);
const normalizedUnit=value=>String(value).toLowerCase().replace(/\s/g,'');
function quantity(text,unit){
 const trimmed=String(text).trim(),s=trimmed.toLowerCase().replace(/\s+/g,'');
 const expected=aliases.find(v=>v[0]===normalizedUnit(unit));
 for(const [suffix,dimension,factor] of aliases){
  // A bare g, k or m may also be a constant or expression variable.
  if(!s.endsWith(suffix)||s.length===suffix.length)continue;
  const prefix=s.slice(0,-suffix.length);
  if(!/[\d)²³]$/.test(prefix))continue;
  if(expected&&dimension!==expected[1])throw Error('Единица не подходит. Нужны '+unit+'.');
  if(!expected&&normalizedUnit(unit)!==suffix)throw Error('Введи число в указанных единицах: '+unit+'.');
  return numeric(prefix,constants)*factor/(expected?.[2]||1);
 }
 return numeric(trimmed,constants);
}
export function checkPhysicsAnswer(task,input){
 if(task.kind==='fields'){
  try{
   const values=JSON.parse(input),results=task.fields.map(f=>({label:f.label,...checkPhysicsAnswer(f,values[f.id]??'')}));
   const invalid=results.find(r=>!r.valid);if(invalid)return {valid:false,message:invalid.label+': '+invalid.message};
   return {valid:true,correct:results.every(r=>r.correct),incorrect:results.filter(r=>!r.correct).map(r=>r.label)};
  }catch{return {valid:false,message:'Заполни все поля ответа.'};}
 }
 if(task.kind!=='number')return checkAnswer(task,input);
 if(!String(input).trim())return {valid:false,message:'Сначала введи ответ.'};
 try{
  const v=quantity(input,task.unit),targets=[task.answer,...(task.acceptedAnswers||[])].map(value=>numeric(value,constants));
  return {valid:true,correct:targets.some(target=>Number.isFinite(v)&&Math.abs(v-target)<=(target===0?1e-12:Math.abs(target)*(task.tolerance??.005)))};
 }catch(e){return {valid:false,message:e.message};}
}
export function physicsInputHelp(task,input,help){
 input.placeholder=task.kind==='expression'?'Через '+task.variables.join(', '):'Ответ в '+task.unit;
 if(help)help.textContent='Единицы: '+task.unit+'. Дробь и десятичная запись равнозначны; допустимо округление до 0,5%. g=9,8; R=8,31; k=1,38·10⁻²³; N_A=6,02·10²³. Для КПД 0,25 и 25% равнозначны.';
}
