from textbook_common import *

def graph_cards(b,section,i,page,f,points,lines,derivative=None,details='',variables=None):
 d2=derivative if derivative is not None else s.factor(s.diff(f,x,2))
 pts=[]
 for p in ([] if variables else points):
  py=f.subs(x,p)
  # RootOf and radicals are evaluated to eight decimal places for tractable answer entry.
  px=s.N(p,12);yy=s.N(py,12)
  pts.append('('+str(px)+';'+str(yy)+')')
 pointanswer=' | '.join(pts) or 'нет'
 if variables:pointanswer=points[0]
 pttex=r'\text{нет}' if not pts and not variables else r',\quad'.join('('+str(s.N(p,9))+';'+str(s.N(f.subs(x,p),9))+')' for p in points) if not variables else details
 task=add(b,section,str(i)+'-inflection',page,7,'Перегибы · исследование графика',r'y='+tex(f),pointanswer,
  four(r'f^{\prime\prime}(x_0)=0\text{ или не существует};\quad f^{\prime\prime}\text{ меняет знак, }f\text{ непрерывна в }x_0',
   r'f^{\prime\prime}='+tex(d2),details or r'\text{Проверяем допустимые корни и смену знака }f^{\prime\prime}.',
   r'\boxed{\begin{gathered}'+pttex+r'\end{gathered}}',
   ['Одного равенства f″=0 недостаточно.','Находим вторую производную внутри области определения.','Убираем точки вне области и разрывы; оставляем точки со сменой выпуклости.','Координаты приведены приближённо; вводи не менее 8 знаков после запятой.']),
  kind='points',variables=variables or [],instruction='Найди все точки перегиба. Формат (x;y) | (x;y), либо «нет». Приближённые координаты вводи с 8 знаками после запятой.',
  note='Адаптация задания «построить график»: здесь проверяются точки перегиба. Полное построение графика не оценивается.')
 record(b,task,'domain-filtered second-derivative roots and sign changes',pointanswer)
 task['sources']=[source(page,f'Задача {section}, пример {i}','textbook')]
 task['meta']=ref(section,i,page)+' · перегибы'
 fs=s.fraction(s.cancel(f))
 formula=r'k=\lim_{x\to\pm\infty}f(x)/x,\quad b=\lim_{x\to\pm\infty}(f(x)-kx)'
 task=add(b,section,str(i)+'-asymptotes',page,8,'Асимптоты · исследование графика',r'y='+tex(f),lines or 'нет',
  four(formula,r'\text{Проверяем границы области и поведение на бесконечности.}',
   details or r'\text{Нули знаменателя после сокращения дают полюса; целая часть даёт прямую на бесконечности.}',
   r'\boxed{\begin{gathered}'+line_tex(lines)+r'\end{gathered}}'),
  kind='lines',instruction='Введи все асимптоты: x=...; y=... . Если их нет, введи «нет».',
  note='Адаптация задания «построить график»: здесь проверяются асимптоты. Полное построение графика не оценивается.')
 record(b,task,'domain boundaries and directional asymptote coefficients',lines or 'none')
 task['sources']=[source(page,f'Задача {section}, пример {i}','textbook')]
 task['meta']=ref(section,i,page)+' · асимптоты'

def line_tex(lines):
 if not lines:return r'\text{нет}'
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,convert_xor
 result=[]
 for line in lines.split(';'):
  axis,value=line.strip().split('=')
  expr=parse_expr(value,local_dict={'x':x,'sqrt':s.sqrt,'pi':s.pi,'e':s.E,'arctan':s.atan,'exp':s.exp},transformations=standard_transformations+(convert_xor,))
  result.append(axis+'='+tex(expr))
 return r'\\'.join(result)

