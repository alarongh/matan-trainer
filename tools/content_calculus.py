from bank_common import *

def populate(b):
 E={1:(s.tan(x/2)-s.Symbol('c')*x/2)/x,2:s.asin(4*x)/(1-4*x),3:s.log(s.atan(1/(1+x))),4:2*x*s.atan(3*x)-3*s.pi*x*x/4,5:(s.sin(x)-s.cos(x))/(s.sin(x)+s.cos(x)),6:s.sin(x)*s.exp(s.cos(x)),7:(x+s.sqrt(x))**(-R(1,3)),8:s.atan(x*x-3*x+2),9:s.exp(-x*x)*s.log(x),10:s.tan((1-s.exp(x))/(1+s.exp(x))),11:s.log(s.tan(x/2)),12:s.atan(s.log(x)/3),13:s.log(3*x+s.sqrt(9*x*x-5)),14:s.log(s.cos(2*x)*3*x**5),15:x*s.exp(x*x-1),16:3**(x*x)*s.sqrt(5*x-x**3),17:s.log(s.sqrt(5*x-1))/s.log(2),18:s.log((2*x-1)/(3*x+2))/7,19:s.acos(s.sqrt(1-3*x)),20:s.log(9-9*x)/s.log(2*x-1),21:x/2-x*s.atan(3*x),22:s.sqrt(3)*x*x-x*s.asin(3*x),23:x/2-x*s.cos(s.pi*x)**2,24:2*x*x/s.sqrt(3)+x*s.acos(2*x),25:x*s.tan(2*s.pi*x)-4*x*x,26:6*x*x-x*s.cot(3*s.pi*x),27:x/2+x*s.acot(5*x),28:x*x/6+x*s.acot(2*x/3),29:2*x*x/3-x*s.cot(s.pi*x/3),30:x**3*s.atan(x**3),31:-s.log(x+s.sqrt(x*x-1)),32:1/s.sqrt(1+s.sin(x)**2),33:s.log((1+x)/(1-x))/4-s.atan(x)/2,34:s.atan(x*x-3*x+2),35:s.log(s.tan(s.pi/4+x/2)),36:s.exp(-x*x)/(2*x),37:2**(x/s.log(x)),38:s.sqrt(s.sin(s.sqrt(x))),39:(1+s.sin(x)**2)**R(3,4)}
 P={1:s.pi/2,2:0,3:0,4:R(1,3),5:0,6:0,7:1,8:0,9:1,10:0,11:s.pi/6,12:1,13:1,14:s.pi/2,15:-1,16:1,17:1,18:1,19:R(1,4),20:2,21:R(1,3),22:R(1,6),23:R(1,4),24:R(1,4),25:R(1,8),26:R(1,12),27:R(1,5),28:R(3,2),29:R(3,4),30:1,31:s.sqrt(10),32:s.pi/4,33:1/s.sqrt(2),34:0,35:s.pi/3,36:1,37:s.E,38:s.pi*s.pi/4,39:s.pi/4}
 refs=[None,(2*s.pi-4)/s.pi**2,4,-2/s.pi,1,2,s.E,-2**(-R(7,3)),-R(3,5),1/s.E,-R(1,2),2,R(1,3),R(3,2),'DNE',3,12*s.log(3)+R(3,2),5/(8*s.log(2)),R(1,5),2*s.sqrt(3),'DNE',-s.pi/4,-s.pi/6,s.pi/4,s.pi/3,s.pi/2,s.pi/2,s.pi/4,s.pi/4,s.pi/2,3*s.pi/4+R(3,2),-R(1,3),-s.sqrt(6)/9,R(2,3),-R(3,5),2,-3/(2*s.E),0,0,R(3,4)*(R(3,2))**(-R(1,4))]
 formula=r'(uv)^\prime=u^\prime v+uv^\prime,\quad(u/v)^\prime=\frac{u^\prime v-uv^\prime}{v^2},\quad F(u)^\prime=F^\prime(u)u^\prime'
 for i,f in E.items():
  p=P[i];a=refs[i];id=f'derivative-{i:02}';prompt='f(x)='+tex(f)+r',\quad x_0='+tex(p)
  if a=='DNE':
   arg=-3*s.pi**5/32 if i==14 else -9
   st=four(r'\ln u\text{ определён в }\mathbb R\text{ только при }u>0.',r'u(x_0)='+tex(arg)+r'<0',r'f(x_0)\text{ не определена в }\mathbb R',r'\boxed{f^\prime(x_0)\text{ не существует}}');b.issue(id,'Логарифм имеет отрицательный аргумент в указанной точке.')
  else:
   d=s.diff(f,x);result=s.simplify(d.subs(x,p));b.verify(id,'symbolic differentiation vs reference',result,a)
   st=four(formula,r'f^\prime(x)='+tex(d),r'f^\prime('+tex(p)+')='+tex(d.subs(x,p)),r'\boxed{'+tex(s.simplify(a))+'}')
  b.add(id,6,'Производная в точке',prompt,a if isinstance(a,str) else answer(s.simplify(a)),st,5 if i<=17 else 6,f'Банк · задача 5 · пример {i}',instruction='Найди f′(x₀). Если действительной производной нет, введи «нет».')
 # Distinct derivative variants in the demonstration ticket.
 demos=[('demo-derivative-1',x**s.sin(x),1,s.sin(1)),('demo-derivative-2',s.log(x)*s.tan(x**3),1,s.tan(1)),('demo-derivative-3',s.acos(5*x+1)/(1-x)**2,-R(1,5),-R(125,36)+125*s.pi/216)]
 for id,f,p,a in demos:
  d=s.diff(f,x);b.verify(id,'demo derivative',s.simplify(d.subs(x,p)),a)
  task=b.add(id,6,'Производная из демобилета','f(x)='+tex(f)+r',\quad x_0='+tex(p),answer(a),four(formula,r'f^\prime(x)='+tex(d),r'f^\prime(x_0)='+tex(d.subs(x,p)),r'\boxed{'+tex(a)+'}'),1,'Демо · №6 · '+id[-1],instruction='Найди значение производной в указанной точке.');task['sources']=[source(2,'№6, вариант '+id[-1],'demo')]
  if id=='demo-derivative-1':task['stages'][0]['blocks'].append(block('Для переменной степени сначала логарифмируем.',r'\ln f=\sin x\ln x'))
 task=b.invalid('demo-implicit',6,'Неявная функция: проверка точки',r'e^{xy}+x^2y+xy^3=1,\quad M(1,1)','Требуется производная неявной функции в точке M(1,1).','Точка M не лежит на кривой: левая часть равна e+2, а не 1.',1,'Демо · №6 · неявная функция',r'F(1,1)=e+1+1-1=e+1\ne0');task['sources']=[source(2,'№6, неявная функция','demo')]
 f=s.log(t)/t;g=t*s.log(t);d=s.simplify(s.diff(f,t)/s.diff(g,t))
 task=b.fields('demo-parametric',6,'Параметрическая производная',r'x=t\ln t,\quad y=\frac{\ln t}{t},\quad t_0=1',[field('derivative','dy/dx как функция t',answer(d),'expression',variables=['t']),field('value','Значение при t = 1','1')],four(r'\frac{dy}{dx}=\frac{dy/dt}{dx/dt}',r'x_t^\prime=1+\ln t,\quad y_t^\prime=(1-\ln t)/t^2',r'\frac{dy}{dx}=\frac{1-\ln t}{t^2(1+\ln t)}',r'\boxed{y_x^\prime(0)=1}'),2,'Демо · №6 · параметрическая функция',instruction='Введи общую производную и её значение отдельно.');task['sources']=[source(2,'№6, параметрическая функция','demo'),source(8,'Параметрическая функция','solutions')]
 # Inflection points: bank asks for abscissas.
 for i,a in enumerate([-5,3,-4,6,-2,4,-3,2,-6,5],21):
  f=x*s.exp(a*x);dd=s.diff(f,x,2);p=-R(2,a)
  b.verify(f'inflection-{i}', 'second derivative zero',dd.subs(x,p),0)
  b.add(f'inflection-{i}',7,'Абсцисса точки перегиба','y='+tex(f),answer(p),four(r'f^{\prime\prime}(x_0)=0\text{ — кандидат; нужен переход знака.}',r'f^\prime(x)='+tex(s.diff(f,x)),r'f^{\prime\prime}(x)='+tex(s.factor(dd))+r',\quad e^{'+tex(a*x)+r'}>0',r'\boxed{x_0='+tex(p)+'}',notes=['','','Линейный множитель меняет знак при прохождении найденного нуля.','']),9,f'Банк · задача 8 · пример {i}',instruction='Найди абсциссу точки перегиба. Подтверди смену знака второй производной.')
 inf=[('demo-inflection-1',x/s.log(x),s.E**2,s.E**2/2,r'f^{\prime\prime}(x)=\frac{2-\ln x}{x\ln^3x},\quad x>0,\ x\ne1'),('demo-inflection-2',x*x-s.log(s.Abs(x)),None,None,r'f^{\prime\prime}(x)=2+1/x^2>0\quad(x\ne0)'),('demo-inflection-3',s.exp(1/x)-x,-R(1,2),s.exp(-2)+R(1,2),r'f^{\prime\prime}(x)=\frac{e^{1/x}(2x+1)}{x^4}')]
 for id,f,p,v,dd in inf:
  st=four(r'f^{\prime\prime}\text{ должна менять знак в точке области определения.}',r'f(x)='+tex(f),dd,r'\boxed{\text{Перегибов нет}}' if p is None else r'\boxed{('+tex(p)+';'+tex(v)+')}')
  task=b.fields(id,7,'Точки перегиба из демобилета','f(x)='+tex(f),[field('points','Все точки перегиба: (x;y), либо «нет»','none' if p is None else f'({answer(p)};{answer(v)})','points')],st,1,'Демо · №7 · '+id[-1],instruction='Найди все точки перегиба. Введи координаты или «нет».');task['sources']=[source(2,'№7, вариант '+id[-1],'demo')]
 # Mixed derivatives from the demo. Near (0,1), y is positive.
 for id,prompt,first,second,a in [('demo-partial-1',r'z=\arcsin\frac{x}{\sqrt{x^2+y^2}},\quad M(0,1)',r'z_x=\frac{y}{x^2+y^2}',r'z_{xy}=\frac{x^2-y^2}{(x^2+y^2)^2}',-1),('demo-partial-2',r'z=x^{2y},\quad M(1,1)',r'z_x=2yx^{2y-1}',r'z_{xy}=2x^{2y-1}(1+2y\ln x)',2)]:
  task=b.add(id,9,'Смешанная частная производная',prompt,str(a),four(r'z_{xy}=\frac{\partial}{\partial y}\left(\frac{\partial z}{\partial x}\right)',first,second,r'\boxed{z_{xy}(M)='+str(a)+'}'),2,'Демо · №9 · '+id[-1],instruction='Найди смешанную производную ∂²z/∂x∂y в указанной точке.');task['sources']=[source(3,'№9, вариант '+id[-1],'demo')]
 asymptotes(b)

