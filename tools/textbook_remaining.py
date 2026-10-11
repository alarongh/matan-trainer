"""The six practical sections previously outside the ticket mapping."""
from textbook_common import *

def populate(b):
 sequences(b); definitions(b); taylor(b); extrema(b)
 from textbook_review import populate as reviews
 reviews(b)

def sequences(b):
 rows=[((7*n-1)/(n+1),7,R(1,100)),((4*n*n+1)/(3*n*n+2),R(4,3),R(1,100)),
 ((9-n**3)/(1+2*n**3),-R(1,2),R(1,100)),((-R(1,2))**n,0,R(1,1000)),
 (1+(-1)**n/(2*n+1),1,R(1,100)),((4*n-3)/(2*n+1),2,R(1,1000)),
 ((1-2*n*n)/(2+4*n*n),-R(1,2),R(1,100)),((2*n+(-1)**n)/n,2,R(1,100)),
 (-5*n/(n+1),-5,R(1,100)),(1/s.log(n+1),0,R(1,3)),
 ((n+1)/(1-2*n),-R(1,2),R(1,100)),((2*n+1)/(3*n-5),R(2,3),R(1,100)),
 ((1-2*n*n)/(n*n+3),-2,R(1,100)),(3*n*n/(2-n*n),-3,R(1,100)),
 (n/(3*n-1),R(1,3),R(1,100)),(2*n/(1+n*n),0,R(1,10)),
 (3*n**3/(n**3-2),3,R(1,100)),((4+2*n)/(1-3*n),-R(2,3),R(1,100)),
 ((5*n+15)/(6+n),5,R(1,100)),((3-n*n)/(1+2*n*n),-R(1,2),R(1,100)),
 ((7-n)/(n+3),-1,R(1,100)),((3*n*n+4)/(2-n*n),-3,R(1,100)),
 ((-5+4*n**3)/(3+2*n**3),2,R(1,100)),(R(1,3)**n,0,R(1,1000)),
 (3-(-1)**n/(n+5),3,R(1,100)),((9*n+7)/(2*n-3),R(9,2),R(1,100)),
 ((2+n*n)/(4+2*n*n),R(1,2),R(1,100)),((-5*n+(-1)**n)/(2*n+3),-R(5,2),R(1,100)),
 (2/s.log(3*n+4),0,R(1,4)),((-R(2,7))**n,0,R(1,1000))]
 for i,(u,A,eps) in enumerate(rows,1):
  error=s.simplify(u-A)
  # Each parity subsequence has decreasing absolute error for real n>=2.
  # Check N and N+1 to cover both parities. Small initial terms are checked too.
  def holds(N):return all(abs(s.N(error.subs(n,k),50))<eps for k in (N,N+1))
  N=1
  while not holds(N):N+=1
  assert N<10000
  certificates=[]
  for parity in (1,-1):
   q=s.simplify(error.subs((-1)**n,parity))
   # Eliminate negative geometric base in the absolute magnitude.
   if i in (4,30):q=(R(1,2) if i==4 else R(2,7))**n
   derivative=s.diff(q*q,n)
   for v in (max(2,N),max(3,N+1),N+100,N+10000):
    assert s.N(derivative.subs(n,v),40)<=0,(i,parity,v)
   certificates.append(tex(s.simplify(q)))
  task=add(b,1,i,7 if i<=10 else 8,11,'Предел по определению · последовательность',
   r'u_n='+tex(u)+r',\quad A='+tex(A)+r',\quad\varepsilon='+tex(eps),str(N),
   four(r'\forall\varepsilon>0\ \exists N\in\mathbb N:\ \forall n\ge N\quad |u_n-A|<\varepsilon',
    r'u_n-A='+tex(error),
    r'|u_n-A|<'+tex(eps)+r'\quad\text{для всех }n\ge '+str(N),
    r'\boxed{N\ge '+str(N)+'}',
    ['На бумаге докажи утверждение для произвольного ε, затем найди N для указанного ε. Сайт проверяет только достаточность числового N.',
     'Вычти A и приведи к общей дроби. Для (−1)^n модуль равен 1; при разных числителях проверь обе чётности.',
     'Реши строгое неравенство. Ошибка убывает на каждом из двух хвостов чётных и нечётных n; проверь первые два значения хвоста.',
     'Можно взять большее целое N. Числовой ответ сам по себе не заменяет доказательство по определению.']),
   kind='threshold',minimum=N,instruction='Докажи на бумаге предел по определению. Введи любое достаточное целое N, при котором неравенство верно для всех n ≥ N.')
  record(b,task,'exact first-tail and parity checks; derivative of squared error sampled on tail',f'N_min={N}; N and N+1 checked at 50 digits')