def populate(b):
 full=[]
 rational=[
 (1,1,0,-1,0,-1),(1,2,0,-2,0,-1),(1,1,0,-4,0,-4),(1,1,-3,2,-3,2),(1,1,-1,-2,-1,-2),
 (-1,0,0,0,2,1),(1,-2,0,0,-2,1),(-1,0,0,0,2,1),(1,-1,0,0,2,1),(1,3,3,1,-2,1),
 (-1,2,0,-6,0,-3),(-2,2,0,-6,0,-3),(2,-1,0,2,0,-2),(-3,2,0,-6,0,-3),(3,-2,0,2,0,-1),
 (2,-1,-1,6,1,-6),(-2,1,-1,-2,-1,-1),(3,3,-3,-6,-1,-2),(-3,-4,-4,24,1,-6),(1,1,1,-2,1,-2),
 (-1,2,2,-4,1,-2),(-1,-1,-3,-2,3,2),(2,-1,3,-2,-3,2),(2,1,-4,3,-4,3),(-2,-1,2,3,-2,-3),
 (-2,-4,-8,12,2,-3),(-2,-3,-12,-9,4,3),(-2,-2,10,-12,-5,6),(3,4,-4,-24,-1,-6),(1,3,15,18,5,6)]
 for i,(a,c,d,e,p,q) in enumerate(rational,1):
  original_num=a*x**3+c*x*x+d*x+e;original_den=x*x+p*x+q
  f=s.cancel(original_num/original_den);num,den=s.fraction(f)
  d2=s.factor(s.diff(f,x,2));pn,pd=s.fraction(d2)
  roots=s.Poly(pn,x).real_roots(multiple=False) if pn!=0 else []
  pts=[r for r,m in roots if m%2 and original_den.subs(x,r)!=0]
  poles=[r for r in s.solve(den,x) if r.is_real]
  quotient=s.div(num,den,x)[0]
  lines='; '.join(['x='+ans(r) for r in poles]+['y='+ans(quotient)])
  details=r'f(x)='+tex(quotient)+r'+\frac{'+tex(s.div(num,den,x)[1])+'}{'+tex(den)+r'},\quad f^{\prime\prime}='+tex(d2)
  graph_cards(b,20,i,48 if i<=9 else 49,f,pts,lines,d2,details)
  for task in b.tasks[-2:]:task['prompt']=r'y=\frac{'+tex(original_num)+'}{'+tex(original_den)+'}'
  zeros=[r for r,m in s.Poly(original_num,x).real_roots(multiple=False) if original_den.subs(x,r)!=0]
  ztex=r'x\in\{'+','.join(tex(s.N(r,9)) for r in zeros)+r'\}' if zeros else r'\varnothing'
  full.append((20,i,48 if i<=9 else 49,f,pts,lines,d2,b.tasks[-1]['prompt'],{'excluded':s.solve(original_den,x),'zero_equation':ztex}))
 fractional(b,full)
 elementary(b,full)
 from textbook_full_graphs import full_graph
 for section,i,page,f,pts,lines,d2,prompt,kwargs in full:
  full_graph(b,section,i,page,f,pts,lines,d2,prompt,**kwargs)
  if i%5==0:print("full graph",section,i,flush=True)

