import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {numeric,checkAnswer} from '../src/answer.js';
import {complex,checkLinearAnswer} from '../src/linear-answer.js';

test('fractions, decimal points and decimal commas represent the same answer in every numeric input kind',()=>{
 const cases=[
  [{answer:'1/2'},['0.5','0,5','2/4','\\frac{1}{2}']],
  [{answer:'0,5'},['1/2','0.5']],
  [{answer:'-3/4'},['-0.75','-0,75']],
  [{kind:'expression',variables:['x'],answer:'x/2-3/4'},['0.5*x-0.75','0,5*x-0,75']],
  [{kind:'set',answer:'-1/2;3/4'},['0.75;-0.5','0,75;-0,5']],
  [{kind:'points',answer:'(1/2;-3/4)'},['(0.5;-0.75)','(0,5;-0,75)']],
  [{kind:'lines',answer:'x=1/2;y=x/4-3/4'},['y=0.25*x-0.75;x=0.5','y=0,25*x-0,75;x=0,5']],
  [{kind:'matrix',answer:'1/2 -3/4;5/4 1/8'},['0.5 -0.75;1.25 0.125','0,5 -0,75;1,25 0,125','[[0.5,-0.75],[1.25,0.125]]','[["0,5","-0,75"],["5/4","1/8"]]']],
  [{kind:'matrix',answer:'0.5 -0.75;1.25 0.125'},['1/2 -3/4;5/4 1/8']],
  [{kind:'matrix',answer:'1/2;3/4'},['0.5;0.75','0,5;0,75']],
  [{kind:'complex',answer:'1/2-3i/4'},['0.5-0.75i','0,5-0,75i']],
  [{kind:'complex-set',answer:'1/2+i/4;1/2-i/4'},['0.5-0.25i;0.5+0.25i','0,5-0,25i;0,5+0,25i']],
  [{kind:'vector',answer:'(1/2;-3/4;1/8)'},['(0.5;-0.75;0.125)','(0,5;-0,75;0,125)']],
  [{kind:'direction',answer:'(1/2;1/4;-3/4)'},['(0.5;0.25;-0.75)','(0,5;0,25;-0,75)']],
  [{kind:'equation',variables:['x','y','z'],answer:'x/2+y/4-3z/4=1/8'},['0.5x+0.25y-0.75z=0.125','0,5x+0,25y-0,75z=0,125']],
  [{kind:'line3',answer:'x=1/2+t;y=3/4+2t;z=1/8-t'},['x=0.5+t;y=0.75+2t;z=0.125-t','x=0,5+t;y=0,75+2t;z=0,125-t']],
  [{kind:'affine',answer:'(1/2+t;3/4+2t;1/8-t)'},['(0.5+t;0.75+2t;0.125-t)','(0,5+t;0,75+2t;0,125-t)']],
  [{kind:'system-point',matrix:[[2,0,0],[0,4,0],[0,0,8]],rhs:[1,3,1],answer:'(1/2;3/4;1/8)'},['(0.5;0.75;0.125)','(0,5;0,75;0,125)']],
 ];
 const linearKinds=new Set(['matrix','complex','complex-set','vector','direction','equation','line3','affine','system-point']);
 for(const [task,inputs] of cases){
  const check=linearKinds.has(task.kind)?checkLinearAnswer:checkAnswer;
  for(const input of inputs)assert.deepEqual(check(task,input),{valid:true,correct:true},`${task.kind||'number'}: ${input}`);
 }
 for(const check of [checkAnswer,checkLinearAnswer]){
  const fields=[{id:'a',label:'Число',answer:'1/2'},{id:'b',label:'Координаты',kind:'points',answer:'(-3/4;1/8)'}];
  assert.equal(check({kind:'fields',fields},JSON.stringify({a:'0,5',b:'(-0,75;0,125)'})).correct,true);
 }
});

test('decimal matrix entries cannot silently become two integers or accept a wrong value',()=>{
 for(const input of ['0,5','1/2'])assert.equal(checkLinearAnswer({kind:'matrix',answer:'0 5'},input).correct,false,input);
 for(const input of ['0,6','-0,5','5'])assert.equal(checkLinearAnswer({kind:'matrix',answer:'1/2'},input).correct,false,input);
 assert.equal(checkLinearAnswer({kind:'matrix',answer:'1/2 -3/4;5/4 1/8'},'0,5 -0,75;1,25 0,12').correct,false);
 for(const check of [checkAnswer,checkLinearAnswer])for(const input of ['0,6','-0,5','5','1/0'])assert.notEqual(check({answer:'1/2'},input).correct,true,input);
});

const decimal=(value,comma)=>{
 const text=Number.isInteger(value)&&Math.abs(value)<1e20?value.toFixed(1):String(value);
 return comma?text.replace('.',','):text;
};
function decimalAnswer(task,comma){
 const answer=task.answer;
 if(['choice','multi'].includes(task.kind)||/^(none|DNE)$/.test(answer))return null;
 if(task.kind==='fields'){
  const values=JSON.parse(answer);let changed=false;
  for(const field of task.fields){const value=decimalAnswer(field,comma);if(value!==null){values[field.id]=value;changed=true;}}
  return changed?JSON.stringify(values):null;
 }
 if(task.kind==='matrix')return answer.split(';').map(row=>row.trim().split(/\s+/).map(v=>decimal(numeric(v),comma)).join(' ')).join(';');
 if(task.kind==='complex'||task.kind==='complex-set')return answer.split(';').map(v=>{const [real,imaginary]=complex(v);return `${decimal(real,comma)}+(${decimal(imaginary,comma)})*i`;}).join(';');
 if(!['expression','set','points','lines','vector','direction','equation','line3','affine','system-point'].includes(task.kind)){
  const value=numeric(answer);return Number.isFinite(value)?decimal(value,comma):null;
 }
 // Replace only standalone literal fractions, preserving powers and expressions.
 const converted=answer.replace(/(?<![\w.)^])\d+\/\d+(?![\w.(^])/g,v=>`(${decimal(numeric(v),comma)})`);
 return converted!==answer?converted:null;
}
test('actual calculus and linear algebra banks accept equivalent decimal answers, including nested fields',t=>{
 for(const [file,check] of [['tasks',checkAnswer],['linear-tasks',checkLinearAnswer]]){
  const tasks=JSON.parse(readFileSync(new URL(`../data/${file}.json`,import.meta.url),'utf8'));let checked=0;
  for(const task of tasks)for(const comma of [false,true]){
   const input=decimalAnswer(task,comma);if(input===null)continue;
   const result=check(task,input);assert.equal(result.valid,true,`${task.id}: ${input}: ${result.message}`);assert.equal(result.correct,true,`${task.id}: ${input}`);checked++;
  }
  assert.ok(checked>50);t.diagnostic(`${file}: ${checked} decimal variants accepted`);
 }
});