def definitions(b):
 # Infinity without a sign means |f|, and x→∞ without a sign means |x|.
 rows=[('-inf','abs',None),(-1,'pos','-'),('absinf',4,None),('inf','neg',None),
 (0,-3,'-'),('-inf',0,None),('absinf','abs',None),('inf',-1,None),(-2,'neg','+'),
 ('absinf','pos',None),(1,'abs',None),('-inf','pos',None),(-3,-3,'+'),('absinf','neg',None),
 (0,'pos',None),('inf','pos',None),(0,'neg','+'),('-inf','abs',None),(-4,'neg',None),(0,-8,None),
 ('absinf',0,None),(-3,'neg','-'),('inf','abs',None),('absinf','neg',None),(0,0,'+'),
 ('-inf',-5,None),(0,'neg',None),(3,'pos','+'),('inf',0,None),(2,'abs','-')]
 for i,(a,v,side) in enumerate(rows,1):
  infin=isinstance(a,str);outinf=isinstance(v,str)
  if infin:
   premise={'inf':'x>K','-inf':'x<-K','absinf':'|x|>K'}[a]
   quant=r'\exists K>0\ \forall x\in D_f:'
   wrongprem={'inf':'x<K','-inf':'x>-K','absinf':'|x|<K'}[a]
   xt={'inf':r'+\infty','-inf':r'-\infty','absinf':r'\infty'}[a]
  else:
   premise=(r'0<x-('+str(a)+r')<\delta' if side=='+' else r'0<('+str(a)+r')-x<\delta' if side=='-' else r'0<|x-('+str(a)+r')|<\delta')
   wrongprem=r'|x-('+str(a)+r')|>\delta'
   quant=r'\exists\delta>0\ \forall x\in D_f:'
   xt=str(a)+(r'^{'+side+'}' if side else '')
  conclusion={'abs':'|f(x)|>M','pos':'f(x)>M','neg':'f(x)<-M'}[v] if outinf else '|f(x)-('+str(v)+r')|<\varepsilon'
  prefix=r'\forall M>0\ ' if outinf else r'\forall\varepsilon>0\ '
  definition=prefix+quant+r'\quad '+premise+r'\Rightarrow '+conclusion
  wrong=prefix+quant+r'\quad '+wrongprem+r'\Rightarrow '+conclusion
  swapped=definition.replace(r'\forall M>0',r'\exists M>0').replace(r'\forall\varepsilon>0',r'\exists\varepsilon>0')
  correct=str(1+i%3)
  options=[{'value':str(k),'label':'','tex':definition if str(k)==correct else wrong if k==(int(correct)%3)+1 else swapped} for k in (1,2,3)]
  vt={'abs':r'\infty','pos':r'+\infty','neg':r'-\infty'}[v] if outinf else str(v)
  task=add(b,3,i,11,11,'Логическая запись предела',r'\lim_{x\to '+xt+r'}f(x)='+vt,correct,
   four(r'\forall=\text{для любого},\quad\exists=\text{существует}',
    prefix+quant,premise+r'\Rightarrow '+conclusion,definition,
    ['Сначала самостоятельно запиши определение и объясни его геометрически. Затем выбери соответствующую запись.',
     'Точность ε или высота M выбирается произвольно; после неё выбирается граница K или расстояние δ.',
     'Предпосылка указывает, с какой стороны подходит x. Знак бесконечности определяет требование к f(x).',
     'Геометрически: все точки графика из указанной окрестности или хвоста должны лежать в полосе |y−A|<ε, выше M, ниже −M либо вне |y|≤M, как в этой записи.']),
   kind='choice',options=options,instruction='Запиши определение и геометрический смысл на бумаге. Выбери верную логическую запись.',
   note='∞ без знака в этом пособии означает модульную бесконечность; +∞ и −∞ учитывают знак.')
  record(b,task,'quantifier construction from transcribed side and signed limit',definition)

