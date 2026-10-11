// Written proofs and drawings cannot receive automatic mathematical grading.
export function mountReview(container,task,item,{save,finish}){
 container.replaceChildren();
 const note=document.createElement('p');note.className='input-help';
 note.textContent='Реши на бумаге. Здесь можно оставить свои заметки; сайт их не оценивает.';
 const notes=document.createElement('textarea');notes.id='written-notes';notes.maxLength=2048;notes.rows=4;
 notes.placeholder='Мои наблюдения и места, которые нужно проверить';notes.value=item.draft||'';
 notes.oninput=()=>save(notes.value);
 container.append(note,notes);
 const complete=item.step>=task.stages.length;
 if(!complete){const p=document.createElement('p');p.className='input-help';p.textContent='После всех этапов появится список для сверки и отметка о работе с разбором.';container.append(p);return;}
 const checklist=document.createElement('div');checklist.className='written-checklist';
 const button=document.createElement('button');button.type='button';button.id='review-complete';button.className='primary-button';button.textContent='Сверил по разбору';button.disabled=true;
 for(const text of task.checklist){const label=document.createElement('label'),check=document.createElement('input'),span=document.createElement('span');check.type='checkbox';span.textContent=text;check.onchange=()=>{button.disabled=[...checklist.querySelectorAll('input')].some(i=>!i.checked);};label.append(check,span);checklist.append(label);}
 button.onclick=()=>finish(notes.value);
 container.append(checklist,button);
}

export function graphReference(plot){
 const ns='http://www.w3.org/2000/svg',box=document.createElement('div');box.className='graph-reference';
 const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 640 420');svg.setAttribute('role','img');svg.setAttribute('aria-label',plot.caption);
 const range=document.createElement('input');range.type='range';range.min='2';range.max='40';range.value=plot.polar?'12':'20';range.setAttribute('aria-label','Масштаб графика');
 const label=document.createElement('label');label.textContent='Масштаб ';label.append(range);
 const caption=document.createElement('p');caption.className='input-help';caption.textContent=plot.caption;
 function render(){
  svg.replaceChildren();const radius=Number(range.value),scale=280/radius;
  const line=(x1,y1,x2,y2)=>{const p=document.createElementNS(ns,'line');for(const [k,v] of Object.entries({x1,y1,x2,y2}))p.setAttribute(k,String(v));p.setAttribute('stroke','var(--border)');svg.append(p);};
  line(0,210,640,210);line(320,0,320,420);
  const tick=radius>16?5:radius>6?2:1;
  for(let a=-radius;a<=radius;a+=tick){const x=320+a*scale;line(x,205,x,215);const t=document.createElementNS(ns,'text');t.setAttribute('x',String(x+3));t.setAttribute('y','230');t.setAttribute('fill','var(--muted)');t.setAttribute('font-size','11');t.textContent=String(a);svg.append(t);}
  for(const segment of plot.segments){const p=document.createElementNS(ns,'polyline');p.setAttribute('points',segment.map(([x,y])=>`${320+x*scale},${210-y*scale}`).join(' '));p.setAttribute('fill','none');p.setAttribute('stroke','var(--accent)');p.setAttribute('stroke-width','2');svg.append(p);}
 }
 range.oninput=render;render();box.append(svg,label,caption);return box;
}
