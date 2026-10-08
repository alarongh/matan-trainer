export const subject=new URLSearchParams(location.search).get('subject')==='linear'?'linear':'matan';
export const isLinear=subject==='linear';
export const subjectName=isLinear?'Линейная алгебра и аналитическая геометрия':'Математический анализ';
export function subjectStorage(storage){
 if(!isLinear)return storage;
 return {getItem:()=>storage.getItem('linear-trainer:v1'),setItem:(_,value)=>storage.setItem('linear-trainer:v1',value)};
}
export function setupSubjects(){
 const label=document.createElement('label');label.className='subject-picker';
 const text=document.createElement('span');text.textContent='ПРЕДМЕТ · 1 СЕМЕСТР 2025–26';
 const select=document.createElement('select');select.id='subject-select';select.setAttribute('aria-label','Выбрать предмет');
 for(const [value,title] of [['matan','Матан'],['linear','Линал и аналитическая геометрия']]){const option=document.createElement('option');option.value=value;option.textContent=title;select.append(option);}
 select.value=subject;select.onchange=()=>{const url=new URL(location.href);if(select.value==='linear')url.searchParams.set('subject','linear');else url.searchParams.delete('subject');location.assign(url.href);};
 label.append(text,select);document.querySelector('.brand').after(label);
 if(isLinear){
  document.title='Предел. — линал в своём темпе';
  document.querySelector('.brand').href='?subject=linear';
  document.querySelector('.sidebar-caption').textContent='ЛИНЕЙНАЯ АЛГЕБРА';
  document.querySelector('meta[name="description"]').content='Линейная алгебра и аналитическая геометрия, 1 семестр 2025–26. Задания билета, поэтапные разборы и отдельный прогресс.';
  document.querySelector('.pdf-link').href='./sources/linear-essentials.pdf';
  document.querySelector('.pdf-link').textContent='Открыть пособие с формулами ↗';
  document.querySelector('.source-fidelity').textContent='Исходная нумерация сохранена. Повторяющиеся условия имеют ссылки на оба источника, отличающиеся условия представлены отдельно. Авторские вопросы для проверки теории помечены отдельно.';
 }
}