def taylor(b):
 rows=[((2*x+3)/(4*x-5),2,4),((x+2)*s.log(3*x-7),3,4),(s.sin(2*x+1)**2,-1,5),((x-2)*s.cos(x-3),2,5),
 ((3*x+5)**R(1,3),1,4),((2*x+5)*s.exp(2*x+3),-2,4),((3*x-4)/(x-5),2,4),((x*x+x)*s.log(2*x+1),0,5),
 (s.sin(4*x-3),1,5),(s.cos(x+2)**2,-1,5),((4*x+12)**R(1,4),1,4),((x+2)*s.exp(x*x+x),-1,4),
 ((x*x-4)/(2*x+1),2,4),(x*s.log((5-2*x)**R(1,3)),2,4),((2*x-3)*s.sin(x+3),-2,5),
 (s.cos(2*x+6)**2,-4,5),((x+2)*s.sqrt(3*x+4),4,4),((x-7)*s.exp(4*x-2),1,5),
 ((3*x+2)/(x-6),5,4),((2*x-9)*s.log(4*x+1),1,4),(s.sin(3*x-2)**2,2,5),((3*x+4)*s.cos(2*x-1),3,5),
 ((2*x-5)**R(1,3),16,4),((2*x*x+5)*s.exp(3*x-2),1,5),((x*x-4)/(2*x+1),-1,4),
 ((x*x+7*x)*s.log(4*x+3),1,4),((x+2)*s.sin(x+2),2,5),((2*x+1)*s.cos(3*x-5),2,5),
 ((x+12)**R(1,4),4,4),((-x+4)*s.exp(x+3),-2,5)]
 h=s.Symbol('h',real=True)
 for i,(f,a,degree) in enumerate(rows,1):
  coefficients=[s.simplify(s.diff(f,x,k).subs(x,a)/s.factorial(k)) for k in range(degree+1)]
  polynomial=sum(c*h**k for k,c in enumerate(coefficients))
  independent=s.series(f.subs(x,a+h),h,0,degree+1).removeO()
  assert s.simplify(polynomial-independent)==0
  task=add(b,18,i,41 if i<=14 else 42,11,'Разложение Тейлора',r'f(x)='+tex(f)+r',\quad x_0='+str(a)+r',\quad n='+str(degree),ans(polynomial),
   four(r'f(x_0+h)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}h^k+o(h^n)',
    r'h=x-('+str(a)+r'),\quad f(x_0+h)='+tex(f.subs(x,a+h)),
    r'\begin{gathered}'+r'\\'.join(r'c_{'+str(k)+r'}='+tex(c) for k,c in enumerate(coefficients))+r'\end{gathered}',
    r'f(x_0+h)='+tex(polynomial)+r'+o(h^{'+str(degree)+'})',
    ['Нужен многочлен со всеми членами вплоть до степени n включительно: остаток o(h^n).','Сдвигаем центр в ноль.','Коэффициент cₖ — производная порядка k в центре, делённая на k!.','Верни h=x−x₀, если записываешь ответ в исходной переменной.']),
   kind='expression',variables=['h'],instruction='Введи многочлен Тейлора через h = x − x₀, без остатка o(h^n). Сохрани все члены до указанной степени включительно.')
  record(b,task,'independent SymPy series equals derivative coefficient construction',str(polynomial))