def fractional(b,full):
 # (alpha,beta,a,b,c), as printed. The even roots use their natural real domains.
 rows=[(3,2,1,0,1),(3,2,9,1,-1),(3,2,1,1,-3),(5,4,4,-2,1),(5,4,3,0,-2),
 (4,3,1,2,-1),(4,3,4,0,2),(3,4,2,0,-1),(3,2,4,-2,2),(3,2,9,-1,-2),
 (4,3,4,1,2),(4,3,1,0,-1),(6,5,4,0,1),(2,1,9,-2,-1),(2,1,4,1,3),(4,3,1,0,1),
 (4,3,9,0,-1),(2,1,1,0,2),(6,5,1,-1,-2),(6,5,9,0,-1),
 (3,1,-2,1,-1),(3,-1,-4,1,1),(3,2,-1,1,-2),(3,-2,5,-1,2),(5,1,-1,2,-1),
 (5,-1,2,-3,2),(5,2,-1,-1,3),(5,-2,-3,0,1),(3,-3,4,0,-2),(5,3,-2,0,1)]
 for i,(alpha,beta,a,bb,c) in enumerate(rows,1):
  a=s.Integer(a);c=s.Integer(c);bb=s.Integer(bb);p=R(beta,alpha)
  if i<=10:
   # Absolute value is equivalent for even beta; odd beta and even alpha require x²≥a.
   f=c*(s.Abs(x*x-a)**p if beta%2==0 else (x*x-a)**p)+bb
   d2=2*c*p*(x*x-a)**(p-2)*((2*p-1)*x*x-a)
   pts=[-s.sqrt(a/(2*p-1)),s.sqrt(a/(2*p-1))] if 2*p-1>0 else []
   lines=''
   detail=r'f^{\prime\prime}=\frac{2c\beta}{\alpha}(x^2-a)^{\beta/\alpha-2}\left((2\beta/\alpha-1)x^2-a\right)'
  elif i<=20:
   f=c*s.Abs(x*x-a)**p+bb;d2=2*c*p*s.Abs(x*x-a)**(p-2)*((2*p-1)*x*x-a)
   pts=[-s.sqrt(a/(2*p-1)),s.sqrt(a/(2*p-1))] if 2*p-1>0 else []
   lines='y='+ans(c*x+bb)+'; y='+ans(-c*x+bb) if p==R(1,2) else ''
   detail=r'f^{\prime\prime}=2cp|x^2-a|^{p-2}((2p-1)x^2-a),\quad p=\beta/\alpha'
  else:
   p=R(2,alpha);f=c*x**beta*s.Abs(x-a)**p+bb
   poly=s.expand(beta*(beta-1)*(x-a)**2+2*beta*p*x*(x-a)+p*(p-1)*x*x)
   d2=c*x**(beta-2)*s.Abs(x-a)**(p-2)*poly
   roots=s.Poly(poly,x).real_roots(multiple=False)
   pts=[r for r,m in roots if m%2 and r not in (a,0)]
   if beta>=3 and beta%2:pts.append(s.Integer(0))
   lines='x=0; y='+ans(bb) if beta<0 else ''
   detail=r'f^{\prime\prime}=c x^{\beta-2}|x-a|^{p-2}P(x),\quad P(x)='+tex(poly)+r',\ p=2/\alpha'
  graph_cards(b,21,i,50,f,pts,lines,d2,detail)
  # Preserve the radical form of the printed function rather than silently replacing it by Abs.
  original=c*s.Pow((x*x-a)**beta,R(1,alpha),evaluate=False)+bb if i<=10 else c*s.Pow(s.Abs(x*x-a)**beta,R(1,alpha),evaluate=False)+bb if i<=20 else c*x**beta*s.Pow((x-a)**2,R(1,alpha),evaluate=False)+bb
  for task in b.tasks[-2:]:task['prompt']='y='+tex(original)
  if i<=20:
   d1=2*c*p*x*s.sign(x*x-a)*s.Abs(x*x-a)**(p-1) if not i in (6,7) else 2*c*p*x*(x*x-a)**(p-1)
   crit=[s.Integer(0),-s.sqrt(a),s.sqrt(a)] if a>=0 else [s.Integer(0)]
   exclusions=[]
  else:
   d1=c*x**(beta-1)*s.Abs(x-a)**(p-1)*(beta*s.Abs(x-a)+p*x*s.sign(x-a))
   crit=[s.Integer(0),a,s.cancel(beta*a/(beta+p))]
   exclusions=[s.Integer(0)] if beta<0 else []
  if i<=20:
   target=-bb/c;zeros=[]
   if target>=0:
    power=target**(1/p)
    squared=[a+power] if i in (6,7) else [a+power,a-power]
    zeros=list(set(q for val in squared if val>=0 for q in [-s.sqrt(val),s.sqrt(val)]))
  else:
   poly=c**alpha*x**(beta*alpha)*(x-a)**2-(-bb)**alpha if beta>=0 else c**alpha*(x-a)**2-(-bb)**alpha*x**(-beta*alpha)
   zeros=[r for r,m in s.Poly(poly,x).real_roots(multiple=False) if not (beta<0 and r==0)]
  ztex=r'x\in\{'+','.join(tex(s.N(r,9)) for r in sorted(zeros,key=float))+r'\}' if zeros else r'\varnothing'
  full.append((21,i,50,f,pts,lines,d2,b.tasks[-1]['prompt'],{'critical':crit,'excluded':exclusions,'d1':d1,'zero_equation':ztex}))

