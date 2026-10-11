from textbook_common import *

def populate(b):
 L=s.log;S=s.sin;C=s.cos;T=s.tan;Q=s.cot;E=s.exp
 rows=[
 L(C((x-1)/x)),x*S(L(x)-s.pi/4),s.atan(L(1/x)),x/L(x)**2,L(L(3-2*x**3)),2**Q(1/x),
 s.sqrt(E(S(x)**2)),s.sqrt(C(x)**2-2*S(x)**2),s.sqrt(3*S(x)**2+5*C(x)**2),
 C(x)**3*(3*C(x)**2-5)/15,x*x/L(x),(1+s.sqrt(x))/(1-s.sqrt(x)),R(3,4)*((1+L(x))**4)**R(1,3),
 s.atan(3*T(x))/3,E(T(3*x)**2),s.asin(s.sqrt(x)/2),s.atan(E(x)+E(-x)),s.asin(s.sqrt(x-1)),
 s.atan(s.sqrt((x-1)/2)),T(s.sqrt(3*x))**2,T(x)**2/2+L(C(x)),
 L(S(x))+Q(x)**2/2-Q(x)**4/4,R(2,3)*(L(x)-5)*s.sqrt(1+L(x)),
 2/s.sqrt(3)*s.atan((2*x+1)/s.sqrt(3)),L(2*x+s.sqrt(3))**3,(x+s.sqrt(x))**R(1,3),
 (1+C(2*x))/(1-C(2*x)),L(S(x))+Q(x)**2/2,T(x)**5/5+T(x)**7/7,s.asin(x*x/s.sqrt(3))/2]
 for i,f in enumerate(rows,1):derivative_card(b,9,i,25 if i<=24 else 26,f)
 rows=[
 (1+2*x*x)/(x*s.sqrt(1+x*x)),s.sqrt(1+x*x)*(x*x-2)/3,
 s.sqrt(1+x*x)*(2*x*x-1)/(3*x**3),s.atan(x/2+s.sqrt(x*x/4+x-1)),
 L(s.sqrt(3)*x+s.sqrt(3*x*x-2))/s.sqrt(3),R(2,35)*(1+x)**R(5,2)*(5*x-2),
 (1+2*x*x)**R(5,2)*(5*x*x-1)/70,(x-2)/(4*s.sqrt(4*x-x*x)),
 L(x+R(1,2)+s.sqrt(x*x+x+1)),R(2,15)*(3*x-4)*(2+x)**R(3,2),
 R(4,3)*(x**R(3,4)-L(1+x**R(3,4))),L((s.sqrt(x+1)-1)/(s.sqrt(x+1)+1)),
 (3*x-9)*((x+2)**2)**R(1,3)/10,(20*x+32)*(x-2)*(x-2)**R(1,4)/45,
 L((s.sqrt(x*x-x+2)+x-s.sqrt(2))/(s.sqrt(x*x-x+2)+x+s.sqrt(2)))/s.sqrt(2),
 (1+x**3)**R(1,3)*(x*x-3)/x**2,
 L((s.sqrt(2+2*x)-s.sqrt(2-x))/(s.sqrt(2+2*x)+s.sqrt(2-x)))/s.sqrt(2),
 s.atan((5*T(x)+4)/3)/3,s.asin((8*x+3)/s.sqrt(41))/2,
 L(((x+2)/C(x)**2)**R(1,3)),L(s.sqrt((1+x)/T(x))),s.atan(1/s.sqrt(2*x))**2,
 L(((1+4*x)/S(x)**3)**R(1,4)),s.asin((x-1)/s.sqrt(x)),
 L(5*(1+3*T(x))),L((x-2)**5/(x+1)**3),2*(10+3*x)/(9*s.sqrt(5+3*x)),
 R(4,21)*(3*E(x)-4)*(E(x)+1)**R(3,4),2*s.sqrt(x+1)*(L(x+1)-2),L(x**3/(x**3+8))/24]
 for i,f in enumerate(rows,1):derivative_card(b,10,i,26 if i<=18 else 27,f)
 rows=[
 x*s.sqrt(x*x+1)/((x**3+1)**R(1,3)*(x**4+1)**R(1,4)),
 x**5*(x*x/((x*x+1)*(2*x+3)))**R(1,3),
 (x-1)*(x*x+1)**R(1,3)/s.sqrt(x*(2-x)),x**C(x),S(x)**(1/x),x**T(x),T(x)**C(x),
 s.asin(x)**(x*x),(1+x*x)**(x*x),C(x)**x,s.atan(x)**x,S(3*x)**x,
 (s.sqrt(x)-1)/((x+2)**R(2,3)*(x+3)**R(3,2)),(x-2)**3/s.sqrt((x-1)**5*(x-3)**11),
 s.sqrt(x*(x-1)**R(1,3)/(x*x-2)),T(x)**E(x),L(S(3*x))**x,(1+x**3)**(x**3),
 C(x)**S(x),x**s.sqrt(x),x**(1/x),s.sqrt(C(x))*2**s.sqrt(C(x)),
 s.atan(x)**L(x),S(x)**L(x),(1+x*x)**s.acos(x),
 (x**3*(x*x*s.sqrt(x+1))**R(1,3))**R(1,4),
 (x*x+3*x+1)**R(1,4)/(x*x+4*s.sqrt(7*x+1))**R(1,3),
 (x*x+1)**s.sqrt(x),x**6*(x*x+1)**10*(x**3+1)/(2*x*x+5)**2,
 R(3,2)*((1+x)/(1-x))**R(1,3)*s.sqrt(x*x+1)]
 for i,f in enumerate(rows,1):
  if i==17:
   task=b.invalid('textbook-11-17',6,'Область логарифмического дифференцирования',r'y=(\ln\sin3x)^x',
    'Проверяем исходную вещественную запись перед логарифмическим дифференцированием.',
    'При sin3x>0 всегда ln(sin3x)≤0. Основание не бывает положительным, поэтому обычный метод переменной вещественной степени через ln основания здесь неприменим; нужно уточнение условия.',28,ref(11,i,28),
    r'0<\sin3x\le1\Rightarrow\ln(\sin3x)\le0')
   task['sources']=[source(28,'Задача 11, пример 17','textbook')]
  else:derivative_card(b,11,i,27 if i<=14 else 28,f,logarithmic=True)
 param=[
 (2*S(t)/(1+3*C(t)),5*C(t)/(1+3*C(t))),(L(1+t*t),t-s.atan(t)),(E(-t*t),s.atan(2*t+1)),
 (4*T(t/2)**2,2*S(t)+3*C(t)),(s.asin(t*t-1),s.acos(2*t)),(5*(C(t)+t*S(t)),5*(S(t)-t*C(t))),
 (s.acos(1/s.sqrt(1+t*t)),s.asin(t/s.sqrt(1+t*t))),(L(T(t/2))+C(t),t*S(t)+C(t)),
 (t*t+2*t,t*t-L(t*t)),(t**3/(t+1),t*t/(t+1)),(1/(t*t-1),(t*t+1)/(t+2)),
 (6*t/(1+t**3),6*t*t/(1+t**3)),(s.sqrt(t),t**R(1,3)),(E(t),s.asin(t)),
 (2*C(t)**2,3*S(t)**2),(L(t),(t+1/t)/2),(6*t/(1+t*t),3*(1-t*t)/(1+t*t)),
 (s.sqrt(1+t*t),(t-1)/s.sqrt(1+t*t)),(s.asin(t),s.sqrt(1-t*t)),(5*C(t)**3,4*S(t)**3),
 (2*t-t**3,2*t*t),(C(t)**3/s.sqrt(C(2*t)),S(t)**3/s.sqrt(C(2*t))),
 ((t**3+2)/(t*t+1),t**3/(t*t+1)),(t*t*E(-t),t*t*E(2*t)),
 (2*(t+1/t),t+3/t+1/t**2),(L(t),S(t)**2),(E(t)*C(t),E(t)*S(t)),
 (1/(t+1),(t/(t+1))**2),(1/(t+1),t/(t+1)),(t+L(C(t)),t-L(S(t)))]
 for i,(X,Y) in enumerate(param,1):
  dx=s.diff(X,t);dy=s.diff(Y,t);d=s.factor(dy/dx)
  task=add(b,12,i,28 if i<=4 else 29 if i<=18 else 30,6,'Параметрическая производная',
   r'\begin{cases}x='+tex(X)+r'\\y='+tex(Y)+r'\end{cases}',ans(d),
   four(r'\frac{dy}{dx}=\frac{dy/dt}{dx/dt}\quad(dx/dt\ne0)',r'x_t^\prime='+tex(dx)+r',\quad y_t^\prime='+tex(dy),
    r'y_x^\prime=\frac{'+tex(dy)+'}{'+tex(dx)+'}',r'\boxed{y_x^\prime='+tex(d)+'}'),
   kind='expression',variables=['t'],instruction='Введи dy/dx как выражение через t. Формула действует при x′(t)≠0.')
  assert s.simplify(d*dx-dy)==0
  record(b,task,'parametric chain rule identity','dy/dx * dx/dt = dy/dt')
 implicit(b)
 partials(b)
 from textbook_tangents import populate as tangents
 tangents(b)

