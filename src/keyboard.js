// Keep the native input as the single source of truth, including its selection.
export function mountKeyboard(root,input){
 const panel=document.createElement('div');panel.className='keyboard-panel';panel.id='math-keys';
 const header=document.createElement('div');header.className='keyboard-heading';
 const toggle=document.createElement('button');toggle.type='button';toggle.className='text-button';toggle.id='toggle-keyboard';toggle.setAttribute('aria-controls',panel.id);toggle.setAttribute('aria-expanded','true');
 const title=document.createElement('span');title.textContent='Математическая клавиатура';
 const indicator=document.createElement('span');indicator.textContent='Скрыть ↑';toggle.append(title,indicator);header.append(toggle);root.append(header,panel);
 toggle.onclick=()=>{panel.hidden=!panel.hidden;toggle.setAttribute('aria-expanded',String(!panel.hidden));indicator.textContent=panel.hidden?'Показать ↓':'Скрыть ↑';};
 const finePointer=()=>window.matchMedia('(pointer:fine)').matches;
 function replace(text,start,end,caret){
  if(input.value.length-(end-start)+text.length>input.maxLength)return;
  input.setRangeText(text,start,end,'end');
  input.setSelectionRange(caret,caret);
  input.dispatchEvent(new Event('input',{bubbles:true}));
 }
 function edit(key){
  const start=input.selectionStart??input.value.length,end=input.selectionEnd??start;
  const selected=input.value.slice(start,end);
  if(finePointer())input.focus({preventScroll:true});
  if(key.action==='left'||key.action==='right'){
   const caret=key.action==='left'?Math.max(0,start-(start===end?1:0)):Math.min(input.value.length,end+(start===end?1:0));input.setSelectionRange(caret,caret);return;
  }
  if(key.action==='clear'){replace('',0,input.value.length,0);return;}
  if(key.action==='delete'){
   const from=start===end?Math.max(0,start-1):start;replace('',from,end,from);return;
  }
  if(key.text===')'&&!selected&&input.value[start]===')'){input.setSelectionRange(start+1,start+1);return;}
  const text=key.prefix!==undefined?key.prefix+selected+key.suffix:key.text;
  const caret=key.prefix!==undefined&&!selected?start+key.prefix.length:start+text.length;
  replace(text,start,end,caret);
 }
 function button(key){
  const b=document.createElement('button');b.type='button';b.className='math-key'+(key.style?' '+key.style:'');b.textContent=key.label;b.dataset.key=key.id||key.text||key.action;
  b.title=key.hint||key.label;b.setAttribute('aria-label',key.hint||key.label);
  if(key.action==='delete'){
   b.textContent='';const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg'),path=document.createElementNS(ns,'path');
   svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('width','21');svg.setAttribute('height','21');svg.setAttribute('aria-hidden','true');
   svg.setAttribute('fill','none');svg.setAttribute('stroke','currentColor');svg.setAttribute('stroke-width','1.5');svg.setAttribute('stroke-linecap','round');svg.setAttribute('stroke-linejoin','round');
   path.setAttribute('d','M9 5H21V19H9L3 12Z M12 9L18 15 M18 9L12 15');svg.append(path);b.append(svg);
  }
  // Pointer keys must not steal the input's selection or summon a phone keyboard.
  b.addEventListener('pointerdown',e=>e.preventDefault());
  b.onclick=()=>edit(key);return b;
 }
 function grid(cls,keys,parent=panel){const g=document.createElement('div');g.className=cls;for(const key of keys)g.append(button(key));parent.append(g);}
 grid('keyboard-shortcuts',[
  {id:'exponential',label:'eˣ',prefix:'e^(',suffix:')',hint:'Экспонента: e в степени'},
  {id:'root',label:'√',prefix:'sqrt(',suffix:')',hint:'Квадратный корень'},
  {id:'power',label:'xʸ',prefix:'^(',suffix:')',hint:'Степень'},
  {text:'/',label:'a/b',hint:'Дробь: числитель / знаменатель'},
  {text:'π',label:'π',hint:'Число пи'},
  {text:'∞',label:'∞',hint:'Бесконечность'}
 ]);
 grid('keyboard-digits',[
  ...['7','8','9','(',')','4','5','6','*','/','1','2','3','+','-','0',',','e'].map(text=>({text,label:({'*':'×','/':'÷','-':'−'})[text]||text,hint:({'*':'Умножение','/':'Деление','-':'Минус','(':'Открывающая скобка',')':'Закрывающая скобка',',':'Десятичная запятая',e:'Число e'})[text]})),
  {action:'left',label:'←',hint:'Курсор влево'},{action:'right',label:'→',hint:'Курсор вправо'}
 ]);
 const more=document.createElement('details');more.className='keyboard-more';const summary=document.createElement('summary');summary.textContent='Ещё функции';more.append(summary);
 grid('keyboard-functions',['sin','cos','tan','arctan','arccot','arcsin','arccos','ln','exp','abs'].map(name=>({id:name,label:name,prefix:name+'(',suffix:')',hint:name+' — вставить функцию'})),more);panel.append(more);
 grid('keyboard-functions',['x','y','t','a','l','k','c','=',';','|','нет'].map(text=>({text,label:text})),more);
 const actions=document.createElement('div');actions.className='keyboard-actions';
 actions.append(button({action:'clear',label:'Очистить'}),button({action:'delete',label:'⌫',hint:'Удалить символ или выделение'}));
 const check=document.createElement('button');check.type='submit';check.className='primary-button';check.id='keyboard-check';check.textContent='Проверить ↵';actions.append(check);panel.append(actions);
 return {setInput(next){input=next;}};
}
