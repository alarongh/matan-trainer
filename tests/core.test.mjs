import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import katex from 'katex';
import {numeric,checkAnswer} from '../src/answer.js';
import {emptyState,recordAttempt,validateState,loadState,saveState,KEY} from '../src/state.js';
const tasks=JSON.parse(readFileSync(new URL('../data/tasks.json',import.meta.url),'utf8'));
const ids=new Set(tasks.map(t=>t.id));
test('safe arithmetic accepts equivalent mathematical notation',()=>{
 for(const [input,expected] of [['2/3',2/3],['0,5',.5],['3sqrt(3)',3*Math.sqrt(3)],['e^-3',Math.exp(-3)],['е^(-3)',Math.exp(-3)],['-2^2',-4],['2^-3',.125],['2^3^2',512],['e^(-3*pi/4)',Math.exp(-3*Math.PI/4)],['\\frac{1}{\\sqrt{4}}',.5],['2(3+1)',8],['sin(pi/2)',1],['бесконечность',Infinity],['-∞',-Infinity]])assert.ok(Object.is(numeric(input),expected)||Math.abs(numeric(input)-expected)<1e-13,input);
});
test('invalid code, undefined arithmetic and huge input are rejected',()=>{
 for(const input of ['alert(1)','globalThis.process','1;2','1/0','sqrt(-1)','2**3','2+','(2','0/0','x','2'.repeat(257)])assert.throws(()=>numeric(input),undefined,input);
});
test('answer comparison distinguishes small exponentials from zero and sign errors',()=>{
 assert.equal(checkAnswer({answer:'exp(-56)'},'0').correct,false);
 assert.equal(checkAnswer({answer:'exp(-36)'},'exp(36)').correct,false);
 assert.equal(checkAnswer({answer:'exp(-3)'},'-3').correct,false);
 assert.equal(checkAnswer({answer:'0'},'0').correct,true);
 assert.equal(checkAnswer({answer:'sqrt(2)'},'1.414214').correct,true);
 assert.equal(checkAnswer({answer:'1/2'},'').valid,false);
});
test('inverse trigonometric notation is conventional in every displayed task',()=>{
 for(const task of tasks)for(const tex of [task.prompt,...task.stages.flatMap(s=>s.blocks.map(b=>b.tex))])assert.doesNotMatch(tex,/\\operatorname\{(?:atan|acot|asin|acos)\}/,task.id);
 assert.equal(numeric('arctan(1)'),Math.PI/4);
 assert.equal(numeric('arccot(1)'),Math.PI/4);
 assert.equal(numeric('arcsin(1)'),Math.PI/2);
 assert.equal(numeric('arccos(1)'),0);
 assert.equal(numeric('3×4÷2'),6);
});
test('complete bank contains all source examples with valid math, sources and accepted answers',()=>{
 assert.equal(tasks.length,426);assert.equal(ids.size,426);
 assert.equal(tasks.filter(t=>t.origin==='source').length,378);
 for(const [prefix,count,start=1] of [['parity',30],['sequence',40],['monotonic',29],['sequence-theory',10],['function-theory',10],['function-limit',40],['advanced-limit',40],['derivative',39],['asymptote',40],['tangent',20],['tangent',10,31],['inflection',10,21],['practical',35],['oral',28]])for(let n=start;n<start+count;n++)assert.ok(ids.has(`${prefix}-${String(n).padStart(2,'0')}`),`${prefix}-${n}`);
 for(const task of tasks){
  assert.equal(checkAnswer(task,task.answer).correct,true,task.id+' answer');
  let wrong=task.answer==='0'?'1':'0';
  if(task.kind==='choice')wrong=(task.options?.map(o=>o.value)||['1','2','3']).find(v=>v!==task.answer);
  if(task.kind==='multi')wrong=task.answer==='1'?'2':'1';
  if(task.kind==='fields'){const map=JSON.parse(task.answer);const f=task.fields[0];map[f.id]=f.answer==='0'?'1':f.kind==='lines'?'x=98765':f.kind==='points'?'(98765;98765)':'0';wrong=JSON.stringify(map);}
  assert.notEqual(checkAnswer(task,wrong).correct,true,task.id+' wrong answer');
  assert.ok(task.stages.length>=4,task.id+' stages');
  for(const tex of [task.prompt,...task.stages.flatMap(s=>s.blocks.map(b=>b.tex).filter(Boolean))])assert.doesNotThrow(()=>katex.renderToString(tex,{throwOnError:true,strict:'ignore',trust:false}),task.id+' '+tex);
  for(const src of task.sources)assert.ok(existsSync(new URL(`../sources/${src.file}.pdf`,import.meta.url)),task.id+' PDF');
 }
 const verified=JSON.parse(readFileSync(new URL('../data/verification.json',import.meta.url),'utf8'));
 assert.ok(verified.length>=64);assert.ok(verified.every(v=>v.passed));
});
test('history preserves independent versus assisted attempts across export and reload',()=>{
 const state=emptyState();recordAttempt(state,'sequence-01','0',false,1);
 assert.equal(state.items['sequence-01'].step,1);
 recordAttempt(state,'sequence-01','1/2',true,2);
 assert.equal(state.items['sequence-01'].status,'assisted');
 state.items['sequence-01'].step=0;recordAttempt(state,'sequence-01','1/2',true,3);
 assert.equal(state.items['sequence-01'].status,'solved');
 state.theme='night';state.selected='sequence-01';
 let stored;const storage={setItem:(k,v)=>{assert.equal(k,KEY);stored=v;},getItem:()=>stored};
 assert.ok(saveState(storage,state));assert.deepEqual(loadState(storage,ids),state);
 assert.deepEqual(validateState(JSON.parse(stored),ids),state);
 assert.equal(loadState({getItem:()=>'{broken'},ids).theme,'sage');
 assert.equal(saveState({setItem:()=>{throw Error();}},state),false);
 const incoming={...state,group:'10',items:{unknown:{status:'solved'},'sequence-02':{status:'solved',step:999,draft:'x'.repeat(9999),attempts:[]}}};
 const safe=validateState(incoming,ids);assert.equal(safe.items.unknown,undefined);assert.equal(safe.items['sequence-02'].step,20);assert.equal(safe.items['sequence-02'].draft.length,2048);assert.equal(safe.group,'10');
});
test('structured results compare coordinates, lines, sets and parameter expressions',()=>{
 for(const [task,input] of [[{kind:'points',answer:'(2;1/2)|(-2;-1/2)'},'(-2;-0,5) | (sqrt(4);0.5)'],[{kind:'lines',answer:'x=2; y=3x+1'},'y=1+3*x; x=4/2'],[{kind:'set',answer:'-2;5'},'5;-2'],[{kind:'expression',variables:['l'],answer:'l/4'},'0.25*l']])assert.equal(checkAnswer(task,input).correct,true);
 assert.equal(checkAnswer({kind:'expression',variables:['a'],answer:'a/sqrt(2)'},'a/2').correct,false);
 assert.equal(checkAnswer({kind:'lines',answer:'y=x'},'y=x^2').valid,false);
 assert.equal(checkAnswer({kind:'points',answer:'none'},'нет').correct,true);
 assert.equal(checkAnswer({kind:'multi',options:[{value:'1'},{value:'2'},{value:'3'}],answer:'1;3'},'3;1').correct,true);
});
