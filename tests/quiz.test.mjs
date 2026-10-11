import test from 'node:test';
import assert from 'node:assert/strict';
import katex from 'katex';
import {formulaBanks,fullTex,tileTex,rightTex} from '../src/formula-bank.js';
import {numeric} from '../src/answer.js';
import {emptyQuiz,startWave,nextFormula,submitFormula,matchFormula,waveQueue,validateQuiz,loadQuiz,saveQuiz,quizKey} from '../src/quiz-core.js';
test('formula banks cover every section and render every fragment, template and revealed step',()=>{
 assert.equal(formulaBanks.matan.length,112);assert.equal(formulaBanks.linear.length,48);
 for(const [subject,cards] of Object.entries(formulaBanks)){
  assert.equal(new Set(cards.map(c=>c.id)).size,cards.length);
  for(let group=1;group<=10;group++)assert.ok(cards.some(c=>c.groups.includes(group)),subject+' №'+group);
  for(const card of cards){
   assert.ok(card.conditions&&card.tip&&card.explanation,card.id);
   assert.ok(card.parts.length&&card.wrong.length>=2,card.id);
   assert.ok(card.wrong.every(v=>!card.parts.includes(v)),card.id+' distractors');
   assert.deepEqual([...new Set([...card.layout.matchAll(/@(\d+)@/g)].map(v=>Number(v[1])))].sort(),card.parts.map((_,i)=>i),card.id+' slots');
   for(const order of card.orders){
    assert.deepEqual([...order].sort(),card.parts.map((_,i)=>i),card.id+' permutation');
    assert.deepEqual(matchFormula(card,order.map(i=>card.parts[i])),[],card.id+' valid construction');
   }
   for(const value of [...card.parts,...card.wrong])assert.doesNotThrow(()=>katex.renderToString(tileTex(value),{throwOnError:true,strict:'ignore'}),card.id+' piece');
   for(const step of card.steps||[])if(step[2])assert.doesNotThrow(()=>katex.renderToString(step[2],{throwOnError:true,strict:'ignore'}),card.id+' worked step');
   for(let mask=0;mask<2**card.parts.length;mask++)assert.doesNotThrow(()=>katex.renderToString(fullTex(card,card.parts.map((v,i)=>mask&(1<<i)?v:null)),{throwOnError:true,strict:'ignore'}),card.id+' partial');
   for(let i=0;i<card.parts.length;i++)for(const wrong of card.wrong){
    const selected=[...card.parts];selected[i]=wrong;assert.ok(matchFormula(card,selected).length,card.id+' wrong fragment');
    assert.doesNotThrow(()=>katex.renderToString(fullTex(card,selected),{throwOnError:true,strict:'ignore'}),card.id+' wrong preview');
   }
  }
 }
});
test('matan reverse and transformation waves preserve old history and match the chosen practice',()=>{
 const cards=formulaBanks.matan;
 assert.deepEqual(Object.fromEntries(['forward','reverse','transform'].map(type=>[type,cards.filter(c=>c.type===type).length])),{forward:66,reverse:20,transform:26});
 for(const practice of ['forward','reverse','transform']){
  const state=emptyQuiz();state.practice=practice;state.groups=[3,4,6];assert.ok(startWave(state,cards,()=>.37));
  assert.ok(state.queue.every(id=>{const card=cards.find(c=>c.id===id);return card.type===practice&&card.groups.some(g=>state.groups.includes(g));}));
  state.items['m-first-limit']={attempts:1,correct:1,wrong:0,clean:1,streak:1,lastAt:1};
  state.round.selected=[...cards.find(c=>c.id===state.round.id).parts];
  const restored=validateQuiz(JSON.parse(JSON.stringify(state)),cards);assert.deepEqual(restored,state);
  for(let i=0;i<state.queue.length*3;i++){nextFormula(state,cards,()=>.37);assert.equal(cards.find(c=>c.id===state.round.id).type,practice);}
  assert.equal(restored.items['m-first-limit'].clean,1,'old formula result retained');
 }
 const legacy=emptyQuiz();delete legacy.practice;startWave(legacy,cards.slice(0,58));assert.equal(validateQuiz(legacy,cards).practice,'all');
 for(const card of cards.filter(c=>c.type==='reverse'))assert.equal(fullTex(card),rightTex(card)+'\\;'+card.relation+'\\;'+card.left,'reverse layout '+card.id);
 const state=emptyQuiz();state.groups=[10];state.practice='reverse';assert.equal(startWave(state,cards),false,'empty selection cannot launch');
});
test('independent math values agree with logarithm and coefficient-sensitive construction cards',()=>{
 const cards=formulaBanks.matan,at=id=>cards.find(c=>c.id==='m-transform-'+id);
 const close=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-9,actual+' vs '+expected);
 const value=tex=>numeric(tex.replace(/\\ln(\d+)/g,'ln($1)'));
 // Evaluate the selected fragments independently of the authored explanations.
 close(numeric(rightTex(at('exp-to-root'))),Math.sqrt(2/3));
 close(value(rightTex(at('limit-exponent'))),(Math.log(2)-Math.log(3))/2);
 close(value(rightTex(at('cancel-small'))),(Math.log(7)-Math.log(2))/4);
 close(numeric(rightTex(at('square-ratio'))),25/4);
 close(numeric(rightTex(at('cos-power-limit'))),Math.exp(-36));
 const quartic=at('sine-double-limit');close((numeric(quartic.parts[1])/numeric(quartic.parts[2]))**(1/numeric(quartic.parts[0])),(7/2)**.25);
 for(const x of [-.31,.17,1.2]){
  close(numeric(rightTex(at('rationalize')),{x}),Math.sqrt(x+4)-2);
  close(numeric(rightTex(at('factor-cancel')),{x}),(x*x+4*x+3)/(x*x+x-6));
  close(numeric(rightTex(at('base-minus-one')),{x}),(1+2**x)/(1+3**x)-1);
 }
});
test('endless waves respect multiple selected sections, avoid adjacent repeats and prioritize mistakes',()=>{
 const cards=formulaBanks.matan,state=emptyQuiz();state.groups=[3,8];
 assert.ok(startWave(state,cards,()=>.37));
 const expected=cards.filter(c=>c.groups.some(g=>state.groups.includes(g))).map(c=>c.id);
 assert.deepEqual([...state.queue].sort(),[...expected].sort());
 const weak=expected[0];state.items[weak]={wrong:1,streak:0};
 const queue=waveQueue(cards,state,()=>.37);assert.equal(queue.filter(id=>id===weak).length,2);
 assert.ok(queue.every((id,i)=>i===0||id!==queue[i-1]));
 for(let i=0;i<expected.length*6;i++){const previous=state.round.id;assert.ok(nextFormula(state,cards,()=>.37));assert.ok(expected.includes(state.round.id));assert.notEqual(state.round.id,previous);}
 assert.ok(state.wave>5);
 const single=[cards[0]],one=emptyQuiz();assert.ok(startWave(one,single));for(let i=0;i<10;i++)assert.ok(nextFormula(one,single));
 state.groups=[];assert.equal(startWave(state,cards),false);
});
test('wrong answers reveal one step; hints and retries cannot count as independent recall',()=>{
 const cards=[formulaBanks.matan.find(c=>c.id==='m-quotient')],card=cards[0],state=emptyQuiz();startWave(state,cards);
 assert.equal(submitFormula(state,card).valid,false);assert.deepEqual(state.items,{});
 state.round.selected=[...card.parts];state.round.selected[2]=card.wrong[0];
 assert.equal(submitFormula(state,card,1).correct,false);assert.equal(state.round.step,1);assert.equal(state.items[card.id].wrong,1);
 state.round.selected=[...card.parts];assert.equal(submitFormula(state,card,2).correct,true);assert.equal(state.items[card.id].clean,0);
 assert.equal(submitFormula(state,card,3).already,true);assert.equal(state.items[card.id].attempts,2);
 nextFormula(state,cards);state.round.selected=[...card.parts];submitFormula(state,card,4);assert.equal(state.items[card.id].streak,1);
 nextFormula(state,cards);state.round.selected=[...card.parts];submitFormula(state,card,5);assert.equal(state.items[card.id].streak,2);
 nextFormula(state,cards);state.round.step=1;state.round.selected=[...card.parts];submitFormula(state,card,6);assert.equal(state.items[card.id].streak,0);assert.equal(state.items[card.id].clean,2);
 const product=formulaBanks.matan.find(c=>c.id==='m-product');assert.deepEqual(matchFormula(product,[...product.parts].reverse()),[]);
 for(const id of ['m-double-sine','m-tangent','m-asymptote','m-base-exp-derivative','l-parabola']){
  const commutative=Object.values(formulaBanks).flat().find(c=>c.id===id);
  assert.deepEqual(matchFormula(commutative,[...commutative.parts].reverse()),[],id);
 }
 const matrices=formulaBanks.linear.find(c=>c.id==='l-left-matrix');
 assert.notDeepEqual(matchFormula(matrices,[...matrices.parts].reverse()),[]);
 assert.notDeepEqual(matchFormula(card,[card.parts[1],card.parts[0],card.parts[2]]),[]);
});
test('separate quiz storage restores the exact round without modifying study histories',()=>{
 const values=new Map([['matan-trainer:v1','existing calculus history'],['linear-trainer:v1','existing linear history']]);
 const storage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};
 const state=emptyQuiz(),cards=formulaBanks.matan;startWave(state,cards);state.round.selected[0]=state.round.choices[0];
 assert.ok(saveQuiz(storage,'matan',state));assert.deepEqual(loadQuiz(storage,'matan',cards),state);
 assert.equal(loadQuiz(storage,'linear',formulaBanks.linear).round,null);assert.equal(values.get('matan-trainer:v1'),'existing calculus history');assert.equal(values.get('linear-trainer:v1'),'existing linear history');
 values.set(quizKey('matan'),'{broken');assert.equal(loadQuiz(storage,'matan',cards).round,null);
 assert.equal(saveQuiz({setItem:()=>{throw Error();}},'matan',state),false);
 const malicious={...state,groups:[-1,3,99],items:{unknown:{attempts:999}},round:{...state.round,selected:['\\href{bad}{bad}'],step:999,result:'correct'}};
 const valid=validateQuiz(malicious,cards);assert.deepEqual(valid.groups,[3]);assert.deepEqual(valid.items,{});assert.equal(valid.round.step,4);assert.equal(valid.round.result,null);assert.ok(valid.round.selected.every(v=>v===null));
});
