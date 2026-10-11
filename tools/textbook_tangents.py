from textbook_common import *

def line_pair(px,py,k):
 if k in (s.oo,-s.oo):return 'x='+ans(px),'y='+ans(py)
 if k==0:return 'y='+ans(py),'x='+ans(px)
 return 'y='+ans(s.expand(k*(x-px)+py)),'y='+ans(s.expand(-(x-px)/k+py))

def populate(b):
 rows=[
 (x**4-6*x*x+8*x,[(0,0),(1,3)],[8,0]),
 (s.asin(2*x-3),[(R(3,2),0),(2,s.pi/2)],[2,s.oo]),
 ((5*x-3)**R(1,3),[(-1,-2),(R(3,5),0)],[R(5,12),s.oo]),
 ((x*(x-2)**2)**R(1,3),[(1,1),(0,0)],[-R(1,3),s.oo]),
 ((1-x*x)**R(1,3),[(3,-2),(1,0)],[-R(1,2),s.oo]),
 (s.sqrt(x*x-2*x),[(-1,s.sqrt(3)),(2,0)],[-2/s.sqrt(3),s.oo]),
 (s.sqrt(s.sin(x)),[(s.pi/6,1/s.sqrt(2)),(s.pi,0)],[s.sqrt(6)/4,s.oo]),
 (x*s.exp(1/(x-2)),[(3,3*s.E),(s.pi,0)],[None,None]),
 (x*s.log(x),[(1,0),(0,0)],[1,s.oo]),
 (x*x*s.log(x),[(1,0),(0,0)],[1,0]),
 (x**x,[(1,1),(0,1)],[1,s.oo]),
 (s.sin(x)/x,[(s.pi/4,2*s.sqrt(2)/s.pi),(0,1)],[2*s.sqrt(2)*(s.pi-4)/s.pi**2,0])]
 for i,(f,points,slopes) in enumerate(rows,1):
  if i==8:
   task=b.invalid('textbook-14-8',6,'Проверка точки касания',r'y=xe^{1/(x-2)},\quad M_1(3;3e),\ M_2(\pi;0)',
    'Требуются касательная и нормаль в обеих напечатанных точках.',
    'Точка M₂(π;0) не лежит на графике: π·exp(1/(π−2))>0. Вторую пару прямых по этому условию составить нельзя.',33,ref(14,i,33),
    r'f(\pi)=\pi e^{1/(\pi-2)}>0')
   task['sources']=[source(33,'Задача 14, пример 8','textbook')]
   continue
  fs=[];details=[]
  d=s.diff(f,x)
  for j,((px,py),k) in enumerate(zip(points,slopes),1):
   if px!=0 or i<9:
    value=f.subs(x,px)
    # Cube-root evaluations use the real source branch.
    if i in (3,5):value=s.real_root((5*x-3 if i==3 else 1-x*x).subs(x,px),3)
    assert s.simplify(value-py)==0,(i,j,value,py)
   a,c=line_pair(px,py,k);fs.extend([field(f't{j}',f'Касательная в M{j}',a,'lines'),field(f'n{j}',f'Нормаль в M{j}',c,'lines')])
   details.append(r'M_'+str(j)+'('+tex(px)+';'+tex(py)+r'),\quad k='+tex(k))
  conditions=r',\quad '+r',\ '.join(r'M_'+str(j)+r'('+tex(px)+';'+tex(py)+')' for j,(px,py) in enumerate(points,1))
  add_card(b,i,33,r'y='+tex(f)+conditions,fs,r'y^\prime='+tex(d),details,note='В M₂ при x→0+ используется непрерывное продолжение функции.' if i>=9 else '')
  record(b,b.tasks[-1],'source point membership and tangent slopes (including one-sided singular points)',str(slopes))
 # Implicit curves, including all branches at the node in item 15.
 implicit=[
 (13,x*x/16+y*y/9-1,[(2,3*s.sqrt(3)/2),(4,0)],[-s.sqrt(3)/4,s.oo]),
 (14,x*x/16-y*y/9-1,[(5,R(9,4)),(4,0)],[R(5,4),s.oo]),
 (15,3*y*y-x*(x-3)**2,[(3,0),(0,0)],[None,s.oo]),
 (16,2*y*s.log(y)-x,[(0,1),(-2/s.E,1/s.E)],[R(1,2),s.oo]),
 (17,x**R(2,3)+y**R(2,3)-1,[(R(1,8),3*s.sqrt(3)/8),(0,1)],[-s.sqrt(3),s.oo]),
 (18,(x*x+y*y)**2-2*(x*x-y*y),[(s.sqrt(3)/2,R(1,2)),(s.sqrt(2),0)],[0,s.oo])]
 for i,F,points,slopes in implicit:
  fs=[];details=[];d=s.factor(-s.diff(F,x)/s.diff(F,y))
  for j,((px,py),k) in enumerate(zip(points,slopes),1):
   assert s.simplify(F.subs({x:px,y:py}))==0
   if i==15 and j==1:
    a='y=x-3; y=-x+3';c='y=-x+3; y=x-3'
    details.append(r'x=3+h:\quad3y^2=(3+h)h^2,\quad y/h\to\pm1')
   else:
    a,c=line_pair(px,py,k);details.append(r'M_'+str(j)+'('+tex(px)+';'+tex(py)+r'),\quad k='+tex(k))
   fs.extend([field(f't{j}',f'Касательные в M{j}',a,'lines'),field(f'n{j}',f'Нормали в M{j}',c,'lines')])
  conditions=r',\quad '+r',\ '.join(r'M_'+str(j)+r'('+tex(px)+';'+tex(py)+')' for j,(px,py) in enumerate(points,1))
  add_card(b,i,34,tex(F)+'=0'+conditions,fs,r'y^\prime='+tex(d),details)
  record(b,b.tasks[-1],'implicit point membership; branch slopes at singularities',str(slopes))
 param=[
 (19,2*t-t*t,3*t-t**3,[0,-1]),
 (20,t*s.exp(3*t),t*s.exp(-2*t),[0,-R(1,3)]),
 (21,t-s.sin(t),1-s.cos(t),[s.pi/6,0]),
 (22,s.cos(t)**3,s.sin(t)**3,[s.pi/4,s.pi/2]),
 (23,(1+t)/t**3,3/(2*t*t)+1/(2*t),[1,-R(3,2)]),
 (24,s.log(1+t*t),t-s.atan(t),[2,0]),
 (25,s.sqrt(1-t*t),s.asin(t),[-1,0])]
 # Polar equations become x=r*cos(phi), y=r*sin(phi).
 for i,r,ts in [(26,t,[s.pi/2,0]),(27,s.cos(2*t),[s.pi/4,0]),(28,s.sqrt(s.cos(t)),[s.pi/3,0]),(29,1-s.cos(t),[s.pi/3,s.pi]),(30,1+s.cos(t),[s.pi/3,0])]:
  param.append((i,r*s.cos(t),r*s.sin(t),ts))
 for i,X,Y,ts in param:
  dx=s.diff(X,t);dy=s.diff(Y,t);d=s.factor(dy/dx);fs=[];details=[]
  for j,p in enumerate(ts,1):
   px=s.simplify(X.subs(t,p));py=s.simplify(Y.subs(t,p))
   if i==25 and p==-1:k=0
   else:
    k=s.simplify(d.subs(t,p))
    if k.has(s.nan,s.zoo):
     k=s.limit(d,t,p,dir='+')
   a,c=line_pair(px,py,k);fs.extend([field(f't{j}',f'Касательная при t{j}',a,'lines'),field(f'n{j}',f'Нормаль при t{j}',c,'lines')])
   details.append(r't_'+str(j)+'='+tex(p)+r',\quad M('+tex(px)+';'+tex(py)+r'),\quad k='+tex(k))
  conditions=r',\quad t_1='+tex(ts[0])+r',\ t_2='+tex(ts[1])
  add_card(b,i,34 if i<=26 else 35,r'\begin{cases}x='+tex(X)+r'\\y='+tex(Y)+r'\end{cases}'+conditions,fs,
   r'x_t^\prime='+tex(dx)+r',\quad y_t^\prime='+tex(dy),details,
   note='Для полярной кривой записана эквивалентная параметризация x=r cosφ, y=r sinφ; t=φ.' if i>=26 else '')
  record(b,b.tasks[-1],'parametric tangent/normal coefficients and singular direction limits',str(ts))

