import test from 'node:test';
import assert from 'node:assert/strict';
import katex from 'katex';
import {formulaBanks,fullTex,tileTex} from '../src/formula-bank.js';
import {emptyQuiz,startWave,nextFormula,submitFormula,matchFormula,waveQueue,validateQuiz,loadQuiz,saveQuiz,quizKey} from '../src/quiz-core.js';
test('both formula banks cover every ticket section and render every fragment, template and revealed step',()=>{
 assert.equal(formulaBanks.matan.length,58);assert.equal(formulaBanks.linear.length,48);
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
   for(const value of [...card.parts,...card.wrong])assert.doesNotThrow(()=>katex.renderToString(tileTex(value),{throwOnError:true}),card.id+' piece');
   for(let mask=0;mask<2**card.parts.length;mask++)assert.doesNotThrow(()=>katex.renderToString(fullTex(card,card.parts.map((v,i)=>mask&(1<<i)?v:null)),{throwOnError:true}),card.id+' partial');
   for(let i=0;i<card.parts.length;i++)for(const wrong of card.wrong){
    const selected=[...card.parts];selected[i]=wrong;assert.ok(matchFormula(card,selected).length,card.id+' wrong fragment');
    assert.doesNotThrow(()=>katex.renderToString(fullTex(card,selected),{throwOnError:true}),card.id+' wrong preview');
   }
  }
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
 for(let i=0;i<400;i++){const previous=state.round.id;assert.ok(nextFormula(state,cards,()=>.37));assert.ok(expected.includes(state.round.id));assert.notEqual(state.round.id,previous);}
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
