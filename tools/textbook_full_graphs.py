"""Full written graph study in addition to the existing two short exercises."""
from textbook_common import *
from textbook_review import review,sampled_graph
import math

def domain_data(section,i,f,excluded):
 if section==20:
  return s.Complement(s.S.Reals,s.FiniteSet(*excluded))
 if section==21:
  if i in (6,7):
   a=1 if i==6 else 4
   return s.Union(s.Interval(-s.oo,-s.sqrt(a)),s.Interval(s.sqrt(a),s.oo))
  return s.Complement(s.S.Reals,s.FiniteSet(0)) if i>20 and i in (22,26,28,29) else s.S.Reals
 domains={4:s.Interval(1,s.oo),5:s.Union(s.Interval.open(0,1),s.Interval.open(1,s.oo)),
  7:s.Complement(s.S.Reals,s.FiniteSet(0)),8:s.Complement(s.S.Reals,s.FiniteSet(0)),9:s.Complement(s.S.Reals,s.FiniteSet(2)),
  10:s.Complement(s.S.Reals,s.FiniteSet(0)),12:s.Union(s.Interval.open(-s.oo,0),s.Interval.open(3,s.oo)),
  13:s.Complement(s.S.Reals,s.FiniteSet(2)),14:s.Union(s.Interval.open(-s.oo,-4),s.Interval.open(0,s.oo)),
  15:s.Complement(s.S.Reals,s.FiniteSet(1)),17:s.Complement(s.S.Reals,s.FiniteSet(-1)),18:s.Interval.open(0,s.oo),
  20:s.Interval.open(-1,1),21:s.Complement(s.S.Reals,s.FiniteSet(0)),22:s.Complement(s.S.Reals,s.FiniteSet(2)),
  24:s.Union(s.Interval.open(-s.oo,0),s.Interval.open(4,s.oo)),25:s.Union(s.Interval.open(-s.oo,-2),s.Interval.open(0,s.oo)),
  26:s.Interval.open(0,s.oo),28:s.Union(s.Interval.open(0,1),s.Interval.open(1,s.oo)),
  29:s.Union(s.Interval.open(-s.oo,-3),s.Interval.open(0,s.oo)),30:s.Complement(s.S.Reals,s.FiniteSet(-R(7,2)))}
 return domains.get(i,s.S.Reals)

def sign_table(f,domain,crit,excluded):
 # List signs over every domain component split at derivative zero/singular points.
 bounds=sorted(set([s.N(v,16) for v in crit+excluded if v.is_real]),key=float)
 boundaries=[-s.oo]+bounds+[s.oo];rows=[]
 for a,c in zip(boundaries,boundaries[1:]):
  q=(float(c)-max(1,abs(float(c))/2)) if a==-s.oo else (float(a)+max(1,abs(float(a))/2)) if c==s.oo else (float(a)+float(c))/2
  if not bool(domain.contains(q)):continue
  v=s.N(f.subs(x,q),20)
  if not v.is_real or v==0:continue
  left=tex(a) if a in (-s.oo,s.oo) else tex(s.N(a,7));right=tex(c) if c in (-s.oo,s.oo) else tex(s.N(c,7))
  rows.append(r'('+left+';'+right+')&'+('+' if v>0 else '-'))
 return r'\begin{array}{c|c}\text{интервал }x&\text{знак}\\\hline '+r'\\'.join(rows)+r'\end{array}' if rows else ''