def add_card(b,i,page,prompt,fs,derivative,details,note=''):
 final=r'\begin{gathered}'+r'\\'.join(f['label']+r':\ '+f['answer'].replace('sqrt','\\sqrt').replace('pi',r'\pi').replace('e','e') for f in fs)+r'\end{gathered}'
 # Answer equations are rendered as math, labels stay in notes.
 steps=[
  stage('Нужные формулы',block('Нормаль перпендикулярна касательной. Вертикальной касательной соответствует горизонтальная нормаль.',
   r'y-y_0=k(x-x_0),\quad y-y_0=-\frac1k(x-x_0),\quad y^\prime=-F_x/F_y,\quad y_x^\prime=y_t^\prime/x_t^\prime')),
  stage('Производная',block('Находим производную внутри области определения. В особой точке вычисляем направление через предел.',derivative)),
  stage('Точки и наклоны',*[block('',v) for v in details]),
  stage('Ответ',*[block(f['label'],display_lines(f['answer'])) for f in fs])]
 return add(b,14,i,page,6,'Касательные и нормали · пособие',prompt,json.dumps({f['id']:f['answer'] for f in fs}),steps,
  kind='fields',fields=fs,instruction='Введи уравнения прямых. Несколько прямых в одном поле разделяй «;».',note=note)

def display_lines(value):
 from textbook_graphs import line_tex
 return r'\begin{gathered}'+line_tex(value)+r'\end{gathered}'
