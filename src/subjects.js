const querySubject=new URLSearchParams(location.search).get('subject');
export const subject=['matan','linear','physics'].includes(querySubject)?querySubject:'matan';
const requested=subject;
export const isLinear=requested==='linear';
export const isPhysics=requested==='physics';
export const subjectName=({matan:'Математический анализ',linear:'Линейная алгебра и аналитическая геометрия',physics:'Физика'})[requested];
export function subjectStorage(storage){
 if(requested==='matan')return storage;
 const key=requested+'-trainer:v1';
 return {getItem:()=>storage.getItem(key),setItem:(_,value)=>storage.setItem(key,value)};
}
export function setupSubjects(){
 const label=document.createElement('label');label.className='subject-picker';
 const text=document.createElement('span');text.textContent='ПРЕДМЕТ · 1 СЕМЕСТР 2025–26';
 const select=document.createElement('select');select.id='subject-select';select.setAttribute('aria-label','Выбрать предмет');
 for(const [value,title] of [['matan','Матан'],['linear','Линал и аналитическая геометрия'],['physics','Физика']]){const option=document.createElement('option');option.value=value;option.textContent=title;select.append(option);}
 select.value=requested;select.onchange=()=>{const url=new URL(location.href);if(select.value!=='matan')url.searchParams.set('subject',select.value);else url.searchParams.delete('subject');location.assign(url.href);};
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
 if(isPhysics){
  document.title='Предел. — физика в своём темпе';
  document.querySelector('.brand').href='?subject=physics';
  document.querySelector('.brand-mark').textContent='φ';
  document.querySelector('.sidebar-caption').textContent='ФИЗИКА · ЧАСТЬ 1';
  document.querySelector('meta[name="description"]').content='Физика, 1 семестр 2025–26: задачи, формулы, викторина и отдельный прогресс.';
  document.querySelector('.pdf-link').href='./sources/physics-topics.pdf';
  document.querySelector('.pdf-link').textContent='Открыть список формул для зачёта ↗';
  document.querySelector('.source-fidelity').textContent='Повторы списка и домашних работ объединены с ссылками на оба источника. Неоднозначные условия и модельные предположения отмечены; устные ответы проверяются самостоятельно.';
  document.querySelector('#show-tasks').textContent='Задачи и теория';
 }
}
