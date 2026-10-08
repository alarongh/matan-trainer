export const KEY='matan-trainer:v1';
export const emptyState=()=>({version:1,theme:'sage',selected:null,group:'all',origin:'all',mode:'all',autoAdvance:true,items:{}});
export function validateState(raw,ids){
 if(!raw||raw.version!==1||typeof raw.items!=='object'||Array.isArray(raw.items))throw new Error('Это не файл прогресса тренажёра.');
 const s=emptyState();
 s.theme=['sage','paper','lavender','night'].includes(raw.theme)?raw.theme:'sage';
 s.group=['all','1','2','3'].includes(raw.group)?raw.group:'all';
 s.origin=['all','source','extra'].includes(raw.origin)?raw.origin:'all';
 s.mode=['all','new','review','solved'].includes(raw.mode)?raw.mode:'all';
 s.autoAdvance=raw.autoAdvance!==false;
 s.selected=ids.has(raw.selected)?raw.selected:null;
 for(const [id,item] of Object.entries(raw.items)){
  if(!ids.has(id)||!item||typeof item!=='object')continue;
  const attempts=Array.isArray(item.attempts)?item.attempts.slice(-200).filter(a=>typeof a.answer==='string'&&typeof a.correct==='boolean'&&Number.isFinite(a.at)).map(a=>({answer:a.answer.slice(0,256),correct:a.correct,at:a.at})):[];
  s.items[id]={attempts,status:['new','learning','solved','assisted'].includes(item.status)?item.status:'new',step:Number.isInteger(item.step)?Math.max(0,Math.min(20,item.step)):0,draft:typeof item.draft==='string'?item.draft.slice(0,256):''};
 }
 return s;
}
export function loadState(storage,ids){try{const r=storage.getItem(KEY);return r?validateState(JSON.parse(r),ids):emptyState();}catch{return emptyState();}}
export function itemState(s,id){return s.items[id]??={attempts:[],status:'new',step:0,draft:''};}
export function saveState(storage,s){try{storage.setItem(KEY,JSON.stringify(s));return true;}catch{return false;}}
export function recordAttempt(s,id,answer,correct,at=Date.now()){
 const item=itemState(s,id);item.attempts.push({answer,correct,at});item.attempts=item.attempts.slice(-200);
 item.status=correct?(item.step>0?'assisted':'solved'):'learning';
 if(!correct)item.step=Math.max(1,item.step);
 return item;
}