def full_graph(b,section,i,page,f,points,lines,d2,original_prompt,excluded=None,critical=None,d1=None,zero_equation=None):
 excluded=list(excluded or []);domain=domain_data(section,i,f,excluded)
 d1=d1 if d1 is not None else s.diff(f,x)
 if critical is None:
  numerator=s.fraction(s.factor(d1))[0]
  critical=[r for r,m in s.Poly(numerator,x).real_roots(multiple=False)]
 critical=list(critical)
 boundaries=[]
 for comp in (domain.args if isinstance(domain,s.Union) else [domain]):
  if isinstance(comp,s.Interval):boundaries += [v for v in [comp.start,comp.end] if v not in (-s.oo,s.oo)]
 for q in boundaries:
  if q not in excluded:excluded.append(q)
 critical=[q for q in critical if bool(domain.contains(q))]
 symmetry='Чётность проверяется вместе с симметрией области; при несимметричной области функция ни чётная, ни нечётная.'
 try:
  symmetric=domain==s.imageset(s.Lambda(x,-x),domain)
  if symmetric:
   symmetry='Функция чётная.' if s.simplify(f.subs(x,-x)-f)==0 else 'Функция нечётная.' if s.simplify(f.subs(x,-x)+f)==0 else 'Функция ни чётная, ни нечётная.'
 except (TypeError,NotImplementedError):pass
 intercept=r'\text{Нули: }'+(zero_equation or tex(f)+r'=0')
 if bool(domain.contains(0)):
  intercept+=r',\quad f(0)='+tex(f.subs(x,0))
 else:intercept+=r',\quad 0\notin D_f'
 signs=sign_table(d1,domain,critical,excluded)
 # For the two oscillatory functions use the exact periodic sign criteria.
 if section==22 and i in (11,16):
  signs=(r'f^\prime=e^{-x}(\cos x-\sin x)' if i==11 else r'f^\prime=e^x(\cos x-\sin x)')+r',\quad x=\pi/4+k\pi\quad(k\in\mathbb Z)'
 extrema=[]
 for q in critical:
  try:
   qf=float(q);near=[float(v) for v in critical+excluded if v!=q and v.is_real]
   delta=min([.0001]+[abs(qf-v)/4 for v in near if abs(qf-v)>1e-12])
   if not bool(domain.contains(qf-delta)) or not bool(domain.contains(qf+delta)):continue
   left=float(d1.subs(x,qf-delta));right=float(d1.subs(x,qf+delta))
   if left*right<0:
    extrema.append(('max' if left>0 else 'min',q,s.simplify(f.subs(x,q))))
  except (TypeError,ValueError,ZeroDivisionError):continue
 extrematex=r'\begin{gathered}'+r'\\'.join(r'\text{'+typ+r'}:\ ('+tex(s.N(q,9))+';'+tex(s.N(v,9))+')' for typ,q,v in extrema)+r'\end{gathered}' if extrema else r'\text{Проверить границы области и особые точки отдельно.}'
 if section==22 and i in (11,16):
  extrematex=r'x_k=\pi/4+k\pi,\quad k\in\mathbb Z;\quad\text{чётные }k:\max,\quad\text{нечётные }k:\min'
 if section==22 and i==4:
  extrematex+=r'\quad\text{минимум на границе ОДЗ: }(1;0)'
 inflection=b.find(f'textbook-{section:02}-{i}-inflection');asymptote=b.find(f'textbook-{section:02}-{i}-asymptotes')
 derivativecuts=[q for q in points if isinstance(q,s.Basic)]+critical
 convexity=sign_table(d2,domain,derivativecuts,excluded) if not (section==22 and i in (11,16)) else tex(d2)+r'\quad\text{знак периодического множителя}'
 fn=s.lambdify(x,f,'math')
 # Compile interval membership once instead of doing symbolic work for every pixel.
 components=domain.args if isinstance(domain,s.Union) else [domain]
 intervals=[comp for comp in components if isinstance(comp,s.Interval)]
 def member(q):
  if domain==s.S.Reals:return True
  if intervals:return any(float(a.start)<q<float(a.end) or q==float(a.start) and not a.left_open or q==float(a.end) and not a.right_open for a in intervals)
  return bool(domain.contains(q))
 plot=sampled_graph(fn,member,ymax=25)
 stages=[
  stage('План исследования',block('На бумаге: ОДЗ, чётность, пересечения с осями, пределы на границах и асимптоты, интервалы монотонности и экстремумы, выпуклость и перегибы. Затем рисунок.',r'f^\prime:+\to-\Rightarrow\max,\quad f^\prime:-\to+\Rightarrow\min')),
  stage('Область и симметрия',block(symmetry,r'D_f='+tex(domain))),
  stage('Пересечения с осями',block('Реши указанное уравнение только в исходной области. Исключённые точки не становятся нулями после сокращения.',intercept)),
  stage('Границы и асимптоты',block('У границ ОДЗ вычисли односторонние пределы. Для наклонной асимптоты проверяй обе бесконечности.',r'k=\lim f(x)/x,\quad b=\lim(f(x)-kx)'),*asymptote['stages'][-1]['blocks']),
  stage('Монотонность и экстремумы',block('На интервалах с плюсом функция возрастает, с минусом убывает. Нули производной без смены знака не являются экстремумами. Координаты ниже округлены.',r'f^\prime='+tex(d1)),block('',signs),block('',extrematex)),
  stage('Выпуклость и перегибы',block('Плюс f″ означает выпуклость вниз (чашка), минус — вверх. Для перегиба нужна непрерывность и смена знака; особые точки также проверяются.',r'f^{\prime\prime}='+tex(d2)),block('',convexity),*inflection['stages'][-1]['blocks']),
  stage('Сверка рисунка',block('Сверь все ветви, граничные точки и дырки по исходной ОДЗ. Численный рисунок показывает конечное окно; сам по себе он не доказывает исследование.'))]
 task=review(b,section,str(i)+'-full',page,'Полное исследование и график',original_prompt,stages,
  ['Исходная ОДЗ и чётность проверены','Пересечения с осями найдены','Пределы на границах и все асимптоты проверены','Монотонность и экстремумы указаны','Выпуклость и перегибы проверены','Все ветви рисунка согласованы с исследованием'],plot=plot)
 task['sources']=[source(page,f'Задача {section}, пример {i}','textbook')]
 task['meta']=ref(section,i,page)+' · полное исследование'
