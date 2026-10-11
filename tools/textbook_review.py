"""Written work: source-specific reference steps, with honest self-review."""
from textbook_common import *
import math

def review(b,section,number,page,topic,prompt,steps,checklist,**kw):
 task=add(b,section,number,page,11,topic,prompt,'',steps,kind='review',
  instruction='Сначала выполни задание на бумаге. Открывай разбор по шагам и сравнивай свою работу.',
  note='Самопроверка: сайт не оценивает написанное доказательство или рисунок. Отметка сохраняется как работа с разбором.',
  checklist=checklist,**kw)
 record(b,task,'source transcription and explicit self-review; no automatic correctness claim','written work')
 return task

def populate(b):
 discontinuities(b); polar(b)

def discontinuities(b):
 S=s.sin;C=s.cos;L=s.log;E=s.exp;P=s.pi
 rows=[
 (s.Abs(x+3)/(x+3)*x+4,r'x\ne-3',r'\lim_{x\to-3^-}f=7,\quad\lim_{x\to-3^+}f=1','В −3 скачок (разрыв первого рода).'),
 ((x+2)/s.Abs(x+2)*x*x,r'x\ne-2',r'\lim_{x\to-2^-}f=-4,\quad\lim_{x\to-2^+}f=4','В −2 скачок.'),
 (E(1/(x+4)),r'x\ne-4',r'\lim_{x\to-4^-}f=0,\quad\lim_{x\to-4^+}f=+\infty','В −4 разрыв второго рода.'),
 (1/((x+3)*(x-5)),r'x\ne-3,5',r'\begin{gathered}f(-3^-)\to+\infty,\ f(-3^+)\to-\infty\\f(5^-)\to-\infty,\ f(5^+)\to+\infty\end{gathered}','В −3 и 5 разрывы второго рода.'),
 ((3*x*x+x-4)/(3*x*x-x-2),r'x\ne1,-2/3',r'f(x)=\frac{3x+4}{3x+2}\ (x\ne1),\quad\lim_{x\to1}f=7/5','В 1 устранимый разрыв; в −2/3 бесконечный разрыв второго рода.'),
 ((5*x*x-x-6)/(2*x*x-x-3),r'x\ne-1,3/2',r'f(x)=\frac{5x-6}{2x-3}\ (x\ne-1),\quad\lim_{x\to-1}f=11/5','В −1 устранимый; в 3/2 бесконечный разрыв.'),
 (s.atan(1/(1-x)),r'x\ne1',r'\lim_{x\to1^-}f=\pi/2,\quad\lim_{x\to1^+}f=-\pi/2','В 1 скачок.'),
 (S(P/x),r'x\ne0',r'f(1/(1/2+2k))=1,\quad f(1/(3/2+2k))=-1\quad(k\to+\infty)','В 0 колебательный разрыв второго рода: односторонние пределы не существуют.'),
 (x*S(P/x),r'x\ne0',r'|x\sin(\pi/x)|\le |x|\to0','В 0 устранимый: продолжение f(0)=0.'),
 ((s.sqrt(13+x)-4)/(x*x-9),r'x\ge-13,\quad x\ne-3,3',r'f(x)=\frac1{(\sqrt{13+x}+4)(x+3)}\ (x\ne3),\quad\lim_{x\to3}f=1/48','В 3 устранимый, в −3 бесконечный разрыв. На границе −13 функция непрерывна справа.'),
 (S(1/x)/(x-P),r'x\ne0,\pi',r'\sin(1/\pi)\ne0,\quad \sin(1/x)\text{ колеблется при }x\to0','В π бесконечный, в 0 колебательный разрыв второго рода.'),
 (S(1/x)/(P*x-1),r'x\ne0,1/\pi',r'\lim_{x\to1/\pi}\frac{\sin(1/x)}{\pi x-1}=\frac{-\cos(\pi)\pi^2}{\pi}=\pi','В 1/π устранимый; в 0 колебательный разрыв второго рода.'),
 (1-(x+2)*S(1/(x+2)),r'x\ne-2',r'|(x+2)\sin(1/(x+2))|\le|x+2|\to0,\quad f\to1','В −2 устранимый: f(−2)=1.'),
 ((x+2)*s.atan(1/x),r'x\ne0',r'\lim_{x\to0^-}f=-\pi,\quad\lim_{x\to0^+}f=\pi','В 0 скачок.'),
 (s.Abs(x+5)/s.atan(x+5),r'x\ne-5',r'\arctan h\sim h,\quad |h|/h=-1\ (h<0),\quad |h|/h=1\ (h>0)','В −5 скачок с пределами −1 и 1.'),
 (S(1/x)/L(s.Abs(x)),r'x\ne0,-1,1',r'\left|\frac{\sin(1/x)}{\ln|x|}\right|\le\frac1{|\ln|x||}\to0\quad(x\to0)','В 0 устранимый с пределом 0; в ±1 бесконечные разрывы.'),
 (C(1/x)**(-2),r'x\ne0,\quad x\ne\frac1{\pi/2+k\pi},\ k\in\mathbb Z',r'\cos(1/x)=0\iff x=\frac1{\pi/2+k\pi}','В каждой указанной ненулевой точке бесконечный разрыв. В 0 предела нет: на одних последовательностях f=1, на других f растёт без границы.'),
 (1/(E(1/x)-1),r'x\ne0',r'\lim_{x\to0^-}f=-1,\quad\lim_{x\to0^+}f=0','В 0 скачок.'),
 ((6-s.sqrt(32+x))/(x*x-16),r'x\ge-32,\quad x\ne-4,4',r'f(x)=-\frac1{(6+\sqrt{32+x})(x+4)}\ (x\ne4),\quad\lim_{x\to4}f=-1/96','В 4 устранимый; в −4 бесконечный. В −32 непрерывность справа.'),
 (s.tan(1/x),r'x\ne0,\quad x\ne\frac1{\pi/2+k\pi},\ k\in\mathbb Z',r'\cos(1/x)=0\iff x=\frac1{\pi/2+k\pi}','В ненулевых указанных точках бесконечные разрывы; в 0 колебательный разрыв второго рода.'),
 (1/(1-3**(x/(1-x))),r'x\ne0,1',r'\begin{gathered}1-3^{x/(1-x)}\sim-x\ln3\ (x\to0)\\\lim_{x\to1^-}f=0,\quad\lim_{x\to1^+}f=1\end{gathered}','В 0 бесконечный разрыв, в 1 скачок.'),
 (x/S(x),r'x\ne k\pi,\ k\in\mathbb Z',r'\lim_{x\to0}\frac{x}{\sin x}=1','В 0 устранимый; при k ≠ 0 в kπ бесконечный разрыв.'),
 (s.Pow(C(s.sqrt(x))**2,1/x,evaluate=False),r'x>0',r'\ln f=\frac{2\ln|\cos\sqrt x|}{x}\to-1\quad(x\to0^+)','В 0 возможно непрерывное продолжение справа значением e^(−1). Нули cos√x внутри x>0 не являются разрывами: положительная степень стремится к 0.'),
 (E(x*x/(16-x*x)),r'x\ne-4,4',r'\begin{gathered}f(-4^-)\to0,\ f(-4^+)\to+\infty\\f(4^-)\to+\infty,\ f(4^+)\to0\end{gathered}','В ±4 разрывы второго рода.'),
 ((2**(1/x)-1)/(2**(1/x)+1),r'x\ne0',r'\lim_{x\to0^-}f=-1,\quad\lim_{x\to0^+}f=1','В 0 скачок.'),
 (x/(E(x*(x+1))-1),r'x\ne0,-1',r'e^{x(x+1)}-1\sim x(x+1),\quad\lim_{x\to0}f=1','В 0 устранимый; в −1 бесконечный разрыв.'),
 ((1/(x+3)-1/x)/(1/x-1/(x-3)),r'x\ne-3,0,3',r'f(x)=\frac{x-3}{x+3}\quad(x\ne-3,0,3)','В 0 и 3 устранимые, пределы −1 и 0; в −3 бесконечный. Сокращение не возвращает исключённые точки.'),
 (E(-1/x**2)/x,r'x\ne0',r'\lim_{x\to0}\frac{e^{-1/x^2}}x=0','В 0 устранимый: экспонента убывает быстрее любой степени.'),
 (x*E(1/x),r'x\ne0',r'\lim_{x\to0^-}f=0,\quad\lim_{x\to0^+}f=+\infty','В 0 разрыв второго рода.'),
 (x*L(s.Abs(x))**2,r'x\ne0',r'\lim_{x\to0}x\ln^2|x|=0','В 0 устранимый с пределом 0.')]
 for i,(f,domain,limits,note) in enumerate(rows,1):
  task=review(b,8,i,24 if i<=28 else 25,'Непрерывность и разрывы',r'f(x)='+tex(f),[
   stage('Определения',block('Устранимый: два конечных предела равны, но значение отсутствует или другое. Скачок: конечные пределы различны. Второй род: хотя бы один предел бесконечен или не существует.',r'\lim_{x\to a^-}f(x),\quad\lim_{x\to a^+}f(x),\quad f(a)')),
   stage('Исходная область',block('На остальных внутренних точках области элементарные функции непрерывны.',domain)),
   stage('Односторонние пределы',block('Проверяй все исключённые точки. На границе области подход возможен только из области.',limits)),
   stage('Классификация',block(note))],['Все исключённые точки найдены','Односторонние пределы проверены','Тип каждого разрыва указан','Границы области не перепутаны с двусторонними точками'])

