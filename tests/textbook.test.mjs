import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {checkAnswer,numeric} from '../src/answer.js';
import {validateState,emptyState} from '../src/state.js';
const read=n=>JSON.parse(readFileSync(new URL('../data/'+n+'.json',import.meta.url),'utf8'));
const all=read('tasks'),tasks=all.filter(t=>t.id.startsWith('textbook-')),coverage=read('coverage');
const get=(section,n)=>tasks.find(t=>t.id==='textbook-'+String(section).padStart(2,'0')+'-'+n);

test('textbook coverage retains every variant in the chosen ticket-related sections',()=>{
 assert.equal(tasks.length,747);assert.equal(coverage.textbook.cards,747);
 for(const section of [2,4,5,7,9,10,11,12,13,14,15,16,17,24,25])for(let n=1;n<=30;n++)assert.ok(get(section,n),section+'/'+n);
 for(let n=1;n<=20;n++)for(const letter of ['a','b','c'])assert.ok(get(6,n+letter));
 for(let n=1;n<=27;n++)for(const letter of ['a','b'])assert.ok(get(19,n+letter));
 for(let n=28;n<=30;n++)assert.ok(get(19,n));
 for(const section of [20,21,22])for(let n=1;n<=30;n++)for(const kind of ['inflection','asymptotes'])assert.ok(get(section,n+'-'+kind));
 assert.equal(new Set(tasks.map(t=>t.sources[0].label)).size,657);
 assert.ok(tasks.every(t=>t.sources[0].file==='textbook'&&t.sources[0].page>=8&&t.sources[0].page<=55));
 const state={...emptyState(),origin:'textbook',selected:get(7,13).id};
 assert.equal(validateState(state,new Set(all.map(t=>t.id))).origin,'textbook');
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