def implicit(b):
 L=s.log;E=s.exp;S=s.sin;C=s.cos
 rows=[
 L(x)+E(-y/x)+5,x**R(2,3)+y**R(2,3)-10,y-s.sqrt(4*x-x*x+10*y-4)+3,
 E(x)-E(y)+x-y-6,x-(2*x*x*y*y+5*x+y-5)**R(1,3)+9,
 3/s.sqrt(x*y)-s.sqrt(x/y)-s.sqrt(y/x)-8,s.atan(y/x)-L(s.sqrt(x*x+y*y))+2,
 E(x)-E(y)-x*y,y-s.sqrt(2*x-x*x-5*x*y-y),2*C(x+y)**2+x*y-9,
 3*s.atan(y/x)-s.sqrt(x*x+y*y)+5,L(5*y)+x/y+7,x-s.acot(x+y)+1,
 y-((2*y-1)/x)**R(1,3)+12,E(x)*S(y)-E(-y)*C(x),x-(y**3+x-4)**R(1,3),
 y**3-(x-y)/(x+y)-6,y*E(x-1)-E(y)+9,y*y-x-L(y/x)-4,x+y-3*(x-y)**R(1,3)+11,
 y-(x+10*y-6+(4*y+5)/x)**R(1,3),x-s.sqrt(2*y**3-x*x/y+y/x-3),
 x-s.sqrt(1+2*x*y+y*y-8*y**3)+3,x/y-S(x)/S(y)+3,s.sqrt(x+y)-y*s.sqrt(x-y)-7,
 L(x+y)-8/s.sqrt(x+y*y),S(y-x*x)-L(y*y-x),E(x)+E(y)-2*x*y-2,
 x**(y*y)+y*y*L(x)-4,x*x*S(y)+y**3*C(x)-2*x]
 for i,F in enumerate(rows,1):
  fx=s.diff(F,x);fy=s.diff(F,y);d=s.factor(-fx/fy)
  task=add(b,13,i,31 if i<=14 else 32 if i<=28 else 33,6,'Неявная производная',r'F(x,y)='+tex(F)+r'=0',ans(d),
   four(r'F_x+F_y y^\prime=0,\quad y^\prime=-F_x/F_y\ (F_y\ne0)',
    r'F_x='+tex(fx)+r',\quad F_y='+tex(fy),r'y^\prime=-\frac{'+tex(fx)+'}{'+tex(fy)+'}',r'\boxed{y^\prime='+tex(d)+'}'),
   kind='expression',variables=['x','y'],instruction="Введи y′ через x и y; результат действует на допустимой ветви при F_y≠0.")
  assert s.cancel(d*fy+fx)==0
  record(b,task,'implicit differentiation identity','F_x + F_y yprime = 0')

