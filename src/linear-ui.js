export const linearFormulas=[
 ['Матрицы','Порядок множителей имеет значение.',String.raw`A^{-1}=\frac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix},\quad AX=B\Rightarrow X=A^{-1}B,\quad XA=B\Rightarrow X=BA^{-1}`],
 ['Определители и ранг','Множитель одной строки выносится один раз; множитель всей матрицы - n раз.',String.raw`A_{ij}=(-1)^{i+j}M_{ij},\quad\det A=\sum_j a_{ij}A_{ij},\quad\det(kA)=k^n\det A`],
 ['СЛАУ','При r=n решение единственное, при r<n есть n-r свободных параметров.',String.raw`\operatorname{rank}A=\operatorname{rank}(A|b)\iff\text{совместна},\quad X=X_p+\sum c_jv_j`],
 ['Векторы','Вычитаем начало из конца. Для угла при C используем CA и CB.',String.raw`\overrightarrow{AB}=B-A,\quad a\cdot b=\sum a_ib_i,\quad\cos\varphi=\frac{a\cdot b}{|a||b|}`],
 ['Площадь, объём, компланарность','Объём и площадь неотрицательны.',String.raw`S_\triangle=\frac12|a\times b|,\quad V_{\rm тетр}=\frac16|(a\times b)\cdot c|,\quad(a,b,c)=0\iff\text{компланарны}`],
 ['Прямая и плоскость','Нормаль плоскости и направление перпендикулярной ей прямой коллинеарны.',String.raw`r=r_0+ts,\quad n\cdot(r-r_0)=0,\quad d(P,\alpha)=\frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}`],
 ['Проекции и симметрия','Для прямой сначала находим параметр проекции.',String.raw`t_0=\frac{(P-Q)\cdot s}{s\cdot s},\quad H=Q+t_0s,\quad P^*=2H-P`],
 ['Эллипс и гипербола','Оси и центр могут быть сдвинуты; a - большая полуось эллипса или действительная полуось гиперболы.',String.raw`\frac{u^2}{a^2}+\frac{v^2}{b^2}=1:\ c^2=a^2-b^2;\quad\frac{u^2}{a^2}-\frac{v^2}{b^2}=1:\ c^2=a^2+b^2;\quad\varepsilon=c/a`],
 ['Парабола','Знак f задаёт направление от вершины к фокусу.',String.raw`v^2=4fu,\quad F=(f,0),\quad d:u=-f`],
 ['Комплексные числа','Главное значение аргумента берём в (-π;π]. Для нуля аргумент не определён.',String.raw`i^2=-1,\quad\frac1{a+bi}=\frac{a-bi}{a^2+b^2},\quad z=r(\cos\varphi+i\sin\varphi)=re^{i\varphi}`],
 ['Муавр и корни','Ненулевое число имеет n различных корней n-й степени.',String.raw`z^n=r^ne^{in\varphi},\quad w_k=\sqrt[n]r\,e^{i(\varphi+2\pi k)/n},\quad k=0,\ldots,n-1`],
 ['Практика и многочлены','В моменте силы порядок: радиус-вектор × сила.',String.raw`W=F\cdot s,\quad M_O=\overrightarrow{OP}\times F,\quad P(x)=(x-a)Q(x)+P(a)`]
];
const hints={matrix:'1 2; 3 4',complex:'2-3i', 'complex-set':'-2+3i; -2-3i',vector:'(x;y;z)',equation:'2x-y+4z+3=0',line3:'x=1+2t; y=3-t; z=4t',affine:'(11-14t;6-4t;t)','system-point':'(x₁;x₂;x₃)'};
export function linearInputHelp(task,input,help){
 input.placeholder=hints[task.kind]||'Только итоговый ответ';
 const explanation={matrix:'Матрица: элементы строки через пробел, строки через ;. Дробь 1/2 и десятичные записи 0.5 или 0,5 равнозначны.',complex:'Мнимая единица i: 2-3i. Можно вводить дроби, корни и произведения.', 'complex-set':'Все корни через ; в любом порядке: -2+3i; -2-3i. Повторять один корень несколько раз не нужно.',vector:'Координаты в указанном порядке через ; в скобках: (1;2;3).',equation:'Уравнение со знаком =. Любая запись с ненулевым общим множителем принимается.',line3:'Параметрические уравнения через ; или каноническая цепочка дробей. Параметр t.',affine:'Три координаты через ;, параметр t. Можно выбрать другую равносильную параметризацию.', 'system-point':'Подходит любое частное решение исходной системы.'};
 if(help)help.textContent=explanation[task.kind]||'Введи итоговый ответ. Дроби: 2/3, корни: sqrt(2), углы в радианах: pi/2.';
}
export function addLinearKeys(root,setInput){
 const row=document.createElement('div');row.className='linear-keys';row.setAttribute('role','group');row.setAttribute('aria-label','Символы для линейной алгебры');
 for(const text of ['i','x','y','z','t','=',';',' ']){
  const b=document.createElement('button');b.type='button';b.className='math-key';b.textContent=text===' '?'Пробел':text;b.dataset.linearKey=text;
  b.onpointerdown=e=>e.preventDefault();b.onclick=()=>{const input=setInput();if(!input)return;const start=input.selectionStart??input.value.length,end=input.selectionEnd??start;if(input.value.length-end+start+text.length>input.maxLength)return;input.setRangeText(text,start,end,'end');input.dispatchEvent(new Event('input',{bubbles:true}));if(matchMedia('(pointer:fine)').matches)input.focus({preventScroll:true});};row.append(b);
 }
 root.querySelector('.keyboard-panel').prepend(row);
}
export function renderGraph(data){
 const ns='http://www.w3.org/2000/svg',wrap=document.createElement('figure');wrap.className='solution-graph';
 const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 400 300');svg.setAttribute('role','img');svg.setAttribute('aria-label',data.type==='points'?'Комплексная плоскость с отмеченными решениями':'Схематический график кривой');
 let extent=2,lines=[],points=data.points||[],labels=data.labels||[],h=data.h||0,k=data.k||0;
 if(data.type==='ellipse'){
  extent=Math.max(Math.abs(h)+data.a+data.b,Math.abs(k)+data.a+data.b)*1.1;
  lines.push(Array.from({length:161},(_,i)=>{const angle=i*Math.PI/80;return data.vertical?[h+data.b*Math.sin(angle),k+data.a*Math.cos(angle)]:[h+data.a*Math.cos(angle),k+data.b*Math.sin(angle)];}));
 }else if(data.type==='hyperbola'){
  extent=Math.max(Math.abs(h),Math.abs(k))+Math.max(data.a,data.b)*3;
  for(const sign of [-1,1])lines.push(Array.from({length:161},(_,i)=>{const q=(i-80)/50,U=sign*data.a*Math.cosh(q),V=data.b*Math.sinh(q);return data.vertical?[h+V,k+U]:[h+U,k+V];}));
 }else if(data.type==='parabola'){
  extent=Math.max(Math.abs(h),Math.abs(k))+Math.max(3,Math.abs(data.a));
  lines.push(Array.from({length:161},(_,i)=>{const v=(i-80)*extent/80,u=v*v/data.a;return data.vertical?[h+v,k+u]:[h+u,k+v];}));
 }
 if(data.type!=='points'){
  points=[[h,k]];labels=[data.type==='parabola'?'V':'O'];
  const c=data.type==='ellipse'?Math.sqrt(Math.abs(data.a**2-data.b**2)):data.type==='hyperbola'?Math.hypot(data.a,data.b):data.a/4;
  const offsets=data.type==='parabola'?[c]:[-c,c];for(const offset of offsets){points.push(data.vertical?[h,k+offset]:[h+offset,k]);labels.push('F'+(offsets.length>1?(offset<0?'1':'2'):''));}
 }
 extent=Math.max(extent,...points.flat().map(v=>Math.abs(v)*1.3));
 const scale=120/extent,X=v=>200+v*scale,Y=v=>150-v*scale;
 const draw=(tag,attrs,text)=>{const node=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))node.setAttribute(k,String(v));if(text)node.textContent=text;svg.append(node);return node;};
 draw('rect',{x:0,y:0,width:400,height:300,rx:12,fill:'var(--frame)'});
 for(const v of [-.8,-.4,0,.4,.8]){
  draw('line',{x1:X(v*extent),x2:X(v*extent),y1:24,y2:276,stroke:'var(--border)'});
  draw('line',{x1:24,x2:376,y1:Y(v*extent),y2:Y(v*extent),stroke:'var(--border)'});
 }
 draw('line',{x1:24,x2:376,y1:150,y2:150,stroke:'var(--muted)'});draw('line',{x1:200,x2:200,y1:24,y2:276,stroke:'var(--muted)'});
 for(const points of lines)draw('polyline',{points:points.map(([x,y])=>`${X(x)},${Y(y)}`).join(' '),fill:'none',stroke:'var(--accent)','stroke-width':2});
 points.forEach(([x,y],i)=>{draw('circle',{cx:X(x),cy:Y(y),r:4,fill:'var(--accent)'});draw('text',{x:X(x)+7,y:Y(y)-8,fill:'var(--ink)','font-size':11},labels[i]||'');});
 draw('text',{x:350,y:143,fill:'var(--muted)','font-size':10},data.axes?.[0]||'x');draw('text',{x:208,y:25,fill:'var(--muted)','font-size':10},data.axes?.[1]||'y');draw('text',{x:205,y:165,fill:'var(--muted)','font-size':10},'0');
 wrap.append(svg);const caption=document.createElement('figcaption');caption.textContent='Схема с одинаковым масштабом по осям. Точные координаты и уравнения указаны выше.';wrap.append(caption);return wrap;
}
