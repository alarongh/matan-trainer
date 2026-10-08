import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import katex from 'katex';
import {checkLinearAnswer as check,complex} from '../src/linear-answer.js';
const read=name=>JSON.parse(readFileSync(new URL('../data/'+name+'.json',import.meta.url),'utf8'));
const tasks=read('linear-tasks'),coverage=read('linear-coverage'),ids=new Set(tasks.map(t=>t.id));
test('calculus content, coverage and verification are preserved exactly',()=>{
 for(const [name,hash] of Object.entries({tasks:'32efb326e778d5352931bad9cf59cada93967793227eea0a4f76049c5a9b48fe',coverage:'69cf0968a79ec0bc80d584ddfd46c07fc393713abf4e9d00033255d4767bf880',verification:'8c94d18afcc06b0bd1810fb379a60a00d566be8bd8595d7c6b5d457ed7edfed5'}))assert.equal(createHash('sha256').update(JSON.stringify(read(name))).digest('hex'),hash,name);
});
test('linear bank covers all source examples, tickets, demo variants and official theoretical topics',()=>{
 assert.equal(tasks.length,121);assert.equal(ids.size,121);assert.equal(coverage.source,91);assert.equal(coverage.extra,30);
 for(let n=1;n<=63;n++)assert.ok(ids.has(`la-example-${String(n).padStart(2,'0')}`));
 for(let n=1;n<=30;n++)assert.ok(ids.has(`la-oral-${String(n).padStart(2,'0')}`));
 for(const ticket of [1,2])for(let n=1;n<=10;n++)assert.ok(ids.has(`la-ticket-${ticket}-${n}`));
 for(const [group,count] of Object.entries({1:8,2:4,3:8,4:10,5:7,6:1,7:5,8:5,9:4,10:4}))for(let v=1;v<=count;v++)assert.ok(ids.has(coverage.demoVariants[`${group}.${v}`]),`${group}.${v}`);
 assert.equal(Object.keys(coverage.demoVariants).length,56);
 for(const task of tasks){
  assert.equal(check(task,task.answer).correct,true,task.id+' canonical answer');
  assert.ok(task.stages.length>=4,task.id+' staged solution');
  let wrong=task.answer==='0'?'12345':'0';
  if(task.kind==='choice')wrong=task.options.find(v=>v.value!==task.answer).value;
  if(task.kind==='multi')wrong=task.answer==='1'?'2':'1';
  if(task.kind==='fields'){
   const map=JSON.parse(task.answer),f=task.fields[0];map[f.id]=f.kind==='equation'?'x=98765':f.kind==='matrix'?'98765 0;0 0':f.answer==='0'?'98765':'0';wrong=JSON.stringify(map);
  }
  assert.notEqual(check(task,wrong).correct,true,task.id+' wrong answer');
  for(const tex of [task.prompt,...task.stages.flatMap(s=>s.blocks.map(b=>b.tex))]){assert.doesNotThrow(()=>katex.renderToString(tex,{throwOnError:true,strict:'ignore',trust:false}),task.id+' '+tex);assert.doesNotMatch(tex,/[\t\x00]/,task.id+' control characters');}
  for(const src of task.sources){assert.ok(existsSync(new URL('../sources/'+src.file+'.pdf',import.meta.url)));assert.ok(src.page>=1);}
 }
 assert.ok(read('linear-verification').length>=100);assert.ok(read('linear-verification').every(v=>v.passed));
 assert.equal(coverage.sourceIssues.length,7);
});
test('complex arithmetic, roots and trig notation accept equivalent forms safely',()=>{
 for(const [input,expected] of [['1/(1+i)',[.5,-.5]],['i^3',[0,-1]],['sqrt(-4)',[0,2]],['2*(cos(pi/2)+i*sin(pi/2))',[0,2]]])assert.ok(complex(input).every((v,i)=>Math.abs(v-expected[i])<1e-10),input);
 for(const input of ['alert(1)','globalThis.process','2**3','1/0','()','i'.repeat(300),'sin(i)'])assert.throws(()=>complex(input),undefined,input);
 assert.equal(check({kind:'complex',answer:'-8-6i'},'-2*(4+3i)').correct,true);
 assert.equal(check({kind:'complex-set',answer:'-2+3i;-2-3i'},'-2-3i;-2+3i').correct,true);
 assert.equal(check({kind:'complex-set',answer:'-2+3i;-2-3i'},'-2+3i;-2+3i').correct,false);
 assert.equal(check({kind:'complex',answer:'-8-6i'},'-8+6i').correct,false);
});
test('matrices compare dimensions and entries; equations accept nonzero proportional forms',()=>{
 assert.equal(check({kind:'matrix',answer:'1 2;3 4'},'[[1,2],[3,4]]').correct,true);
 assert.equal(check({kind:'matrix',answer:'1/2 2;3 4'},'.5 2\n3 4').correct,true);
 assert.equal(check({kind:'matrix',answer:'1 2;3 4'},'1 3;2 4').correct,false);
 assert.equal(check({kind:'matrix',answer:'1 2;3 4'},'1 2 3 4').correct,false);
 const plane={kind:'equation',variables:['x','y','z'],answer:'2x-y+4z+3=0'};
 for(const input of ['4x-2y+8z=-6','-2x+y-4z=3','2e-9*x-1e-9*y+4e-9*z+3e-9=0'])assert.equal(check(plane,input).correct,true,input);
 for(const input of ['2x-y+4z-3=0','0=0','1e-9*x=1e-9','sin(x)+y=0'])assert.notEqual(check(plane,input).correct,true,input);
 assert.equal(check({kind:'equation',variables:['x','y'],answer:'(x+1)^2/16-(y-2)^2/9=1'},'9x^2-16y^2+18x+64y-199=0').correct,true);
});
test('3D lines and general solutions accept equivalent parameterizations and reject a wrong point',()=>{
 const line={kind:'line3',answer:'x=-1+6t;y=2-4t;z=3-2t'};
 for(const input of ['(x+1)/3=(y-2)/(-2)=(z-3)/(-1)','x=5+3t;y=-2-2t;z=1-t','(-1+6t;2-4t;3-2t)'])assert.equal(check(line,input).correct,true,input);
 assert.equal(check(line,'x=6+3t;y=-2-2t;z=1-t').correct,false);
 const gauss=tasks.find(t=>t.id==='la-example-46');const solution=gauss.fields.find(f=>f.id==='general');
 assert.equal(check(solution,'(-3-28t;2-8t;1+2t)').correct,true);
 assert.equal(check(solution,'(11-14t;6-4t;2t)').correct,false);
 const particular=gauss.fields.find(f=>f.id==='particular');assert.equal(check(particular,'(-3;2;1)').correct,true);assert.equal(check(particular,'(11;6;1)').correct,false);
});
test('independent golden values retain source distinctions and correct printed mistakes',()=>{
 const answer=id=>tasks.find(t=>t.id===id).answer;
 assert.equal(answer('la-example-03'),'0 16; -14 -3');
 assert.notEqual(answer('la-example-03'),answer('la-demo-1-3'));
 assert.equal(answer('la-example-19'),'(-4;4;-2)');assert.equal(answer('la-demo-3-1'),'(-24/7;8/7;-2/7)');
 assert.equal(answer('la-example-33'),'-8 - 6*i');
 assert.equal(JSON.parse(answer('la-example-50')).complex,'3/34 - 5*i/34');
 assert.equal(answer('la-ticket-1-3'),'none');
 assert.equal(JSON.parse(answer('la-ticket-1-6')).general,'(t + 19/5;t;2/5)');
 const particular=tasks.find(t=>t.id==='la-ticket-1-6').fields.find(f=>f.id==='particular');
 assert.equal(check(particular,'(0;-19/5;2/5)').correct,true);
 assert.equal(check(particular,'(0;-3.75;0.4)').correct,false);
 assert.equal(JSON.parse(answer('la-example-55'))['3'],'3');
});
