export const quizKey=subject=>'formula-quiz:'+subject+':v1';
export const emptyQuiz=()=>({version:1,groups:Array.from({length:10},(_,i)=>i+1),autoAdvance:true,wave:0,queue:[],cursor:0,round:null,items:{}});
export function shuffled(values,random=Math.random){
 const result=[...values];for(let i=result.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[result[i],result[j]]=[result[j],result[i]];}return result;
}
export function matchFormula(card,selected){
 const variants=card.orders.map(order=>order.map(i=>card.parts[i]));
 const wrong=variants.map(parts=>parts.flatMap((part,i)=>part===selected[i]?[]:[i]));
 return wrong.reduce((best,v)=>v.length<best.length?v:best,wrong[0]);
}
export function waveQueue(cards,state,random=Math.random,previous=null){
 const available=cards.filter(card=>card.groups.some(g=>state.groups.includes(g)));
 const pool=shuffled(available.flatMap(card=>state.items[card.id]?.wrong>0&&state.items[card.id]?.streak<2&&available.length>1?[card.id,card.id]:[card.id]),random);
 const queue=[];let last=previous;
 while(pool.length){let index=pool.findIndex(id=>id!==last);if(index<0)index=0;last=pool.splice(index,1)[0];queue.push(last);}return queue;
}
function makeRound(card,random){
 return {id:card.id,choices:shuffled([...new Set([...card.parts,...card.wrong])],random),selected:card.parts.map(()=>null),active:0,step:0,hadError:false,result:null};
}
export function startWave(state,cards,random=Math.random){
 const queue=waveQueue(cards,state,random);if(!queue.length)return false;
 state.wave=1;state.queue=queue;state.cursor=0;state.round=makeRound(cards.find(c=>c.id===queue[0]),random);return true;
}
export function nextFormula(state,cards,random=Math.random){
 const previous=state.round?.id;
 if(state.cursor+1<state.queue.length)state.cursor++;
 else{state.queue=waveQueue(cards,state,random,previous);state.cursor=0;state.wave++;}
 if(!state.queue.length){state.round=null;return false;}
 state.round=makeRound(cards.find(c=>c.id===state.queue[state.cursor]),random);return true;
}
export function submitFormula(state,card,at=Date.now()){
 const round=state.round;if(!round||round.id!==card.id||round.selected.some(v=>v===null))return {valid:false};
 if(round.result==='correct')return {valid:true,correct:true,already:true};
 const wrong=matchFormula(card,round.selected),correct=wrong.length===0;
 const item=state.items[card.id]??={attempts:0,correct:0,wrong:0,clean:0,streak:0,lastAt:0};
 item.attempts++;item.lastAt=at;
 if(correct){item.correct++;const clean=round.step===0&&!round.hadError;item.clean+=Number(clean);item.streak=clean?item.streak+1:0;round.result='correct';}
 else{item.wrong++;item.streak=0;round.hadError=true;round.result='wrong';round.step=Math.max(1,round.step);}
 return {valid:true,correct,wrong,assisted:round.step>0||round.hadError};
}
export function validateQuiz(raw,cards){
 const state=emptyQuiz(),byId=new Map(cards.map(c=>[c.id,c]));
 if(!raw||raw.version!==1)return state;
 if(Array.isArray(raw.groups))state.groups=[...new Set(raw.groups.filter(g=>Number.isInteger(g)&&g>=1&&g<=10))];
 state.autoAdvance=raw.autoAdvance!==false;
 const count=v=>Number.isSafeInteger(v)&&v>=0?Math.min(v,1_000_000):0;
 if(raw.items&&typeof raw.items==='object')for(const [id,v] of Object.entries(raw.items)){
  if(!byId.has(id)||!v||typeof v!=='object')continue;
  state.items[id]=Object.fromEntries(['attempts','correct','wrong','clean','streak','lastAt'].map(k=>[k,count(v[k])]));
  state.items[id].lastAt=Number.isFinite(v.lastAt)&&v.lastAt>=0?v.lastAt:0;
 }
 if(!Array.isArray(raw.queue)||raw.queue.length>cards.length*2)return state;
 state.queue=raw.queue.filter(id=>byId.has(id));
 state.wave=count(raw.wave);state.cursor=Math.min(count(raw.cursor),Math.max(0,state.queue.length-1));
 const card=byId.get(state.queue[state.cursor]);
 if(card){
  state.round=makeRound(card,Math.random);
  const old=raw.round,known=new Set([...card.parts,...card.wrong]);
  if(old?.id===card.id){
   if(Array.isArray(old.choices)&&old.choices.length===known.size&&new Set(old.choices).size===known.size&&old.choices.every(v=>known.has(v)))state.round.choices=old.choices;
   if(Array.isArray(old.selected))state.round.selected=card.parts.map((_,i)=>known.has(old.selected[i])?old.selected[i]:null);
   state.round.active=Math.min(count(old.active),card.parts.length-1);state.round.step=Math.min(4,count(old.step));state.round.hadError=old.hadError===true;
   if(old.result==='correct'&&matchFormula(card,state.round.selected).length===0)state.round.result='correct';
   else if(old.result==='wrong'){state.round.result='wrong';state.round.hadError=true;state.round.step=Math.max(1,state.round.step);}
  }
 }
 return state;
}
export function loadQuiz(storage,subject,cards){try{return validateQuiz(JSON.parse(storage.getItem(quizKey(subject))),cards);}catch{return emptyQuiz();}}
export function saveQuiz(storage,subject,state){try{storage.setItem(quizKey(subject),JSON.stringify(state));return true;}catch{return false;}}
