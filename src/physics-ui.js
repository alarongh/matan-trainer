export function physicsDiagram(kind){
 const ns='http://www.w3.org/2000/svg',box=document.createElement('div');box.className='physics-diagram';
 const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 360 260');svg.setAttribute('role','img');svg.setAttribute('aria-label','Цикл на диаграмме давления и объёма');
 const add=(tag,attributes)=>{const node=document.createElementNS(ns,tag);for(const [key,value] of Object.entries(attributes))node.setAttribute(key,value);svg.append(node);return node;};
 add('path',{d:'M45 20V225H340',fill:'none',stroke:'var(--muted)','stroke-width':1.5});
 const label=(x,y,text)=>{const node=add('text',{x,y,fill:'var(--ink)','font-size':14});node.textContent=text;};
 label(24,22,'p');label(335,245,'V');
 const path=kind==='rectangle'?'M100 185V60H290V185Z':'M100 185V60C145 125 215 165 290 185H100Z';
 add('path',{d:path,fill:'var(--accent-soft)',stroke:'var(--accent)','stroke-width':3});
 for(const [x,y,text] of [[100,185,'1'],[100,60,'2'],[290,kind==='rectangle'?60:185,'3'],...(kind==='rectangle'?[[290,185,'4']]:[])]){add('circle',{cx:x,cy:y,r:4,fill:'var(--accent)'});label(x+7,y-7,text);}
 label(64,125,'↑');label(180,kind==='rectangle'?50:107,'→');label(301,kind==='rectangle'?125:177,'↓');label(180,207,'←');
 const caption=document.createElement('p');caption.className='input-help';caption.textContent='Схема: двигатель обходит цикл по часовой стрелке; площадь внутри — работа за цикл. Масштаб условный.';
 box.append(svg,caption);return box;
}
