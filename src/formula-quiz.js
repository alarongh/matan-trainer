import katex from './vendor/katex/katex.mjs';
import {formulaBanks,tileTex,fullTex} from './formula-bank.js';
import {loadQuiz,saveQuiz,startWave,nextFormula,submitFormula,matchFormula} from './quiz-core.js';
const el=(tag,cls,text)=>{const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node;};
const tex=(node,value,display=false)=>katex.render(value,node,{displayMode:display,throwOnError:false,strict:'ignore',trust:false});
const button=(label,cls='secondary-button')=>{const b=el('button',cls,label);b.type='button';return b;};
export function mountFormulaQuiz({subject,names,storage,cancelTaskAdvance}){
 const cards=formulaBanks[subject],state=loadQuiz(storage,subject,cards),root=document.getElementById('formula-quiz');
 let timer,visible=false,renderedRound=null;
 const heading=el('div','quiz-heading'),intro=el('div');
 intro.append(el('div','eyebrow','ФОРМУЛЫ · '+(subject==='linear'?'ЛИНАЛ':'МАТАН')),el('h2','','Собери и запомни'),el('p','','Выбирай фрагменты правой части. Ошибка откроет разбор по одному шагу.'));
 heading.append(intro,el('span','quiz-infinite','∞ Бесконечные волны'));root.append(heading);
 const topics=el('details','quiz-topics');topics.open=!state.round;
 const summary=el('summary','','Выбрать номера билета'),topicsList=el('div','quiz-topic-list');
 const all=button('Все номера','text-button'),none=button('Снять выбор','text-button'),selectionTools=el('div','quiz-selection-tools');selectionTools.append(all,none);
 const checkboxes=[];
 for(const [number,title] of Object.entries(names)){
  const label=el('label','quiz-topic'),input=el('input');input.type='checkbox';input.value=number;input.checked=state.groups.includes(Number(number));
  label.append(input,el('span','','№'+number+' · '+title));topicsList.append(label);checkboxes.push(input);
 }
 const chosenGroups=()=>checkboxes.filter(c=>c.checked).map(c=>Number(c.value));
 const poolSize=()=>cards.filter(c=>c.groups.some(g=>chosenGroups().includes(g))).length;
 const poolInfo=el('p','input-help'),launch=button('Запустить волну','primary-button');launch.id='quiz-start';
 const configBottom=el('div','quiz-config-bottom');configBottom.append(poolInfo,launch);topics.append(summary,selectionTools,topicsList,configBottom);root.append(topics);
 function config(){poolInfo.textContent=poolSize()+' формул в выбранных номерах. Формулы с ошибками будут чаще возвращаться.';launch.disabled=poolSize()===0;summary.textContent='Номера билета · '+(chosenGroups().length===10?'все':chosenGroups().map(g=>'№'+g).join(', ')||'не выбраны');}
 checkboxes.forEach(c=>c.onchange=config);all.onclick=()=>{checkboxes.forEach(c=>c.checked=true);config();};none.onclick=()=>{checkboxes.forEach(c=>c.checked=false);config();};config();
 const stats=el('div','quiz-stats');stats.setAttribute('aria-label','Прогресс викторины');root.append(stats);
 const autoLabel=el('label','quiz-auto'),auto=el('input');auto.type='checkbox';auto.id='quiz-auto-next';auto.checked=state.autoAdvance;
 autoLabel.append(auto,document.createTextNode('Следующая формула после верного ответа'));root.append(autoLabel);
 const welcome=el('div','quiz-welcome');welcome.append(el('span','','✧'),el('h3','','Короткая практика, сколько захочешь'),el('p','','Выбери один или несколько номеров и запусти волну. Она повторяется без конца; можно остановиться и продолжить позже.'));root.append(welcome);
 const cardBox=el('article','quiz-card');cardBox.id='quiz-card';root.append(cardBox);
 const topline=el('div','task-topline'),badge=el('span','badge'),position=el('span','task-position');topline.append(badge,position);
 const title=el('h3');title.id='quiz-title';const conditions=el('p','quiz-conditions');conditions.id='quiz-conditions';
 const preview=el('div','quiz-preview math');preview.id='quiz-preview';const previewFrame=el('div','problem-frame quiz-problem-frame');previewFrame.append(preview);
 const instruction=el('p','quiz-instruction','1. Выбери место для фрагмента. 2. Нажми на подходящий кусочек ниже.');
 const slots=el('div','quiz-slots');slots.id='quiz-slots';
 const piecesLabel=el('div','quiz-pieces-label','Фрагменты вперемешку'),pieces=el('div','quiz-pieces');pieces.id='quiz-pieces';pieces.setAttribute('role','group');pieces.setAttribute('aria-label','Фрагменты формулы');
 const editing=el('div','quiz-editing'),undo=button('Убрать фрагмент','text-button'),clear=button('Очистить сборку','text-button');undo.id='quiz-undo';clear.id='quiz-clear';editing.append(undo,clear);
 const feedback=el('div','feedback');feedback.id='quiz-feedback';feedback.setAttribute('role','status');feedback.setAttribute('aria-live','polite');
 const actions=el('div','quiz-actions'),check=button('Проверить формулу','primary-button'),next=button('Пропустить →');check.id='quiz-check';next.id='quiz-next';actions.append(check,next);
 const help=button('Нужна помощь ＋','text-button');help.id='quiz-help';
 cardBox.append(topline,title,conditions,previewFrame,instruction,slots,piecesLabel,pieces,editing,feedback,actions,help);
 const solution=el('section','solution quiz-solution');solution.id='quiz-solution';solution.setAttribute('aria-label','Пошаговый разбор формулы');
 const solutionHeader=el('div','solution-heading'),solutionTitle=el('div');solutionTitle.append(el('div','eyebrow','РАЗБЕРЁМСЯ ВМЕСТЕ'),el('h3','','Один шаг за раз'));
 const stepCount=el('span');solutionHeader.append(solutionTitle,stepCount);const steps=el('div'),more=button('Открыть следующий шаг ↓');more.id='quiz-next-step';solution.append(solutionHeader,steps,more);root.append(solution);
 const saved=el('p','quiz-save input-help');saved.id='quiz-save';root.append(saved);
 function persist(){saved.textContent=saveQuiz(storage,subject,state)?'Волна и история формул сохраняются в этом браузере. Прогресс заданий ведётся отдельно.':'Браузер запретил сохранение викторины. Пока вкладка открыта, можно продолжать.';}
 function stopTimer(){clearTimeout(timer);}
 function advance(){stopTimer();nextFormula(state,cards);render();persist();}
 function applyChoice(value){
  const round=state.round;if(round.result==='correct')return;
  round.selected[round.active]=value;const empty=round.selected.findIndex(v=>v===null);if(empty>=0)round.active=empty;
  round.result=null;render();persist();
 }
 function showSteps(card){
  const round=state.round;solution.hidden=!round.step;steps.replaceChildren();stepCount.textContent=round.step+' / 4';
  const explanations=[
   ['Условия и правило',card.conditions+' '+card.tip,null],
   ['Первая часть',card.parts.length===1?card.tip:'Оставим первые фрагменты, остальные пока скрыты.',card.parts.length===1?fullTex(card,[null]):fullTex(card,card.parts.map((v,i)=>i<Math.ceil(card.parts.length/2)?v:null))],
   ['Формула целиком',card.explanation,fullTex(card)],
   ['Закрепим',card.tip+' '+card.explanation+' В следующей попытке собери формулу без открытого разбора.',null]
  ];
  explanations.slice(0,round.step).forEach(([name,note,value],i)=>{const row=el('article','step');row.append(el('span','step-number',String(i+1)),el('h4','',name),el('p','',note));if(value){const m=el('div','math');tex(m,value,true);row.append(m);}steps.append(row);});
  more.disabled=round.step>=4;more.textContent=round.step>=4?'Разбор открыт целиком':'Открыть следующий шаг ↓';
 }
 function render(){
  const round=state.round,activeCards=cards.filter(c=>c.groups.some(g=>state.groups.includes(g)));
  const records=Object.values(state.items),clean=records.reduce((s,v)=>s+v.clean,0),recalled=activeCards.filter(c=>state.items[c.id]?.streak>=2).length;
  stats.replaceChildren(el('span','','Волна '+(state.wave||'—')),el('span','',activeCards.length+' формул'),el('span','','Без подсказок: '+clean),el('span','','Дважды подряд: '+recalled));
  cardBox.hidden=!round;welcome.hidden=!!round;solution.hidden=!round;launch.textContent=round?'Применить номера и начать волну':'Запустить волну';
  if(!round){solution.hidden=true;return;}
  const card=cards.find(c=>c.id===round.id),correct=round.result==='correct',wrong=round.result==='wrong'?matchFormula(card,round.selected):[];
  badge.textContent=card.groups.filter(g=>state.groups.includes(g)).map(g=>'№'+g).join(' · ')||'ФОРМУЛА';position.textContent=(state.cursor+1)+' / '+state.queue.length+' в волне';title.textContent=card.title;conditions.textContent=card.conditions;tex(preview,fullTex(card,round.selected),true);
  if(renderedRound!==round){
   renderedRound=round;slots.replaceChildren();pieces.replaceChildren();
   card.parts.forEach((_,i)=>{const b=button('','quiz-slot');b.dataset.slot=String(i);b.append(el('span','quiz-slot-label','Место '+(i+1)),el('span','quiz-slot-value'));b.onclick=()=>{round.active=i;render();persist();};slots.append(b);});
   round.choices.forEach((value,i)=>{const b=button('','quiz-piece');b.dataset.piece=String(i);tex(b,tileTex(value));b.onclick=()=>applyChoice(value);pieces.append(b);});
  }
  [...slots.children].forEach((b,i)=>{b.classList.toggle('active',round.active===i);b.classList.toggle('wrong',wrong.includes(i));b.classList.toggle('filled',round.selected[i]!==null);b.disabled=correct;b.setAttribute('aria-pressed',String(round.active===i));const value=b.querySelector('.quiz-slot-value');if(round.selected[i]===null)value.textContent='Нажми на фрагмент';else tex(value,tileTex(round.selected[i]));});
  [...pieces.children].forEach((b,i)=>{b.disabled=correct;b.setAttribute('aria-pressed',String(round.selected.includes(round.choices[i])));});
  check.disabled=correct||round.selected.some(v=>v===null);undo.disabled=clear.disabled=correct||round.selected.every(v=>v===null);help.disabled=correct||round.step>=4;
  next.textContent=correct?'Следующая формула →':'Пропустить →';feedback.hidden=!round.result;feedback.className='feedback '+(correct?'success':'error');
  feedback.textContent=correct?(round.hadError||round.step?'Верно. Теперь повторим эту формулу без подсказок в одной из следующих волн.':'Верно! Формула собрана самостоятельно.'):'Проверь '+wrong.map(i=>'место '+(i+1)).join(', ')+'. Ниже открыт первый шаг разбора.';
  showSteps(card);
 }
 launch.onclick=()=>{stopTimer();state.groups=chosenGroups();if(startWave(state,cards)){topics.open=false;render();persist();cardBox.scrollIntoView({behavior:'smooth',block:'start'});}};
 auto.onchange=()=>{state.autoAdvance=auto.checked;stopTimer();persist();};
 check.onclick=()=>{
  const result=submitFormula(state,cards.find(c=>c.id===state.round.id));if(!result.valid)return;
  render();persist();if(result.correct&&state.autoAdvance)timer=setTimeout(()=>{if(visible)advance();},1100);
 };
 next.onclick=advance;
 undo.onclick=()=>{const round=state.round;let index=round.active;if(round.selected[index]===null)index=round.selected.findLastIndex(v=>v!==null);if(index<0)return;round.selected[index]=null;round.active=index;round.result=null;render();persist();};
 clear.onclick=()=>{state.round.selected.fill(null);state.round.active=0;state.round.result=null;render();persist();};
 const reveal=()=>{stopTimer();state.round.step=Math.min(4,state.round.step+1);render();persist();};
 help.onclick=reveal;more.onclick=reveal;
 function setView(quiz,writeUrl=true){
  visible=quiz;stopTimer();if(quiz)cancelTaskAdvance();
  root.hidden=!quiz;document.getElementById('task-practice').hidden=quiz;
  for(const [id,selected] of [['show-quiz',quiz],['show-tasks',!quiz]]){const b=document.getElementById(id);b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected));}
  document.querySelector('.skip').href=quiz?'#formula-quiz':'#task-card';
  if(writeUrl){const url=new URL(location.href);if(quiz)url.searchParams.set('practice','formulas');else url.searchParams.delete('practice');history.replaceState(null,'',url);}
 }
 document.getElementById('show-quiz').onclick=()=>setView(true);document.getElementById('open-quiz').onclick=()=>setView(true);document.getElementById('show-tasks').onclick=()=>setView(false);
 window.addEventListener('pageshow',()=>setView(new URLSearchParams(location.search).get('practice')==='formulas',false));
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')stopTimer();});
 config();render();persist();setView(new URLSearchParams(location.search).get('practice')==='formulas',false);
 return {open:()=>setView(true)};
}
