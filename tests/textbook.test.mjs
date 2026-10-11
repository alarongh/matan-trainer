import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {checkAnswer,numeric} from '../src/answer.js';
import {validateState,emptyState} from '../src/state.js';
const read=n=>JSON.parse(readFileSync(new URL('../data/'+n+'.json',import.meta.url),'utf8'));
const all=read('tasks'),tasks=all.filter(t=>t.id.startsWith('textbook-')),coverage=read('coverage');
const get=(section,n)=>tasks.find(t=>t.id==='textbook-'+String(section).padStart(2,'0')+'-'+n);

test('textbook coverage retains every practical exercise in all 26 sections',()=>{
 assert.equal(tasks.length,1017);assert.equal(coverage.textbook.cards,1017);
 assert.deepEqual(coverage.textbook.excluded,[]);
 for(const section of [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,23,24,25,26])for(let n=1;n<=30;n++)assert.ok(get(section,n),section+'/'+n);
 for(let n=1;n<=20;n++)for(const letter of ['a','b','c'])assert.ok(get(6,n+letter));
 for(let n=1;n<=27;n++)for(const letter of ['a','b'])assert.ok(get(19,n+letter));
 for(let n=28;n<=30;n++)assert.ok(get(19,n));
 for(const section of [20,21,22])for(let n=1;n<=30;n++)for(const kind of ['inflection','asymptotes','full'])assert.ok(get(section,n+'-'+kind));
 assert.equal(new Set(tasks.map(t=>t.sources[0].label)).size,837);
 assert.ok(tasks.every(t=>t.sources[0].file==='textbook'&&t.sources[0].page>=7&&t.sources[0].page<=57));
 const state={...emptyState(),origin:'textbook',selected:get(7,13).id};
 assert.equal(validateState(state,new Set(all.map(t=>t.id))).origin,'textbook');
});

test('epsilon thresholds accept larger valid N; Taylor and Hessian goldens are independent',()=>{
 const task=get(1,1);
 assert.equal(checkAnswer(task,'799').correct,false);
 assert.equal(checkAnswer(task,'800').correct,true);
 assert.equal(checkAnswer(task,'900').correct,true);
 assert.equal(checkAnswer(task,'800,5').valid,false);
 assert.equal(checkAnswer(get(1,8),'100').correct,false);
 assert.equal(checkAnswer(get(1,8),'101').correct,true);
 assert.equal(checkAnswer(get(18,1),'7/3-22h/9+88h^2/27-352h^3/81+1408h^4/243').correct,true);
 assert.equal(checkAnswer(get(18,1),'7/3-22h/9').correct,false);
 assert.equal(checkAnswer(get(26,1),JSON.stringify({point:'(2/7;-13/7;-1)',value:'-36/7',type:'1'})).correct,true);
 assert.equal(checkAnswer(get(26,25),JSON.stringify({point:'(0;0;0)',value:'0',type:'1'})).correct,true);
 assert.equal(checkAnswer(get(26,28),JSON.stringify({point:'(0;0;0)',value:'0',type:'2'})).correct,true);
});

test('written reviews never receive automatic correctness and include reference steps',()=>{
 const reviews=tasks.filter(t=>t.kind==='review');assert.equal(reviews.length,150);
 for(const task of reviews){assert.equal(checkAnswer(task,'готово').manual,true);assert.equal(checkAnswer(task,'готово').correct,undefined);assert.ok(task.checklist.length>=4);}
 const d=get(8,27);assert.match(d.stages.map(s=>JSON.stringify(s)).join(' '),/−1 и 0/);
 assert.match(get(20,'4-full').stages[1].blocks[0].tex,/1/);
 assert.match(get(22,'20-full').stages[1].blocks[0].tex,/-1/);
 for(const section of [20,21,22,23])for(let n=1;n<=30;n++){
  const t=get(section,section===23?n:n+'-full');assert.ok(t.plot.segments.length);
  assert.ok(t.plot.segments.flat().every(p=>p.length===2&&p.every(Number.isFinite)));
 }
});