def partials(b):
 L=s.log;E=s.exp;S=s.sin;C=s.cos;T=s.tan
 rows=[
 x**3+y**3+3*x/y,s.sqrt(x*x-y*y),s.atan((x+y)/(1-x*y)),S(x+C(y)),x*x*L(x+y),E(x/y),
 L(C(y/x)),L(T(x-y)),E((x**3+y*y)**2),x**3+4*x*x*y*y-y**4,x*S(2*x+3*y),C(x*x)/y,
 L(x*x+y),x*y+y/x,x*x*S(y)**4,L(1+x/y),C(y+S(x)),L(T(y/x)),x*y*S(x*y),
 x**4*C(y)**2,E(S(y/x)),x*y/s.sqrt(x*x+y*y),x*C(x+y),E(x)*C(y),
 x**3+2*y*y-2*y**3*x*x,y**x,L(T(x/y)),x**3*S(y)+y**3*C(x),T(y*y/x),y*L(x*x-y*y)]
 mixed=[
 E(x*y*(x*x+y*y)),s.asin(x/s.sqrt(x*x+y*y)),(x*x+y*y)*E(x+y),x*L(x**3*y*y),(x*x-y*y)/(x*x+y*y),
 s.atan(y/(1+x*x)),x*y/(x+y),E(x)*(x*S(y)+y*y),(x+y)/(x-y),s.atan(x/y**2),S(x*x)/y,
 x*s.atan(y/(y-x)),T(x*x/y),s.atan((x+y)/(1-x*y)),L(s.sqrt(x*x+y*y)),
 2*x*x*y+3*x*y*y+x**3,x*x/y**2-y/x,x/s.sqrt(x*x+y*y),s.sqrt(2*x*y+y*y),
 y*L(x*x-y*y),s.atan(y/x)+s.atan(x/y),E(x)*(C(y)+x*S(y)),x**y,x*L(y/x),
 E(x+y)*(x*C(y)+y*S(x)),L(x*x+x*y+y*y),S(x*x-y*y),E(3*x*x+2*y*y-x*y),x*y+x/y,x*y*S(x-y*y)]
 for section,expressions in [(24,rows),(25,mixed)]:
  for i,F in enumerate(expressions,1):
   fx=s.factor(s.diff(F,x));fy=s.factor(s.diff(F,y))
   if section==24:values=[fx,fy];labels=['∂z/∂x','∂z/∂y'];key=r'z_x='+tex(fx)+r',\quad z_y='+tex(fy)
   else:
    xy=s.factor(s.diff(F,x,y));yx=s.factor(s.diff(F,y,x));assert s.simplify(xy-yx)==0,(i,xy,yx)
    values=[xy,yx];labels=['∂²z/∂y∂x','∂²z/∂x∂y'];key=r'z_{xy}='+tex(xy)+r',\quad z_{yx}='+tex(yx)
   fs=[field('a',labels[0],ans(values[0]),'expression',variables=['x','y']),field('b',labels[1],ans(values[1]),'expression',variables=['x','y'])]
   page=52 if section==24 and i<=6 else 53 if section==24 else 54 if i<=28 else 55
   task=add(b,section,i,page,9,'Частные производные' if section==24 else 'Смешанные производные',r'z='+tex(F),
    json.dumps({f['id']:f['answer'] for f in fs}),four(
     r'\partial_x y=0,\quad\partial_y x=0,\quad z_{xy}=\partial_y(\partial_x z),\quad z_{yx}=\partial_x(\partial_y z)',
     r'z_x='+tex(fx)+r',\quad z_y='+tex(fy),key,r'\boxed{\begin{gathered}'+key+r'\end{gathered}}',
     ['При производной по одной переменной остальные считаются константами.','Находим первые производные по правилам произведения, дроби и цепочки.','Для смешанных производных дифференцируем ещё раз по другой переменной.','Результаты действуют внутри области определения; в задаче 25 проверяем равенство.']),
    kind='fields',fields=fs,instruction='Введи два выражения через x и y.')
   record(b,task,'symbolic partial derivatives and mixed derivative equality' if section==25 else 'symbolic partial differentiation',str(values))