def extrema(b):
 z=s.Symbol('z',real=True)
 rows=[2*x*x+y*y+z*z-x*y-3*x+4*y+2*z,x*x+3*y*y+z*z-x*z-2*x+3*y,
 -9*x*x-6*y*y-11*z*z+3*x*y+5*x*z-8*y*z,-4*x*x-3*y*y-z*z-2*x*y+y*z,
 x*x+y*y+2*z*z+y*z+2*z-3*y,2*x*x+R(3,2)*y*y+z*z-x*y+2*x*z+y*z-y+2*z,
 -5*x*x-y*y-3*z*z+x*z+y*z-2*x*y+6*z,2*x*x+y*y+3*z*z+x*y+x*z-4*x-2*y+z,
 x*x+R(3,2)*y*y+2*z*z+x*y+x*z-4*x-2*y+z,-x*x-y*y-5*z*z+R(1,2)*x*y+x*z-2*x+4*y,
 2*x*x+y*y+R(3,2)*z*z-x*z+2*x*y+y*z-3*y,5*x*x+y*y+5*z*z+2*x*y-x*z-R(1,2)*y*z-10*x,
 5*x*x+y*y+5*z*z+2*x*y-x*z-y*z-4*x+2*y,-4*x*x-y*y-5*z*z+x*y+x*z-2*y*z-2*y,
 -2*x*x-y*y-z*z+x*y-2*z+x-4*y,-x*x-3*y*y-z*z+x*z+x-6*y+z,
 2*x*x+y*y+3*z*z+2*x*z+2*x-4*y,-3*x*x-4*y*y-5*z*z+2*y*z-2*x*y+6*x,
 x*x+5*y*y+z*z+2*x*y-x*z-y*z-10*y,x*x+2*y*y+5*z*z+x*y+4*y*z-4*z,
 -2*x*x-5*y*y-5*z*z+2*x*z+4*y*z-2*x*y-4*x,-5*x*x-6*y*y-4*z*z+2*x*y+2*x*z-8*z,
 3*x*x+4*y*y+5*z*z+2*x*y-2*y*z-8*y,4*x*x+6*y*y+5*z*z-2*x*z-2*y*z+10*z,
 9*x*x+6*y*y+11*z*z-3*x*y-5*x*z+8*y*z,x*x+17*y*y+3*z*z+2*x*y-x*z-7*y*z,
 -x*x-17*y*y-3*z*z+x*z+7*y*z-2*x*y,-9*x*x-6*y*y-11*z*z+3*x*y+5*x*z-8*y*z,
 2*x*x+y*y+3*z*z+x*y+x*z-4*x-2*y+z,5*x*x+y*y+z*z+2*x*y-x*z-R(1,2)*y*z-10*x]
 for i,f in enumerate(rows,1):
  vars=(x,y,z);gradient=s.Matrix([s.diff(f,v) for v in vars]);H=s.hessian(f,vars)
  point=tuple(H.inv()*(-gradient.subs({x:0,y:0,z:0})))
  sub=dict(zip(vars,point));assert gradient.subs(sub)==s.zeros(3,1)
  minors=[H[:k,:k].det() for k in (1,2,3)]
  typ='minimum' if all(d>0 for d in minors) else 'maximum' if all((-1)**k*minors[k-1]>0 for k in (1,2,3)) else 'saddle'
  value=s.simplify(f.subs(sub));typelabel={'minimum':'минимум','maximum':'максимум','saddle':'седловая точка'}[typ]
  fs=[field('point','Стационарная точка (x;y;z)','('+';'.join(map(ans,point))+')','points'),field('value','Значение u в этой точке',ans(value)),
      field('type','Тип: 1 — минимум, 2 — максимум, 3 — седло',str({'minimum':1,'maximum':2,'saddle':3}[typ]))]
  task=add(b,26,i,55 if i<=13 else 56 if i<=28 else 57,11,'Экстремум трёх переменных',r'u='+tex(f),json.dumps({q['id']:q['answer'] for q in fs}),
   four(r'\nabla u=0,\quad H=(u_{ij}),\quad\Delta_k=\det H_{1:k,1:k}',
    r'\nabla u='+tex(gradient),r'H='+tex(H)+r',\quad(\Delta_1,\Delta_2,\Delta_3)='+tex(s.Tuple(*minors)),
    r'M='+tex(s.Tuple(*point))+r',\quad u(M)='+tex(value)+r',\quad\text{'+typelabel+'}',
    ['При положительной определённости H — минимум; при отрицательной — максимум; при неопределённости — седло.',
     'Реши три линейных уравнения для координат стационарной точки.','Для минимума все угловые миноры положительны. Для максимума знаки −,+,−.','Для квадратичной функции определённый гессиан даёт также глобальный экстремум.']),
   kind='fields',fields=fs,instruction='Найди стационарную точку, значение функции и классифицируй её по гессиану.')
  record(b,task,'exact gradient zero and Sylvester principal minors',f'{point}; {value}; {typ}; minors={minors}')
