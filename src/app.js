import katex from './vendor/katex/katex.mjs';
import {checkAnswer as checkMathAnswer} from './answer.js';
import {checkLinearAnswer} from './linear-answer.js';
import {subject,isLinear,subjectStorage,setupSubjects} from './subjects.js';
import {linearFormulas,linearInputHelp,addLinearKeys,renderGraph} from './linear-ui.js';
import {mountKeyboard} from './keyboard.js';
import {THEME_KEY,loadTheme,saveTheme} from './theme.js';
import {KEY,emptyState,loadState,saveState,itemState,recordAttempt,validateState} from './state.js';
const $=id=>document.getElementById(id);
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
const math=(target,tex)=>katex.render(tex,target,{displayMode:true,throwOnError:false,strict:'ignore',trust:false});
let tasks=[],coverage,state,ids,current,advanceTimer,toastTimer,storage,keyboard,activeAnswerInput,storageWarning=false;
try{storage=window.localStorage;}catch{storage={getItem:()=>null,setItem:()=>{throw Error();}};}
const preferences=storage;
document.documentElement.dataset.theme=loadTheme(preferences,document.documentElement.dataset.theme);
storage=subjectStorage(storage);
const checkAnswer=isLinear?checkLinearAnswer:checkMathAnswer;
let names={};
const statuses={new:'Ещё не решено',learning:'В работе',solved:'Самостоятельно ✓',assisted:'Решено с помощью'};
function persist(){if(!saveState(storage,state)){$('save-status').textContent='Сохранение недоступно';if(!storageWarning){storageWarning=true;toast('Браузер запретил сохранение. Скачивай историю перед закрытием.');}}}
function toast(text){clearTimeout(toastTimer);$('toast').textContent=text;$('toast').hidden=false;toastTimer=setTimeout(()=>$('toast').hidden=true,3500);}
function cancelAdvance(){clearTimeout(advanceTimer);}
function meta(task){
 if(task.meta)return task.meta;
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
function adjacent(direction=1){
 if(!current)return;
 // Status filters can remove the displayed task after an answer or a hint.
 // Keep its position in the full list as the anchor for both directions.
 const index=tasks.findIndex(t=>t.id===current.id),eligible=new Set(filtered().map(t=>t.id));
 if(index<0)return;
 for(let i=index+direction;i>=0&&i<tasks.length;i+=direction)if(eligible.has(tasks[i].id))return tasks[i];
}
function updateNavigation(){$('previous').disabled=!adjacent(-1);}
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
 $('task-instruction').textContent=current.instruction||(current.kind==='choice'?'Определи чётность функции на её исходной области определения.':'Вычисли предел. Введи только итоговый ответ.');
 $('task-description').textContent=current.description||'';$('task-description').hidden=!current.description;
 math($('problem'),current.prompt);
 $('task-note').hidden=!current.note;$('task-note').textContent=current.note||'';
 renderAnswer(item);
 $('feedback').hidden=true;
 $('next').firstChild.textContent=['solved','assisted'].includes(item.status)?'Следующее ':'Пропустить ';
 updateNavigation();
 $('source-links').replaceChildren();
 for(const src of current.sources){
  const a=el('a','',isLinear?`${src.label} ↗`:`${{bank:'Банк',demo:'Демо',solutions:'Разбор',theory:'Теория'}[src.file]}: ${src.label} ↗`);
  a.href=`./sources/${src.file}.pdf#page=${src.page}`;a.target='_blank';a.rel='noopener';$('source-links').append(a);
 }
 if(!current.sources.length)$('source-links').append(el('span','input-help','Дополнительная задача для тренировки.'));
 $('reveal').textContent=item.step?'Продолжить разбор ＋':'Нужна помощь ＋';
 renderSteps();persist();
}
function answerValue(){
 if(current.kind==='fields')return JSON.stringify(Object.fromEntries([...$('answer-fields').querySelectorAll('input')].map(i=>[i.dataset.field,i.value])));
 if(current.kind==='multi')return [...$('choices').querySelectorAll('input:checked')].map(i=>i.value).join(';');
 return $('answer').value;
}
function draft(){if(current){itemState(state,current.id).draft=answerValue();persist();}}
function activateInput(input){activeAnswerInput=input;keyboard.setInput(input);document.querySelectorAll('.field-entry').forEach(row=>row.classList.toggle('active-field',row.contains(input)));}
function renderAnswer(item){
 const choice=['choice','multi'].includes(current.kind),fields=current.kind==='fields';
 $('answer-row').hidden=choice||fields;$('choices').hidden=!choice;$('answer-fields').hidden=!fields;$('math-keyboard').hidden=choice;
 $('answer-label').hidden=fields;$('answer-label').textContent=choice?'Выбери утверждения':'Твой ответ';
 $('answer-help').textContent=choice?(current.kind==='multi'?'Можно выбрать несколько пунктов. Отметь все подходящие и нажми «Проверить».':'Нажми на один вариант ответа.'):'Дробь: 2/3 · корень: sqrt(2) · степень: e^(-3). Координаты: (x;y), точки разделяй |, прямые и числа в списке — ;. Углы в радианах.';
 $('choices').replaceChildren();$('answer-fields').replaceChildren();
 if(choice){
  const options=current.options||[{value:'1',label:'Чётная'},{value:'2',label:'Нечётная'},{value:'3',label:'Ни та ни другая'}];
  for(const o of options){
   if(current.kind==='choice'){const button=el('button');button.type='button';button.dataset.choice=o.value;button.append(el('span','',o.value),document.createTextNode(' '+o.label));button.onclick=()=>submit(o.value);$('choices').append(button);}
   else{const label=el('label','multi-option'),input=el('input');input.type='checkbox';input.value=o.value;input.checked=(item.draft||'').split(';').includes(o.value);input.onchange=draft;label.append(input,el('span','',`${o.value}. ${o.label}`));$('choices').append(label);}
  }
  if(current.kind==='multi'){const button=el('button','primary-button','Проверить ↵');button.type='submit';$('choices').append(button);}
 }else if(fields){
  let values={};try{values=JSON.parse(item.draft||'{}');}catch{}
  for(const f of current.fields){
   const row=el('div','field-entry'),label=el('label','',f.label),input=el('input');input.id='field-'+f.id;input.dataset.field=f.id;input.name=f.id;input.maxLength=256;input.spellcheck=false;input.value=values[f.id]||'';input.placeholder=({points:'(x;y) | (x;y)',lines:'x=…; y=…',set:'значение; значение',expression:'Выражение через '+(f.variables||[]).join(', ')})[f.kind]||'Только итоговый ответ';
   if(isLinear)linearInputHelp(f,input);
   label.htmlFor=input.id;input.onfocus=()=>activateInput(input);input.onpointerdown=()=>activateInput(input);input.oninput=draft;row.append(label,input);$('answer-fields').append(row);
   if(isLinear&&['matrix','complex','complex-set','equation','line3','affine','system-point','vector'].includes(f.kind)){const help=el('p','input-help');linearInputHelp(f,input,help);row.append(help);}
  }
  const button=el('button','primary-button','Проверить все поля ↵');button.type='submit';$('answer-fields').append(button);activateInput($('answer-fields').querySelector('input'));
 }else{$('answer').value=item.draft||'';activateInput($('answer'));if(isLinear)linearInputHelp(current,$('answer'),$('answer-help'));}
 if(isLinear&&fields)$('answer-help').textContent='Заполни все поля. Матрицы: 1 2; 3 4. Координаты: (1;2;3). Корни: sqrt(2). Углы в радианах.';
}
function renderSteps(){
 if(!current)return;
 const item=itemState(state,current.id),count=Math.min(item.step,current.stages.length);
 $('solution').hidden=!count;$('steps').replaceChildren();$('step-count').textContent=`${count} / ${current.stages.length}`;
 current.stages.slice(0,count).forEach((stage,i)=>{
  const section=el('article','step');section.append(el('span','step-number',`${i+1}`),el('h4','',stage.title));
  for(const block of stage.blocks){if(block.note)section.append(el('p','',block.note));if(block.tex){const m=el('div','math');math(m,block.tex);section.append(m);}if(isLinear&&block.graph)section.append(renderGraph(block.graph));}
  $('steps').append(section);
 });
 $('next-step').textContent=count<current.stages.length?'Открыть следующий шаг ↓':'Повторить самостоятельно ↺';
 $('reveal').textContent=count?'Продолжить разбор ＋':'Нужна помощь ＋';
}
function reveal(){
 if(!current)return;cancelAdvance();const item=itemState(state,current.id);
 if(item.step<current.stages.length){item.step++;if(item.status==='new'||item.status==='solved')item.status='learning';}
 renderSteps();updateOverview();renderList(filtered());updateNavigation();$('task-status').textContent=statuses[item.status];persist();
 $('solution').scrollIntoView({behavior:'smooth',block:'nearest'});
}
function navigate(id,focus=false){cancelAdvance();state.selected=id;render();if(focus){$('task-card').scrollIntoView({behavior:'smooth',block:'start'});}}
function next(){
 if(!current)return;const candidate=adjacent();
 if(candidate)navigate(candidate.id);
 else toast('Дальше в этом списке заданий нет. Можно выбрать другое задание или изменить фильтр.');
}
function feedback(text,kind){$('feedback').className=`feedback ${kind}`;$('feedback').textContent=text;$('feedback').hidden=false;const r=$('feedback').getBoundingClientRect();if(r.bottom>innerHeight||r.top<0)$('feedback').scrollIntoView({behavior:'smooth',block:'nearest'});}
function submit(value){
 if(!current)return;cancelAdvance();const task=current;
 const result=checkAnswer(task,value);
 if(!result.valid){feedback(result.message,'neutral');return;}
 const item=recordAttempt(state,task.id,String(value),result.correct);item.draft=String(value);persist();updateOverview();
 $('task-status').textContent=statuses[item.status];renderList(filtered());updateNavigation();
 if(result.correct){
  feedback(item.status==='solved'?'Верно. Задание решено самостоятельно.':'Верно. Сохранили в «Повторить»: в этой попытке была помощь.','success');
  $('next').firstChild.textContent='Следующее ';
  if(state.autoAdvance){advanceTimer=setTimeout(()=>{
   if(current?.id!==task.id)return;
   const nextCandidate=adjacent();
   if(nextCandidate){navigate(nextCandidate.id,true);toast('Верно. Перешли к следующему заданию.');if(window.matchMedia('(pointer:fine)').matches)(document.querySelector('#choices:not([hidden]) button, #answer-fields:not([hidden]) input, #answer-row:not([hidden]) input'))?.focus({preventScroll:true});else document.activeElement?.blur();}
   else toast('Дальше в этом списке заданий нет. Можно выбрать другое задание или изменить фильтр.');
  },1100);}
 }else{
  feedback((result.incorrect?.length?`Проверь поля: ${result.incorrect.join(', ')}. `:'Пока неверно. ')+(item.step===1?'Ниже открыт первый этап: нужные формулы.':'Следующий этап разбора можно открыть кнопкой ниже.'),'error');
  renderSteps();
 }
}
function theme(name,save=true){state.theme=name;document.documentElement.dataset.theme=name;document.querySelectorAll('button[data-theme]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.theme===name));$('theme-select').value=name;if(save){saveTheme(preferences,name);persist();}}
function openSettings(){
 $('auto-advance').checked=state.autoAdvance;
 const values=Object.values(state.items),attempts=values.reduce((sum,v)=>sum+v.attempts.length,0);
 $('settings-stats').replaceChildren(el('span','',`Самостоятельно: ${values.filter(v=>v.status==='solved').length}`),el('span','',`С помощью: ${values.filter(v=>v.status==='assisted').length}`),el('span','',`Попыток: ${attempts}`));
 $('history-list').replaceChildren(el('h3','', 'Последние попытки'));
 const all=Object.entries(state.items).flatMap(([id,v])=>v.attempts.map(a=>({id,...a}))).sort((a,b)=>b.at-a.at).slice(0,30);
 if(!all.length)$('history-list').append(el('p','input-help','Здесь появится история ответов.'));
 for(const a of all){const task=tasks.find(t=>t.id===a.id);let text=a.answer;if(task.kind==='fields')try{const values=JSON.parse(a.answer);text=task.fields.map(f=>`${f.label}: ${values[f.id]||'—'}`).join(' · ');}catch{}const row=el('div','history-entry');row.append(el('span','',`№${task.group} · ${meta(task)}`),el('time','',new Date(a.at).toLocaleString('ru-RU',{dateStyle:'short',timeStyle:'short'})),el('span',a.correct?'correct':'wrong',`${a.correct?'Верно':'Ошибка'}: ${text}`));$('history-list').append(row);}
 $('settings-dialog').showModal();
}
function sources(){
 $('sources-description').textContent=`${isLinear?'Линал · 1 семестр 2025–26. ':''}Все №1–10 билета: ${coverage.total} карточек (${coverage.source} из материалов и ${coverage.extra} дополнительных).`;
 $('sources-content').replaceChildren();
 for(const file of coverage.sourceFiles){const a=el('a','source-document',file.title);a.href=`./sources/${file.id}.pdf`;a.target='_blank';a.rel='noopener';a.append(el('small','',file.id==='theory'?'Теоретический список доступен как PDF.':'Оригинал PDF · открыть в новой вкладке ↗'));$('sources-content').append(a);}
 for(const note of coverage.notes)$('sources-content').append(el('p','input-help',note));
 if(coverage.sourceIssues?.length){$('sources-content').append(el('h3','','Особенности печатных условий'));for(const issue of coverage.sourceIssues){const task=tasks.find(t=>t.id===issue.id);const button=el('button','source-issue',`${meta(task)}: ${issue.reason}`);button.onclick=()=>{state.group='all';state.mode='all';state.origin='all';$('search').value='';$('sources-dialog').close();navigate(issue.id,true);};$('sources-content').append(button);}}
 $('sources-dialog').showModal();
}
function formulas(){
 $('formula-content').replaceChildren();
 const sections=isLinear?linearFormulas:[
  ['Второй замечательный предел','При A → 1 и положительном основании; L конечен.',String.raw`L=\lim(A-1)B\quad\Longrightarrow\quad A^B\to e^L`],
  ['Эквивалентности','Все формулы при t → 0. Углы в радианах.',String.raw`\begin{gathered}\sin t\sim t,\quad\tan t\sim t,\quad\arctan t\sim t,\quad\arcsin t\sim t\\1-\cos t\sim\frac{t^2}{2},\quad\ln(1+t)\sim t,\quad e^t-1\sim t\end{gathered}`],
  ['Знаки и сложный аргумент','При x → 0 и фиксированном k ≠ 0.',String.raw`\cos^2t-1=-\sin^2t,\quad\sin^2(kx)\sim k^2x^2`],
  ['Сопряжённое','Знаменатель справа не равен нулю. Сначала преобразование, затем предел.',String.raw`\sqrt A-\sqrt B=\frac{A-B}{\sqrt A+\sqrt B}`],
  ['Корни и степени','n > 0. Сравнивай дробные показатели без округления.',String.raw`\sqrt[k]{n^p}=n^{p/k},\qquad\sqrt{x^2}=|x|`],
  ['Суммы','Геометрическая формула при q ≠ 1.',String.raw`1+\cdots+n=\frac{n(n+1)}2,\quad1+q+\cdots+q^n=\frac{1-q^{n+1}}{1-q}`],
  ['Арктангенс и арккотангенс','Пределы при x → +∞; arccot x ∈ (0, π).',String.raw`\arctan x\to\frac\pi2,\quad\operatorname{arccot}x\to0,\quad\arctan x+\operatorname{arccot}x=\frac\pi2`],
  ['Чётность','Сначала симметричная исходная ОДЗ. Сокращение не возвращает исключённые точки.',String.raw`f(-x)=f(x)\ \text{(чётная)},\qquad f(-x)=-f(x)\ \text{(нечётная)}`],
  ['Производные','Сначала производная как функция, затем подстановка точки.',String.raw`\begin{gathered}(x^a)'=ax^{a-1},\ (e^x)'=e^x,\ (\ln x)'=1/x\\(\sin x)'=\cos x,\ (\cos x)'=-\sin x\\(\tan x)'=1/\cos^2x,\ (\arctan x)'=1/(1+x^2)\\(uv)'=u'v+uv',\ (u/v)'=(u'v-uv')/v^2\\(F(u))'=F'(u)u'\end{gathered}`],
  ['Касательная и нормаль','У нормали эта формула при f′(x₀) ≠ 0.',String.raw`y-f(x_0)=f'(x_0)(x-x_0),\quad k_n=-1/f'(x_0)`],
  ['Асимптоты','На +∞ и −∞ проверяем отдельно. Для вертикальной нужен бесконечный односторонний предел.',String.raw`k=\lim f(x)/x,\quad b=\lim(f(x)-kx),\quad y=kx+b`],
  ['Экстремум и перегиб','Нулевой производной недостаточно: проверяй смену знака. Для максимума на отрезке сравнивай также концы.',String.raw`f':+\to-\Rightarrow\max,\quad f':-\to+\Rightarrow\min;\quad f''\text{ меняет знак}\Rightarrow\text{перегиб}`],
  ['Частные и параметрические производные','При частном дифференцировании остальные независимые переменные фиксируем.',String.raw`z_{xy}=\partial_y(\partial_xz),\quad dy/dx=y_t'/x_t'\quad(x_t'\ne0)`]
 ];
 for(const [title,note,tex] of sections){const box=el('section','formula-section');const m=el('div','math');math(m,tex);box.append(el('h3','',title),el('p','',note),m);$('formula-content').append(box);}
 $('formulas-dialog').showModal();
}
async function init(){
 try{
  setupSubjects();
  const responses=await Promise.all(isLinear?[fetch('./linear-tasks.json'),fetch('./linear-coverage.json')]:[fetch('./tasks.json'),fetch('./coverage.json')]);
  if(responses.some(r=>!r.ok))throw Error('Не удалось загрузить банк заданий.');
  [tasks,coverage]=await Promise.all(responses.map(r=>r.json()));ids=new Set(tasks.map(t=>t.id));state=loadState(storage,ids);
  names=coverage.sections;
  const nav=document.querySelector('.group-nav');nav.replaceChildren();
  for(const [g,label] of [['all','Все задания'],...Object.entries(names)]){const button=el('button','nav-item');button.dataset.group=g;button.append(el('span',g==='all'?'nav-icon':'nav-number',g==='all'?'◈':g),el('span','',label));const count=el('span','nav-count',String(g==='all'?tasks.length:coverage.groups[g]));count.id='count-'+g;button.append(count);nav.append(button);}
  // Mobile controls live in the same settings dialog.
  const row=el('label','setting-row');row.append(el('span','','Цветовая тема'));const select=el('select');select.id='theme-select';
  for(const [value,label] of [['sage','Шалфей'],['paper','Тёплая бумага'],['lavender','Лаванда'],['night','Тихий вечер']]){const option=el('option','',label);option.value=value;select.append(option);}
  row.append(select);$('settings-dialog').insertBefore(row,$('settings-stats'));
  const tools=el('div','dialog-actions');for(const [label,callback] of [['Формулы',formulas],['Материалы',sources]]){const b=el('button','secondary-button',label);b.onclick=()=>{$('settings-dialog').close();callback();};tools.append(b);}$('settings-dialog').insertBefore(tools,$('history-list'));
  // Adopt the current subject's legacy theme once, then share it across subjects.
  theme(loadTheme(preferences,state.theme));
  const syncTheme=()=>theme(loadTheme(preferences,state.theme),false);
  window.addEventListener('storage',event=>{if(event.key===THEME_KEY)syncTheme();});
  window.addEventListener('pageshow',()=>{syncTheme();$('subject-select').value=subject;});
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')syncTheme();});
  keyboard=mountKeyboard($('math-keyboard'),$('answer'));
  if(isLinear)addLinearKeys($('math-keyboard'),()=>activeAnswerInput);
  document.querySelectorAll('[data-group]').forEach(b=>b.addEventListener('click',()=>{state.group=b.dataset.group;render();}));
  document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{state.mode=b.dataset.mode;render();}));
  document.querySelectorAll('button[data-theme]').forEach(b=>b.addEventListener('click',()=>theme(b.dataset.theme)));
  select.onchange=()=>theme(select.value);
  $('origin-filter').onchange=()=>{state.origin=$('origin-filter').value;render();};$('search').oninput=render;
  $('answer').oninput=draft;$('answer').onfocus=()=>activateInput($('answer'));
  $('answer-form').onsubmit=e=>{e.preventDefault();submit(answerValue());};
  $('reveal').onclick=reveal;
  $('next-step').onclick=()=>{const item=itemState(state,current.id);if(item.step>=current.stages.length){item.step=0;item.status='learning';item.draft='';render();toast('Новая попытка без раскрытого решения.');}else reveal();};
  $('next').onclick=next;
  $('previous').onclick=()=>{const candidate=adjacent(-1);if(candidate)navigate(candidate.id);};
  $('clear-filters').onclick=()=>{state.mode='all';state.group='all';state.origin='all';$('search').value='';render();};
  $('open-settings').onclick=openSettings;$('mobile-settings').onclick=openSettings;
  $('open-sources').onclick=sources;$('open-formulas').onclick=formulas;
  document.querySelectorAll('.close-dialog').forEach(b=>b.onclick=()=>b.closest('dialog').close());
  document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
  $('auto-advance').onchange=()=>{state.autoAdvance=$('auto-advance').checked;cancelAdvance();persist();};
  $('export-progress').onclick=()=>{const blob=new Blob([JSON.stringify({...state,subject,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'});const a=el('a');a.href=URL.createObjectURL(blob);a.download=`${subject}-progress-${new Date().toISOString().slice(0,10)}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
  $('import-progress').onclick=()=>$('import-file').click();
  $('import-file').onchange=async()=>{const file=$('import-file').files[0];if(!file)return;try{if(file.size>2_000_000)throw Error('Файл слишком большой.');const raw=JSON.parse(await file.text());if((raw.subject&&raw.subject!==subject)||(isLinear&&raw.subject!=='linear'))throw Error('Это история другого предмета. Выбери соответствующий предмет перед загрузкой.');const incoming=validateState(raw,ids);const keepTheme=loadTheme(preferences,state.theme);state=incoming;theme(keepTheme);render();$('settings-dialog').close();toast('История загружена.');}catch(e){$('import-message').textContent=e.message;}$('import-file').value='';};
  $('reset-progress').onclick=()=>{if(!confirm('Удалить все попытки и подсказки в этом браузере?'))return;const keepTheme=state.theme;state=emptyState();state.theme=keepTheme;theme(keepTheme);render();$('settings-dialog').close();toast('Прогресс сброшен.');};
  render();
 }catch(e){$('task-heading').textContent='Не удалось открыть тренажёр';$('task-instruction').textContent=e.message+' Обнови страницу или проверь подключение.';console.error(e);}
}
init();