def sampled_graph(fn,domain,lo=-12,hi=12,ymax=25,polar=False):
 segments=[];run=[];previous=None
 for j in range(801):
  p=lo+(hi-lo)*j/800
  try:
   q=fn(p)
   if abs(complex(q).imag)>1e-10 or not domain(p):raise ValueError()
   q=float(q)
   if not math.isfinite(q) or abs(q)>ymax:raise ValueError()
   point=[q*math.cos(p),q*math.sin(p)] if polar else [p,q]
   if previous and max(abs(point[k]-previous[k]) for k in (0,1))>ymax/4:
    if len(run)>1:segments.append(run)
    run=[]
   run.append([round(v,6) for v in point]);previous=point
  except (ValueError,ZeroDivisionError,OverflowError,TypeError):
   if len(run)>1:segments.append(run)
   run=[];previous=None
 if len(run)>1:segments.append(run)
 assert segments
 return {'segments':segments,'polar':polar,'caption':('Полярная кривая: только ρ ≥ 0, 0 ≤ φ ≤ 2π.' if polar else 'Обзор графика при −12 ≤ x ≤ 12. Масштаб можно менять; поведение за этим окном проверяй по формулам.')}

def polar(b):
 p=s.Symbol('t',real=True);S=s.sin;C=s.cos;P=s.pi
 rows=[C(3*p+P/4),1+C(p),2+S(p),4*s.tan(p/2),2*C(3*p),s.real_root(C(2*p),3),
  1+C(2*p)**2,5*(1-C(2*p)),2*(1+S(3*p)),S(2*p)**2,s.sqrt(C(P+p)),7*(1+S(p)),
  4*C(2*p),S(p/2),2*S(3*p),3*(2-S(p)),2+S(2*p)**2,1-S(2*p),s.sqrt(4*C(p)),
  5*(1+C(3*p)),4*(1-C(4*p)),2+C(p),2*S(p),C(p/2),5*(2-C(p)),s.sqrt(S(-2*p)),
  2*s.tan(p),3*C(2*p)**2,3+2*C(p),4*S(3*p)**2]
 domains=[r'\cos(3\phi+\pi/4)\ge0',r'[0,2\pi]',r'[0,2\pi]',r'[0,\pi)\cup\{2\pi\}',r'\cos3\phi\ge0',r'\cos2\phi\ge0',
  r'[0,2\pi]',r'[0,2\pi]',r'[0,2\pi]',r'[0,2\pi]',r'[\pi/2,3\pi/2]',r'[0,2\pi]',r'\cos2\phi\ge0',
  r'[0,2\pi]',r'\sin3\phi\ge0',r'[0,2\pi]',r'[0,2\pi]',r'[0,2\pi]',r'[0,\pi/2]\cup[3\pi/2,2\pi]',
  r'[0,2\pi]',r'[0,2\pi]',r'[0,2\pi]',r'[0,\pi]\cup\{2\pi\}',r'[0,\pi]',r'[0,2\pi]',
  r'[\pi/2,\pi]\cup[3\pi/2,2\pi]\cup\{0\}',r'[0,\pi/2)\cup[\pi,3\pi/2)\cup\{2\pi\}',r'[0,2\pi]',r'[0,2\pi]',r'[0,2\pi]']
 for i,f in enumerate(rows,1):
  # Explicit real cube root instead of complex principal power.
  fun=(lambda v:math.cbrt(math.cos(2*v))) if i==6 else s.lambdify(p,f,'math')
  def valid(v):
   if i in (4,27) and abs(math.cos(v/(2 if i==4 else 1)))<1e-8:return False
   try:return fun(v)>=-1e-12
   except (ValueError,ZeroDivisionError):return False
  plot=sampled_graph(fun,valid,0,2*math.pi,40,True)
  examples=[]
  for angle in [0,P/6,P/4,P/3,P/2,2*P/3,3*P/4,P,3*P/2,2*P]:
   try:
    if not valid(float(angle)):continue
    val=s.simplify(f.subs(p,angle))
    if val.has(s.zoo,s.nan):continue
    examples.append(tex(angle)+'&'+tex(val))
   except (TypeError,ValueError):continue
  tab=r'\begin{array}{c|c}\phi&\rho\\\hline '+r'\\'.join(examples)+r'\end{array}'
  derivative=s.diff(f,p)
  printed=s.Pow(C(2*p),R(1,3),evaluate=False) if i==6 else f
  review(b,23,i,52,'Полярная кривая',r'\rho='+tex(printed.subs(p,s.Symbol('phi')))+r',\quad\rho\ge0,\quad0\le\phi\le2\pi',[
   stage('Переход к декартовым координатам',block('Не рисуй отрицательные ρ: условие пособия их исключает.',r'x=\rho\cos\phi,\quad y=\rho\sin\phi')),
   stage('Допустимые углы',block('Пересекаем эту область с 0 ≤ φ ≤ 2π. Нули и границы входят, полюса исключаются.',domains[i-1])),
   stage('Опорные точки',block('Отметь эти радиусы на соответствующих лучах. Между ними проверь знак производной радиуса, симметрию, петли и полюса.',tab)),
   stage('Сверка рисунка',block('Это численный обзор. Для неограниченных ветвей окно обрезано; исследуй приближение к полюсам по исходной формуле.')),],
   ['Допустимые углы учтены','Точки с отрицательным ρ исключены','Опорные точки и симметрия проверены','Ветви и поведение у полюсов проверены'],plot=plot)
