import katex from './vendor/katex/katex.mjs';
import {checkAnswer} from './answer.js';
import {KEY,emptyState,loadState,saveState,itemState,recordAttempt,validateState} from './state.js';
const $=id=>document.getElementById(id);
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
const math=(target,tex)=>katex.render(tex,target,{displayMode:true,throwOnError:false,strict:'ignore',trust:false});
let tasks=[],coverage,state,ids,current,advanceTimer,toastTimer,storage,storageWarning=false;
try{storage=window.localStorage;}catch{storage={getItem:()=>null,setItem:()=>{throw Error();}};}
const names={1:'Чётность и ОДЗ',2:'Предел последовательности',3:'Второй замечательный предел'};
const statuses={new:'Ещё не решено',learning:'В работе',solved:'Самостоятельно ✓',assisted:'Решено с помощью'};
function persist(){if(!saveState(storage,state)){$('save-status').textContent='Сохранение недоступно';if(!storageWarning){storageWarning=true;toast('Браузер запретил сохранение. Скачивай историю перед закрытием.');}}}
function toast(text){clearTimeout(toastTimer);$('toast').textContent=text;$('toast').hidden=false;toastTimer=setTimeout(()=>$('toast').hidden=true,3500);}
function cancelAdvance(){clearTimeout(advanceTimer);}
function meta(task){
 if(task.id.startsWith('parity-'))return `Банк · пример ${Number(task.id.split('-')[1])}`;
 if(task.id.startsWith('sequence-'))return `Банк · пример ${Number(task.id.split('-')[1])}`;
 if(task.origin==='source')return task.sources[0].file==='solutions'?'Разбор · вариант 3':`Демо · ${task.sources[0].label}`;
 return `Тренировка · ${tasks.filter(t=>t.group===task.group&&t.origin==='extra').findIndex(t=>t.id===task.id)+1}`;
}
function filtered(){
 const query=$('search').value.trim().toLocaleLowerCase('ru');
 return tasks.filter(t=>{
  const status=state.items[t.id]?.status||'new';
  return (state.group==='all'||t.group===Number(state.group))&&(state.origin==='all'||t.origin===state.origin)&&
   (state.mode==='all'||state.mode==='new'&&status==='new'||state.mode==='review'&&['learning','assisted'].includes(status)||state.mode==='solved'&&status==='solved')&&
   (!query||`${t.topic} ${meta(t)} ${t.id} ${names[t.group]}`.toLocaleLowerCase('ru').includes(query));
 });
}
function updateOverview(){
 const values=Object.values(state.items),solved=values.filter(v=>v.status==='solved').length,assisted=values.filter(v=>v.status==='assisted').length;
 $('progress-number').textContent=solved;$('progress-total').textContent=`/ ${tasks.length}`;
 $('progress-bar').style.width=`${100*solved/tasks.length}%`;
 $('progress-title').textContent=solved?`${solved} ${solved%10===1&&solved%100!==11?'задание решено':'заданий решено'} самостоятельно`:'Начни с одного задания';
 $('progress-description').textContent=assisted?`Ещё ${assisted} с помощью. Их можно найти в «Повторить».`:'Решения откроются только тогда, когда понадобятся.';
 $('coverage-label').textContent=`${coverage.source} из материалов · ${coverage.extra} дополнительных`;
}
function renderList(list){
 $('list-total').textContent=`${list.length}`;$('task-list').replaceChildren();
 for(const task of list){
  const button=el('button',task.id===state.selected?'active':'');button.type='button';button.dataset.taskId=task.id;
  button.setAttribute('aria-label',`№${task.group}, ${meta(task)}, ${task.topic}`);
  if(task.id===state.selected)button.setAttribute('aria-current','true');
  const number=el('span','list-index',task.id.startsWith('parity-')||task.id.startsWith('sequence-')?task.id.slice(-2):'↗');
  const copy=el('span','list-task-copy');copy.append(el('strong','',meta(task)),el('small','',task.topic));
  const status=state.items[task.id]?.status||'new';const dot=el('i',`dot ${status}`);dot.title=statuses[status];
  button.append(number,copy,dot);button.addEventListener('click',()=>navigate(task.id,true));$('task-list').append(button);
 }
}
function render(){
 cancelAdvance();updateOverview();
 document.querySelectorAll('[data-group]').forEach(b=>{const active=b.dataset.group===state.group;b.classList.toggle('active',active);b.setAttribute('aria-pressed',active);});
 document.querySelectorAll('[data-mode]').forEach(b=>{const active=b.dataset.mode===state.mode;b.classList.toggle('selected',active);b.setAttribute('aria-pressed',active);});
 $('origin-filter').value=state.origin;
 const list=filtered();
 if(!list.some(t=>t.id===state.selected))state.selected=list[0]?.id||null;
 current=tasks.find(t=>t.id===state.selected);
 renderList(list);
 $('task-card').hidden=!current;$('empty-state').hidden=!!current;$('solution').hidden=true;
 if(!current){persist();return;}
 const item=itemState(state,current.id);
 $('task-group').textContent=`ЗАДАНИЕ ${current.group}`;
 $('task-position').textContent=`${list.findIndex(t=>t.id===current.id)+1} из ${list.length}`;
 $('task-heading').textContent=current.topic;
 $('task-status').textContent=statuses[item.status];
 $('task-instruction').textContent=current.kind==='choice'?'Определи чётность функции на её исходной области определения.':'Вычисли предел. Введи только итоговый ответ.';
 math($('problem'),current.prompt);
 $('task-note').hidden=!current.note;$('task-note').textContent=current.note||'';
 $('answer-row').hidden=current.kind==='choice';$('choices').hidden=current.kind!=='choice';
 $('answer-label').textContent=current.kind==='choice'?'Выбери верное утверждение':'Твой ответ';
 $('answer-help').textContent=current.kind==='choice'?'1 — чётная · 2 — нечётная · 3 — ни та ни другая':'Примеры: 2/3, sqrt(2), 3sqrt(3), e^(-3), e^(-3*pi/4), ∞. Десятичная запятая тоже работает.';
 $('answer').value=item.draft||'';
 $('feedback').hidden=true;
 $('next').firstChild.textContent=['solved','assisted'].includes(item.status)?'Следующее ':'Пропустить ';
 $('previous').disabled=list.findIndex(t=>t.id===current.id)===0;
 $('source-links').replaceChildren();
 for(const src of current.sources){
  const a=el('a','',`${{bank:'Банк',demo:'Демо',solutions:'Разбор',theory:'Теория'}[src.file]}: ${src.label} ↗`);
  a.href=`./sources/${src.file}.pdf#page=${src.page}`;a.target='_blank';a.rel='noopener';$('source-links').append(a);
 }
 if(!current.sources.length)$('source-links').append(el('span','input-help','Дополнительная задача для тренировки.'));
 $('reveal').textContent=item.step?'Продолжить разбор ＋':'Нужна помощь ＋';
 renderSteps();persist();
}
function renderSteps(){
 if(!current)return;
 const item=itemState(state,current.id),count=Math.min(item.step,current.stages.length);
 $('solution').hidden=!count;$('steps').replaceChildren();$('step-count').textContent=`${count} / ${current.stages.length}`;
 current.stages.slice(0,count).forEach((stage,i)=>{
  const section=el('article','step');section.append(el('span','step-number',`${i+1}`),el('h4','',stage.title));
  for(const block of stage.blocks){if(block.note)section.append(el('p','',block.note));if(block.tex){const m=el('div','math');math(m,block.tex);section.append(m);}}
  $('steps').append(section);
 });
 $('next-step').textContent=count<current.stages.length?'Открыть следующий шаг ↓':'Повторить самостоятельно ↺';
 $('reveal').textContent=count?'Продолжить разбор ＋':'Нужна помощь ＋';
}
function reveal(){
 if(!current)return;cancelAdvance();const item=itemState(state,current.id);
 if(item.step<current.stages.length){item.step++;if(item.status==='new'||item.status==='solved')item.status='learning';}
 renderSteps();updateOverview();renderList(filtered());$('task-status').textContent=statuses[item.status];persist();
 $('solution').scrollIntoView({behavior:'smooth',block:'nearest'});
}
function navigate(id,focus=false){cancelAdvance();state.selected=id;render();if(focus){$('task-card').scrollIntoView({behavior:'smooth',block:'start'});}}
function next(){
 if(!current)return;const list=filtered(),i=list.findIndex(t=>t.id===current.id);
 if(list.length<=1){toast('Это последнее задание в текущем списке. Можно изменить фильтр.');return;}
 navigate(list[(i+1)%list.length].id);
}
function feedback(text,kind){$('feedback').className=`feedback ${kind}`;$('feedback').textContent=text;$('feedback').hidden=false;}
function submit(value){
 if(!current)return;cancelAdvance();const task=current,oldList=filtered(),index=oldList.findIndex(t=>t.id===task.id);
 const result=checkAnswer(task,value);
 if(!result.valid){feedback(result.message,'neutral');return;}
 const item=recordAttempt(state,task.id,String(value),result.correct);item.draft=String(value);persist();updateOverview();
 $('task-status').textContent=statuses[item.status];renderList(filtered());
 if(result.correct){
  feedback(item.status==='solved'?'Верно. Задание решено самостоятельно.':'Верно. Сохранили в «Повторить»: в этой попытке была помощь.','success');
  $('next').firstChild.textContent='Следующее ';
  if(state.autoAdvance){advanceTimer=setTimeout(()=>{
   if(current?.id!==task.id)return;
   const eligible=filtered(),nextCandidate=oldList.slice(index+1).find(t=>eligible.some(v=>v.id===t.id))||eligible.find(t=>t.id!==task.id);
   if(nextCandidate){navigate(nextCandidate.id,true);toast('Верно. Перешли к следующему заданию.');(current?.kind==='choice'?$('choices').querySelector('button'):$('answer')).focus({preventScroll:true});}
   else toast('Все задания в этом списке пройдены. Выбери другой раздел или фильтр.');
  },1100);}
 }else{
  feedback(item.step===1?'Пока неверно. Проверь своё решение. Ниже открыт только первый этап: нужные формулы.':'Пока неверно. Проверь своё решение; следующий этап разбора можно открыть кнопкой ниже.','error');
  renderSteps();
 }
}
function theme(name){state.theme=name;document.documentElement.dataset.theme=name;document.querySelectorAll('button[data-theme]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.theme===name));$('theme-select').value=name;persist();}
function openSettings(){
 $('auto-advance').checked=state.autoAdvance;
 const values=Object.values(state.items),attempts=values.reduce((sum,v)=>sum+v.attempts.length,0);
 $('settings-stats').replaceChildren(el('span','',`Самостоятельно: ${values.filter(v=>v.status==='solved').length}`),el('span','',`С помощью: ${values.filter(v=>v.status==='assisted').length}`),el('span','',`Попыток: ${attempts}`));
 $('history-list').replaceChildren(el('h3','', 'Последние попытки'));
 const all=Object.entries(state.items).flatMap(([id,v])=>v.attempts.map(a=>({id,...a}))).sort((a,b)=>b.at-a.at).slice(0,30);
 if(!all.length)$('history-list').append(el('p','input-help','Здесь появится история ответов.'));
 for(const a of all){const task=tasks.find(t=>t.id===a.id);const row=el('div','history-entry');row.append(el('span','',`№${task.group} · ${meta(task)}`),el('time','',new Date(a.at).toLocaleString('ru-RU',{dateStyle:'short',timeStyle:'short'})),el('span',a.correct?'correct':'wrong',`${a.correct?'Верно':'Ошибка'}: ${a.answer}`));$('history-list').append(row);}
 $('settings-dialog').showModal();
}
function sources(){
 $('sources-description').textContent=`Интерактивно: ${coverage.total} заданий по №1–3 билета (${coverage.source} из материалов и ${coverage.extra} дополнительных).`;
 $('sources-content').replaceChildren();
 for(const file of coverage.sourceFiles){const a=el('a','source-document',file.title);a.href=`./sources/${file.id}.pdf`;a.target='_blank';a.rel='noopener';a.append(el('small','',file.id==='theory'?'Теоретический список доступен как PDF.':'Оригинал PDF · открыть в новой вкладке ↗'));$('sources-content').append(a);}
 for(const note of coverage.notes)$('sources-content').append(el('p','input-help',note));
 $('sources-dialog').showModal();
}
function formulas(){
 $('formula-content').replaceChildren();
 const sections=[
  ['Второй замечательный предел','При A → 1 и положительном основании; L конечен.',String.raw`L=\lim(A-1)B\quad\Longrightarrow\quad A^B\to e^L`],
  ['Эквивалентности','Все формулы при t → 0. Углы в радианах.',String.raw`\begin{gathered}\sin t\sim t,\quad\tan t\sim t,\quad\arctan t\sim t,\quad\arcsin t\sim t\\1-\cos t\sim\frac{t^2}{2},\quad\ln(1+t)\sim t,\quad e^t-1\sim t\end{gathered}`],
  ['Знаки и сложный аргумент','При x → 0 и фиксированном k ≠ 0.',String.raw`\cos^2t-1=-\sin^2t,\quad\sin^2(kx)\sim k^2x^2`],
  ['Сопряжённое','Знаменатель справа не равен нулю. Сначала преобразование, затем предел.',String.raw`\sqrt A-\sqrt B=\frac{A-B}{\sqrt A+\sqrt B}`],
  ['Корни и степени','n > 0. Сравнивай дробные показатели без округления.',String.raw`\sqrt[k]{n^p}=n^{p/k},\qquad\sqrt{x^2}=|x|`],
  ['Суммы','Геометрическая формула при q ≠ 1.',String.raw`1+\cdots+n=\frac{n(n+1)}2,\quad1+q+\cdots+q^n=\frac{1-q^{n+1}}{1-q}`],
  ['Арктангенс и арккотангенс','Пределы при x → +∞; arccot x ∈ (0, π).',String.raw`\arctan x\to\frac\pi2,\quad\operatorname{arccot}x\to0,\quad\arctan x+\operatorname{arccot}x=\frac\pi2`],
  ['Чётность','Сначала симметричная исходная ОДЗ. Сокращение не возвращает исключённые точки.',String.raw`f(-x)=f(x)\ \text{(чётная)},\qquad f(-x)=-f(x)\ \text{(нечётная)}`]
 ];
 for(const [title,note,tex] of sections){const box=el('section','formula-section');const m=el('div','math');math(m,tex);box.append(el('h3','',title),el('p','',note),m);$('formula-content').append(box);}
 $('formulas-dialog').showModal();
}
async function init(){
 try{
  const responses=await Promise.all([fetch('./tasks.json'),fetch('./coverage.json')]);
  if(responses.some(r=>!r.ok))throw Error('Не удалось загрузить банк заданий.');
  [tasks,coverage]=await Promise.all(responses.map(r=>r.json()));ids=new Set(tasks.map(t=>t.id));state=loadState(storage,ids);
  // Mobile controls live in the same settings dialog.
  const row=el('label','setting-row');row.append(el('span','','Цветовая тема'));const select=el('select');select.id='theme-select';
  for(const [value,label] of [['sage','Шалфей'],['paper','Тёплая бумага'],['lavender','Лаванда'],['night','Тихий вечер']]){const option=el('option','',label);option.value=value;select.append(option);}
  row.append(select);$('settings-dialog').insertBefore(row,$('settings-stats'));
  const tools=el('div','dialog-actions');for(const [label,callback] of [['Формулы',formulas],['Материалы',sources]]){const b=el('button','secondary-button',label);b.onclick=()=>{$('settings-dialog').close();callback();};tools.append(b);}$('settings-dialog').insertBefore(tools,$('history-list'));
  theme(state.theme);
  for(const g of ['all','1','2','3'])$('count-'+g).textContent=g==='all'?tasks.length:coverage.groups[g];
  document.querySelectorAll('[data-group]').forEach(b=>b.addEventListener('click',()=>{state.group=b.dataset.group;render();}));
  document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{state.mode=b.dataset.mode;render();}));
  document.querySelectorAll('button[data-theme]').forEach(b=>b.addEventListener('click',()=>theme(b.dataset.theme)));
  select.onchange=()=>theme(select.value);
  $('origin-filter').onchange=()=>{state.origin=$('origin-filter').value;render();};$('search').oninput=render;
  $('answer').oninput=()=>{if(current){itemState(state,current.id).draft=$('answer').value;persist();}};
  $('answer-form').onsubmit=e=>{e.preventDefault();submit($('answer').value);};
  document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>submit(b.dataset.choice));
  $('reveal').onclick=reveal;
  $('next-step').onclick=()=>{const item=itemState(state,current.id);if(item.step>=current.stages.length){item.step=0;item.status='learning';item.draft='';render();toast('Новая попытка без раскрытого решения.');}else reveal();};
  $('next').onclick=next;
  $('previous').onclick=()=>{const list=filtered(),i=list.findIndex(t=>t.id===current.id);if(i>0)navigate(list[i-1].id);};
  $('clear-filters').onclick=()=>{state.mode='all';state.group='all';state.origin='all';$('search').value='';render();};
  $('open-settings').onclick=openSettings;$('mobile-settings').onclick=openSettings;
  $('open-sources').onclick=sources;$('open-formulas').onclick=formulas;
  document.querySelectorAll('.close-dialog').forEach(b=>b.onclick=()=>b.closest('dialog').close());
  document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
  $('auto-advance').onchange=()=>{state.autoAdvance=$('auto-advance').checked;cancelAdvance();persist();};
  $('export-progress').onclick=()=>{const blob=new Blob([JSON.stringify({...state,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'});const a=el('a');a.href=URL.createObjectURL(blob);a.download=`matan-progress-${new Date().toISOString().slice(0,10)}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
  $('import-progress').onclick=()=>$('import-file').click();
  $('import-file').onchange=async()=>{const file=$('import-file').files[0];if(!file)return;try{if(file.size>2_000_000)throw Error('Файл слишком большой.');const incoming=validateState(JSON.parse(await file.text()),ids);state=incoming;theme(state.theme);render();$('settings-dialog').close();toast('История загружена.');}catch(e){$('import-message').textContent=e.message;}$('import-file').value='';};
  $('reset-progress').onclick=()=>{if(!confirm('Удалить все попытки и подсказки в этом браузере?'))return;const keepTheme=state.theme;state=emptyState();state.theme=keepTheme;theme(keepTheme);render();$('settings-dialog').close();toast('Прогресс сброшен.');};
  render();
 }catch(e){$('task-heading').textContent='Не удалось открыть тренажёр';$('task-instruction').textContent=e.message+' Обнови страницу или проверь подключение.';console.error(e);}
}
init();