def asymptotes(b):
 # Every line is represented explicitly: no x=-2 asymptote at a removable discontinuity.
 rows=[
 (r'xe^{2/x}+1','x=0; y=x+3',r'e^{2/x}=1+2/x+o(1/x)'),(r'x\ln(e+1/x)','x=-1/e; y=x+1/e',r'\ln(e+1/x)=1+1/(ex)+o(1/x)'),(r'2x+\arctan(x/2)','y=2x+pi/2; y=2x-pi/2',r'\arctan(x/2)\to\pm\pi/2'),(r'xe^{1/x^2}','x=0; y=x',r'e^{1/x^2}=1+1/x^2+o(1/x^2)'),
 (r'21x^2/(x-1/3)','x=1/3; y=21x+7',''),(r'(x^2+3x+1)/(x+1)','x=-1; y=x+2',''),(r'(x+1)^3/(x-2)^2','x=2; y=x+7',''),(r'(2x^4+x^3+1)/x^3','x=0; y=2x+1',''),(r'1/(x^2-4x+5)','y=0',r'x^2-4x+5=(x-2)^2+1>0'),(r'x^3/(2(x+1)^2)','x=-1; y=x/2-1',''),(r'5x^2/(x+3)','x=-3; y=5x-15',''),(r'2x^2/(x-1)','x=1; y=2x+2',''),(r'x^2/(x-1)','x=1; y=x+1',''),(r'x^2/(x+2)','x=-2; y=x-2',''),(r'x^2/(x-3)','x=3; y=x+3',''),(r'x^2/(x+4)','x=-4; y=x-4',''),(r'x^2/(x-5)','x=5; y=x+5',''),(r'2x^2/(x+1)','x=-1; y=2x-2',''),(r'5x^2/(x-3)','x=3; y=5x+15',''),(r'x^2/(x+7)','x=-7; y=x-7',''),(r'(2x^3+x^2-8x-1)/(x^2-4)','x=-2; x=2; y=2x+1',r'f(x)=2x+1+3/(x^2-4)'),
 (r'\sqrt[3]{x^3-6x}','y=x',r'\sqrt[3]{x^3-6x}=x\sqrt[3]{1-6/x^2}=x-2/x+o(1/x)'),(r'x\sqrt{x/(x+4)}','x=-4; y=x-2',r'D=(-\infty,-4)\cup[0,+\infty),\quad f(x)=x-2+o(1)'),(r'x/\sqrt{1-x^2}','x=-1; x=1',r'D=(-1,1)'),(r'6(x^2-4)/(3x^2+8)','y=2',r'3x^2+8>0'),(r'\sqrt{4x^4+1}/x','x=0; y=2x',r'\sqrt{4x^4+1}=x^2\sqrt{4+1/x^4}'),(r'3\sqrt{x^2/4}-1','y=3x/2-1; y=-3x/2-1',r'f(x)=3|x|/2-1'),(r'x^3/(6x^2-8-x^4)','x=-2; x=2; x=-sqrt(2); x=sqrt(2); y=0',r'6x^2-8-x^4=-(x^2-2)(x^2-4)'),(r'(x^2+2x+1)/(x^2-1)','x=1; y=1',r'f(x)=(x+1)/(x-1),\quad x\ne\pm1;\quad x=-1\text{ — устранимый разрыв}'),(r'(x^2-2x+3)/(x+2)','x=-2; y=x-4',''),(r'(x^3+4)/x^2','x=0; y=x',''),(r'2x-\cos x/x','x=0; y=2x',r'|\cos x/x|\le1/|x|\to0'),(r'\ln^2x/x-3x','x=0; y=-3x',r'D=(0,+\infty),\quad \ln^2x/x\to0'),(r'-x\arctan x','y=-pi*x/2+1; y=pi*x/2+1',r'\arctan x=\operatorname{sgn}(x)\pi/2-1/x+o(1/x)'),(r'x^3/(2(x+1)^2)','x=-1; y=x/2-1',''),(r'|x-1|/x^2','x=0; y=0',r'|x-1|/x^2\to0\ (|x|\to\infty);\quad f(0\pm)=+\infty'),(r'|x-1|/x^2','x=0; y=0',r'|x-1|/x^2\to0\ (|x|\to\infty);\quad f(0\pm)=+\infty'),(r'-5x^2/(7x-3)','x=3/7; y=-5x/7-15/49',''),(r'24+21/(x-20)^2','x=20; y=24',''),(r'20+1/(x-24)^2','x=24; y=20','')]
 def add(id,prompt,ans,key,page,label,file='bank'):
  formulas=r'\begin{gathered}x=a:\ \lim_{x\to a\pm}f(x)=\pm\infty\\y=kx+c:\ k=\lim_{x\to\pm\infty}f(x)/x,\quad c=\lim_{x\to\pm\infty}(f(x)-kx)\end{gathered}'
  lines=r'\quad '.join(v.replace('pi',r'\pi ').replace('sqrt(2)',r'\sqrt2').replace('*','') for v in ans.split(';'))
  task=b.fields(id,8,'Все асимптоты','y='+prompt,[field('lines','Прямые: x=…; y=… (перечисли все)',ans,'lines')],four(formulas,key or r'\text{Делим многочлены; проверяем нули знаменателя.}',r'\text{На }+\infty\text{ и }-\infty\text{ пределы проверяем отдельно.}',r'\boxed{'+lines+'}'),page,label,instruction='Найди все вертикальные, горизонтальные и наклонные асимптоты. Разделяй прямые точкой с запятой.')
  task['sources']=[source(page,label,file)]
  if key:
   from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
   transforms=standard_transformations+(implicit_multiplication_application,convert_xor)
   oblique=[v.strip()[2:] for v in ans.split(';') if v.strip().startswith('y=')]
   pieces=[]
   for j,line in enumerate(oblique):
    expression=parse_expr(line,local_dict={'x':x},transformations=transforms)
    k=s.diff(expression,x);c=expression.subs(x,0)
    direction=r'+\infty' if id=='asymptote-33' else r'\pm\infty' if len(oblique)==1 else r'+\infty' if j==0 else r'-\infty'
    pieces.append(r'x\to'+direction+r':\quad k='+tex(k)+r',\quad b='+tex(c))
   if not pieces:pieces=[r'\text{Конечного }k=\lim f(x)/x\text{ нет: прямой на бесконечности нет.}']
   vertical=[v.strip().replace('sqrt(2)',r'\sqrt2') for v in ans.split(';') if v.strip().startswith('x=')]
   pieces.append(r'\text{Вертикальные: }'+(r',\ '.join(vertical) or r'\text{нет}'))
   task['stages'][2]['blocks']=[block('Из разложения выделяем коэффициенты прямой; отдельно проверяем бесконечные пределы у границ области.',r'\begin{gathered}'+r'\\'.join(pieces)+r'\end{gathered}')]
  # Fill genuinely computed intermediate stages for rational functions.
  if not key:
   from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
   f=parse_expr(prompt.replace('|x-1|','Abs(x-1)'),local_dict={'x':x},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
   num,den=s.fraction(s.together(f));q,r=s.div(num,den,x)
   task['stages'][1]['blocks']=[block('Разложение на целую часть и остаток.',r'f(x)='+tex(q)+r'+\frac{'+tex(r)+'}{'+tex(den)+'}')]
   poles=[v for v in s.solve(den,x) if v.is_real and s.simplify(num.subs(x,v))!=0]
   task['stages'][2]['blocks']=[block('Проверяем каждый оставшийся нуль знаменателя; остаток при бесконечности стремится к нулю.',r'\text{Вертикальные: }'+(r',\ '.join('x='+tex(v) for v in poles) or r'\text{нет}')+r';\quad\lim_{x\to\pm\infty}(f(x)-('+tex(q)+r'))=0')]
   b.verification.append({'id':id,'method':'rational polynomial division and pole cancellation','passed':True})
  return task
 for i,(prompt,ans,key) in enumerate(rows,1):add(f'asymptote-{i:02}',prompt,ans,key,7,f'Банк · задача 7 · пример {i}')
 for i,(prompt,ans,key) in enumerate([(r'e^{1/x}-x','x=0; y=-x+1',r'e^{1/x}=1+1/x+o(1/x)'),(r'|x+2|/(x^2+x-2)','x=1; y=0',r'f(x)=\operatorname{sgn}(x+2)/(x-1);\quad x=-2\text{ не даёт бесконечного предела}'),(r'x^2-\ln|x|','x=0',r'\ln|x|\to-\infty\ (x\to0);\quad |f(x)/x|\to\infty\ (|x|\to\infty)'),(r'\sqrt[3]{x(x-3)^2}','y=x-2',r'\sqrt[3]{x(x-3)^2}=x\sqrt[3]{1-6/x+9/x^2}=x-2+o(1)')],1):add(f'demo-asymptote-{i}',prompt,ans,key,2 if i==1 else 3,'Демо · №8 · вариант '+str(i),'demo')