def elementary(b,full):
 E=s.exp;L=s.log;S=s.sin;C=s.cos;P=s.pi
 rows=[
 ((2*x+3)*E(-2*x-2),[-R(1,2)],'y=0'),
 (s.Abs(x)**R(2,3)*E(-x/3),[2-s.sqrt(6),2+s.sqrt(6)],'y=0'),
 (x*E(-x*x),[-s.sqrt(R(3,2)),0,s.sqrt(R(3,2))],'y=0'),
 (s.sqrt(x**3*L(x)),[E((-2+s.sqrt(7))/3)],''),
 (x/L(x),[E(2)],'x=1'),(x*E(-x),[2],'y=0'),
 (E(1/x)-x,[-R(1,2)],'x=0; y=-x+1'),(x*x-L(s.Abs(x)),[],'x=0'),
 (E(1/(x*x-4*x+4)),[],'x=2; y=1'),((1+x)*E(1/x),[-R(1,3)],'x=0; y=x+2'),
 (E(-x)*S(x),[],'y=0'),(3*L(x/(x-3))-1,[],'x=0; x=3; y=-1'),
 (E(2-x)/(2-x),[],'x=2; y=0'),(3-3*L(x/(x+4)),[],'x=0; x=-4; y=3'),
 (x*E(1/(x-1)),[R(2,3)],'x=1; y=x+1'),(E(x)*C(x),[],'y=0'),
 (E(2*x+2)/(2*x+2),[],'x=-1; y=0'),(L(x)/s.sqrt(x),[E(R(8,3))],'x=0; y=0'),
 ((3-x)*E(x-2),[1],'y=0'),(L((1+x)/(1-x)),[0],'x=-1; x=1'),
 (E(1/x**2),[],'x=0; y=1'),(x*E(1/(2-x)),[R(8,3)],'x=2; y=x-1'),
 ((2*x+5)*E(-2*x-4),[-R(3,2)],'y=0'),(L(1-4/x)-3,[],'x=0; x=4; y=-3'),
 (4*L(x/(x+2))+1,[],'x=0; x=-2; y=1'),(x*(2-L(x))**2,[s.E],''),
 (x**3*E(-x),[0,3-s.sqrt(3),3+s.sqrt(3)],'y=0'),
 (s.sqrt(x)/L(x),[E(-2*s.sqrt(2)),E(2*s.sqrt(2))],'x=1'),
 (2*L((x+3)/x)-3,[],'x=0; x=-3; y=-3'),(E(x-3)/(2*x+7),[],'x=-7/2; y=0')]
 for i,(f,pts,lines) in enumerate(rows,1):
  variables=None;detail=''
  if i in (11,16):
   variables=['k']
   pts=['(pi/2+k*pi;(-1)^k*exp(-pi/2-k*pi))' if i==11 else '(k*pi;(-1)^k*exp(k*pi))']
   detail=r'( \pi/2+k\pi;\ (-1)^k e^{-\pi/2-k\pi}),\ k\in\mathbb Z' if i==11 else r'(k\pi;\ (-1)^k e^{k\pi}),\ k\in\mathbb Z'
  # Avoid distributional derivatives of |x| in ordinary graph analysis.
  d2=s.exp(-x/3)*s.Abs(x)**R(2,3)*(x*x-4*x-2)/(9*x*x) if i==2 else 2+1/x**2 if i==8 else s.factor(s.diff(f,x,2))
  graph_cards(b,22,i,50 if i<=2 else 51 if i<=28 else 52,f,pts,lines,d2,detail,variables)
  if variables:
   b.tasks[-2]['instruction']='Введи семейство точек через целое k. Формат (x(k);y(k)); k∈ℤ.'
  if i==2:
   for task in b.tasks[-2:]:task['prompt']=r'y=\sqrt[3]{x^2 e^{-x}}'
  crits={1:[-1],2:[0,2],3:[-1/s.sqrt(2),1/s.sqrt(2)],4:[],5:[s.E],6:[1],7:[],8:[-1/s.sqrt(2),1/s.sqrt(2)],9:[],
   10:[(1-s.sqrt(5))/2,(1+s.sqrt(5))/2],11:[],12:[],13:[1],14:[],15:[(3-s.sqrt(5))/2,(3+s.sqrt(5))/2],16:[],17:[-R(1,2)],18:[s.exp(2)],19:[2],20:[],21:[],
   22:[],23:[-2],24:[],25:[],26:[s.E**2,s.E**4],27:[0,3],28:[s.E**2],29:[],30:[-R(5,2)]}
  excluded={2:[0],4:[1],5:[0,1],7:[0],8:[0],9:[2],10:[0],12:[0,3],13:[2],14:[-4,0],15:[1],17:[-1],18:[0],
   20:[-1,1],21:[0],22:[2],24:[0,4],25:[-2,0],26:[0],28:[0,1],29:[-3,0],30:[-R(7,2)]}.get(i,[])
  zeros={1:'-3/2',2:'0',3:'0',4:'1',6:'0',8:None,10:'-1',11:'k*pi',12:'3*exp(1/3)/(exp(1/3)-1)',14:'-4*exp(1)/(exp(1)-1)',15:'0',16:'pi/2+k*pi',18:'1',19:'3',20:'0',22:'0',23:'-5/2',24:'4/(1-exp(3))',25:'2/(exp(-1/4)-1)',26:'exp(2)',27:'0',29:'3/(exp(3/2)-1)'}
  zerotex=r'\varnothing'
  if i==7:zerotex=r'x\approx1.763222834\quad (x\ln x=1,\ x>0)'
  elif i==8:zerotex=r'\varnothing\quad (x^2-\ln|x|>0)'
  elif i in zeros:
   from sympy.parsing.sympy_parser import parse_expr,standard_transformations,convert_xor
   root=parse_expr(zeros[i],local_dict={'exp':s.exp,'k':s.Symbol('k',integer=True),'pi':s.pi},transformations=standard_transformations+(convert_xor,))
   zerotex='x='+tex(root)+(r',\quad k\in\mathbb Z' if i in (11,16) else '')
  full.append((22,i,50 if i<=2 else 51 if i<=28 else 52,f,pts,lines,d2,b.tasks[-1]['prompt'],{'critical':list(map(s.sympify,crits[i])),'excluded':list(map(s.sympify,excluded)),'zero_equation':zerotex}))