test('visually rechecked graph coefficients retain the exact printed variants',()=>{
 assert.match(get(20,'12-full').prompt,/- 2 x\^\{3\}/);
 assert.match(get(20,'16-full').prompt,/6/);
 assert.match(get(20,'27-full').prompt,/- 2 x\^\{3\}/);
 assert.equal(checkAnswer(get(20,'12-asymptotes'),'x=-sqrt(3); x=sqrt(3); y=-2x+2').correct,true);
 assert.equal(checkAnswer(get(20,'16-asymptotes'),'x=-3; x=2; y=2x-3').correct,true);
 assert.equal(checkAnswer(get(20,'27-asymptotes'),'x=-3; x=-1; y=-2x+5').correct,true);
 assert.ok(!get(21,'23-full').stages[1].blocks[0].tex.includes('\\setminus'));
 assert.match(get(22,'7-full').stages[2].blocks[0].tex,/1\.763/);
 assert.doesNotMatch(get(22,'24-full').prompt,/2 \\ln/);
});

test('both actual retake limits and coefficient-sensitive variants have independent golden answers',()=>{
 for(const [section,n,input] of [[7,9,'e^-5'],[7,13,'sqrt(2/3)'],[6,'4a','e^(-1/3)'],[7,11,'e^(-2/9)'],[7,25,'e^-16'],[7,26,'1/sqrt(2)'],[7,29,'1/sqrt(5)'],[5,19,'-6ln(4)'],[4,18,'-2sqrt(6)/3'],[4,23,'-1/2'],[19,'28','-32/9']]){
  assert.equal(checkAnswer(get(section,n),input).correct,true,section+'/'+n);
 }
 assert.equal(checkAnswer(get(7,9),'e^-20').correct,false);
 assert.equal(checkAnswer(get(7,13),'sqrt(3/2)').correct,false);
 assert.equal(checkAnswer(get(6,'5a'),'не существует').correct,true);
 assert.equal(checkAnswer(get(6,'8c'),'нет').correct,true);
 assert.equal(checkAnswer(get(19,'3a'),'DNE').correct,true);
 assert.equal(checkAnswer(get(19,'3a'),'-infinity').correct,false);
 assert.equal(get(7,9).sources[0].page,21);
 assert.equal(get(7,13).sources[0].page,22);
});

test('new derivative notation and real cube roots accept independently written answers',()=>{
 assert.equal(numeric('cbrt(-8)'),-2);
 assert.equal(numeric('ctg(pi/4)'),1/Math.tan(Math.PI/4));
 assert.equal(checkAnswer(get(9,3),'-1/(x*(1+ln(1/x)^2))').correct,true);
 assert.equal(checkAnswer(get(9,29),'tan(x)^4*(1+tan(x)^2)^2').correct,true);
 assert.equal(checkAnswer(get(12,13),'(2/3)*t^(-1/6)').correct,true);
 assert.equal(checkAnswer(get(24,1),JSON.stringify({a:'3x^2+3/y',b:'3y^2-3x/y^2'})).correct,true);
 assert.equal(checkAnswer(get(25,29),JSON.stringify({a:'1-1/y^2',b:'1-1/y^2'})).correct,true);
 assert.equal(checkAnswer(get(25,29),JSON.stringify({a:'1+1/y^2',b:'1-1/y^2'})).correct,false);
});

test('graph adaptations and geometry retain independently derived answers and original ambiguities',()=>{
 assert.equal(checkAnswer(get(22,'1-inflection'),'(-0,5;2/e)').correct,true);
 assert.equal(checkAnswer(get(22,'7-asymptotes'),'y=1-x; x=0').correct,true);
 assert.equal(checkAnswer(get(21,'14-asymptotes'),'y=-x-2; y=x-2').correct,true);
 assert.equal(checkAnswer(get(17,6),JSON.stringify({height:'8'})).correct,true);
 assert.equal(checkAnswer(get(17,23),JSON.stringify({radius:'8/5',height:'4/sqrt(5)',volume:'256pi/(75sqrt(5))'})).correct,true);
 assert.equal(checkAnswer(get(17,24),JSON.stringify({height:'r*(23-sqrt(17))/16'})).correct,true);
 assert.equal(checkAnswer(get(17,30),JSON.stringify({size:'(3;6;4)'})).correct,true);
 for(const [section,n] of [[6,'19c'],[11,17],[14,8],[15,19]]){
  const t=get(section,n);assert.equal(t.kind,'choice');assert.equal(t.answer,'2');
  assert.ok(coverage.sourceIssues.some(issue=>issue.id===t.id));
 }
});
