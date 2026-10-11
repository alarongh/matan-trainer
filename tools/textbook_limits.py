from textbook_common import *

def populate(b):
 # Task 2. Factorials and sums are reduced explicitly, preserving original prompts.
 rows=[
 ((3*n**2-7*n+1)/(2-5*n-6*n**2),-R(1,2)),
 (((2-n)**2-(1+n)**2)/((3+n)**2-(4-n)**2),-R(3,7)),
 (3/(n+2)-5/(2*n+1),0),
 ((2*n**2+5)/(4*n+1)-(n**2+4)/(2*n+3),R(5,8)),
 ((s.sqrt(n*n+1)+n)**2/(27*n**6+1)**R(1,3),R(4,3)),
 ((10*n**3-s.sqrt(n**3+2))/(s.sqrt(4*n**6+3)-n),5),
 ((n*n*s.sin(n*n))**R(1,3)/(n+1),0),
 (3*n*s.cos(s.factorial(n))/(n**4+5*n-9)**R(1,3),0),
 ((3**n+1000)/(3**n+1),1),
 (((-2)**n+3**n)/((-2)**(n+1)+3**(n+1)),R(1,3)),
 ((4**n+2*5**(n+1))/(3**n+3*5**(n-1)+s.sin(n)),R(50,3)),
 (((n*n+3)/(n*n))**(8*n),1),
 (((1-n)/(3-n))**(2*n-1),s.exp(4)),
 (((n*n+1)/(n*n))**n,1),
 (s.sqrt(n*n+n)-n,R(1,2)),
 (s.sqrt(n*n-2*n-1)-s.sqrt(n*n-7*n+3),R(5,2)),
 (((1+n)**2)**R(1,3)-((n-1)**2)**R(1,3),0),
 ((n**3-4*n*n-n)**R(1,3),s.oo),
 (n**R(3,2)*(s.sqrt(n**3+1)-s.sqrt(n**3-2)),R(3,2)),
 ((n+3+4/((n+1)*(n+2)))/(2*n+4)/(1+7/((n+1)*(n+2))),R(1,2)),
 ((7*n+5)/(2*n+2),R(7,2)),
 ((1/(3*n)+3*n+1)/(n-1),3),
 (n*(n+1)/2/(n-n*n+3),-R(1,2)),
 (n*(n+1)/(n*n),1),
 (2-2**(-n),2),
 ((1-(-R(1,5))**n)/6,R(1,6)),
 (2**((1-3**(-n))/2),s.sqrt(2)),
 (s.sqrt(n*n-5*n+6)-s.sqrt(n*n-2*n+9),-R(3,2)),
 (1-1/(n+1),1),
 (R(1,2)*(1-1/(2*n+1)),R(1,2))]
 original={
  7:r'\frac{\sqrt[3]{n^2\sin n^2}}{n+1}',8:r'\frac{3n\cos(n!)}{\sqrt[3]{n^4+5n-9}}',
  20:r'\frac{(n+3)!+4n!}{(2n+4)((n+2)!+7n!)}',
  21:r'\frac{((2n+1)!+(2n+2)!)(7n+5)}{(2n+3)!}',
  22:r'\frac{(3n-1)!+(3n+1)!}{(3n)!(n-1)}',
  23:r'\frac{1+2+\cdots+n}{n-n^2+3}',24:r'\frac{2+4+\cdots+2n}{1+3+\cdots+(2n-1)}',
  25:r'1+\frac12+\cdots+\frac1{2^n}',26:r'\frac15-\frac1{25}+\cdots+\frac{(-1)^{n+1}}{5^n}',
  27:r'\sqrt[3]2\sqrt[9]2\cdots\sqrt[3^n]2',
  29:r'\frac1{1\cdot2}+\frac1{2\cdot3}+\cdots+\frac1{n(n+1)}',
  30:r'\frac1{1\cdot3}+\frac1{3\cdot5}+\cdots+\frac1{(2n-1)(2n+1)}'}
 for i,(f,v) in enumerate(rows,1):
  page=8 if i<=3 else 9 if i<=17 else 10
  if i in (7,8):
   bound=1/n**R(1,3) if i==7 else 3*n/(n**4+5*n-9)**R(1,3)
   task=add(b,2,i,page,2,'Последовательность · оценка',r'\lim_{n\to\infty}'+original[i],'0',four(
    r'|\sin t|\le1,\quad|\cos t|\le1,\quad |a_n|\le b_n,\ b_n\to0\Rightarrow a_n\to0',
    r'|a_n|\le'+tex(bound),limtex(bound,n,s.oo)+r'=0',r'\boxed0'))
   record(b,task,'squeeze bound with symbolic limit',str(s.limit(bound,n,s.oo)))
   continue
  task=limit_card(b,2,i,page,f,s.oo,s.sympify(v),2,'Последовательности · пособие',
   formula=r'\sum_{k=1}^n k=\frac{n(n+1)}2,\quad\sum_{k=0}^n q^k=\frac{1-q^{n+1}}{1-q},\quad (a+b)(a-b)=a^2-b^2',
   var=n,directions=('+',))
  if i in original:
   task['prompt']=r'\lim_{n\to\infty}\left('+original[i]+r'\right)'
   task['stages'][1]['blocks']=[block('Раскрываем факториалы или используем сумму прогрессии. Дроби 1/(k(k+1)) раскладываются в 1/k−1/(k+1).',tex(f))]

 # Task 4. Elementary algebraic limits.
 root=lambda u,k:s.real_root(u,k)
 rows=[
 ((3*x+7)**3*(x-2*x*x)**2/((27*x**5+4*x+1)*(2-4*x)**2),s.oo,R(1,4)),
 (((3*x+1)**3-(3*x-1)**3)/((x+1)**2+(x-1)**2),s.oo,27),
 (s.sqrt(5+16*x*x)/(16*x*x+s.sqrt(x+s.sqrt(x)))**R(1,4),s.oo,s.oo),
 ((x*x**R(1,6)+(35*x**10+1)**R(1,5))/((x+x**R(1,4))*(x**3-1)**R(1,3)),s.oo,35**R(1,5)),
 ((5*x*x+4*x-1)/((27*x**6+1)**R(1,3)-1),s.oo,R(5,3)),
 ((s.sqrt(x)+5*x)/((x**3+1)**R(1,3)+s.sin(x)),s.oo,5),
 ((root(x**3+7,3)+root(x*x+2*x,3))/(17*x+4*s.cos(7*x)),s.oo,R(1,17)),
 (None,None,None),
 ((x*x+5*x+6)/(x*x+4*x+3),-3,R(1,2)),
 ((x**3-3*x+2)/(x**4-4*x+3),1,R(1,2)),
 ((x**3-3*x-2)/(x*x-x-2)**2,-1,-R(1,3)),
 ((x*x-7*x+6)/(x**4-1),1,-R(5,4)),
 ((x**4-1)/(2*x**4-x*x-1),1,R(2,3)),
 ((s.sqrt(5*x-2)-s.sqrt(8))/(x*x-4),2,5/(16*s.sqrt(2))),
 ((s.sqrt(1+x*x)-s.sqrt(1-x*x))/(3*x*x-x**4),0,R(1,3)),
 ((x*s.sqrt(x)-8)/(s.sqrt(x)-2),4,12),
 ((x**R(1,4)-2)/(s.sqrt(x)-4),16,R(1,4)),
 (((9*x)**R(1,3)-3)/(s.sqrt(3+x)-s.sqrt(2*x)),3,-2*s.sqrt(6)/3),
 ((s.sqrt(9+2*x)-5)/(x**R(2,3)-4),8,R(3,5)),
 (((25+x)**R(1,3)-(29-x)**R(1,3))/(x-s.sqrt(2*x)),2,R(4,27)),
 ((x**R(2,3)-2*x**R(1,3)+1)/(x-1)**2,1,R(1,9)),
 ((2*x-1)/(5*x+7)-(1+2*x*x)/(2+5*x*x),s.oo,0),
 (1/(2-x)-12/(8-x**3),2,-R(1,2)),
 (3*x*x/(2*x+1)-(2*x-1)*(3*x*x+x+2)/(4*x*x-1),s.oo,-R(1,2)),
 (x+root(1-x**3,3),s.oo,0),
 (x-root(4-x**3,3),s.oo,s.oo),
 (None,None,None),
 (x*(s.sqrt(x*x+1)-x),s.oo,R(1,2)),
 (s.sqrt(x**4+8*x*x+3)-s.sqrt(x**4+x*x),s.oo,R(7,2)),
 (root(x**3-2*x*x+3,3)-x,s.oo,-R(2,3))]
 for i,(f,p,v) in enumerate(rows,1):
  page=12 if i<=13 else 13 if i<=26 else 14
  if f is None:
   f=(5**x+6**x)/(5**x-6**x) if i==8 else s.sqrt(x*x-5*x+6)-x
   values=[-1,1] if i==8 else [-R(5,2),s.oo]
   task=add(b,4,i,page,4,'Два направления бесконечности',r'f(x)='+tex(f),json.dumps({'plus':ans(values[0]),'minus':ans(values[1])}),
    four(r'\sqrt{x^2}=|x|,\quad (a/b)^x\to0\ (0<a<b,\ x\to+\infty)',
     tex(f),r'\begin{gathered}x\to+\infty:\ '+tex(values[0])+r'\\x\to-\infty:\ '+tex(values[1])+r'\end{gathered}',
     r'\boxed{L_+='+tex(values[0])+r',\ L_-='+tex(values[1])+'}'),kind='fields',
     fields=[field('plus','При x→+∞',ans(values[0])),field('minus','При x→−∞',ans(values[1]))],
     instruction='Вычисли оба предела, как указано в пособии.')
   for point,value in zip([s.oo,-s.oo],values):record(b,task,'100-digit numeric direction check',numeric_limit(f,x,point,value,('+',)))
  else:
   num,den=s.fraction(s.together(f))
   first=tex(s.factor(f))
   if i in (14,15,18,19,28,29):first=r'\frac{('+tex(num)+r')('+tex(num).replace('-','+')+r')}{('+tex(den)+r')('+tex(num).replace('-','+')+r')}'
   # The exact rationalization below is generated from the two radical terms.
   if i in (14,15,18,19):
    terms=s.Add.make_args(s.expand(num));conjugate=terms[0]-terms[1] if len(terms)==2 else None
    if conjugate is not None:first=tex(s.Mul(num,conjugate,evaluate=False))+r'\big/\left('+tex(s.Mul(den,conjugate,evaluate=False))+r'\right)'
   if i in (28,29):
    a=s.sqrt(x*x+1) if i==28 else s.sqrt(x**4+8*x*x+3)
    c=x if i==28 else s.sqrt(x**4+x*x)
    first=tex((x if i==28 else 1)*(a*a-c*c)/(a+c))
   reduced=s.cancel(f)
   if i==14:reduced=5/((x+2)*(s.sqrt(5*x-2)+s.sqrt(8)))
   if i==15:reduced=2/((3-x*x)*(s.sqrt(1+x*x)+s.sqrt(1-x*x)))
   if i==16:reduced=x+2*s.sqrt(x)+4
   if i==17:reduced=1/(x**R(1,4)+2)
   if i==18:
    aa=(9*x)**R(1,3);reduced=-9*(s.sqrt(3+x)+s.sqrt(2*x))/(aa*aa+3*aa+9)
   if i==19:
    aa=x**R(2,3);reduced=2*(aa*aa+4*aa+16)/((x+8)*(s.sqrt(9+2*x)+5))
   if i==20:
    aa=(25+x)**R(1,3);bb=(29-x)**R(1,3);reduced=2*(x+s.sqrt(2*x))/(x*(aa*aa+aa*bb+bb*bb))
   if i==21:reduced=1/(x**R(2,3)+x**R(1,3)+1)**2
   key=None
   if p!=s.oo:
    rn,rd=s.fraction(reduced);nn=s.simplify(rn.subs(x,p));dd=s.simplify(rd.subs(x,p))
    if dd!=0 and nn.is_finite and dd.is_finite:key=r'\begin{gathered}f(x)='+tex(reduced)+r'\\x\to '+tex(p)+r':\quad\frac{'+tex(nn)+'}{'+tex(dd)+'}='+tex(v)+r'\end{gathered}'
   if i==25:
    aa=s.real_root(1-x**3,3);first=r'a=\sqrt[3]{1-x^3},\quad(x+a)(x^2-xa+a^2)=1';key=r'\frac1{x^2-xa+a^2}\to0'
   if i==26:first=r'x-\sqrt[3]{4-x^3}=x[1+(1-4/x^3)^{1/3}]';key=r'x(1+1+o(1))\to+\infty'
   if i==28:key=r'\frac1{\sqrt{1+1/x^2}+1}\to\frac12'
   if i==29:key=r'\frac{7+3/x^2}{\sqrt{1+8/x^2+3/x^4}+\sqrt{1+1/x^2}}\to\frac72'
   if i==30:
    first=r'a=\sqrt[3]{x^3-2x^2+3},\quad a-x=\frac{-2x^2+3}{a^2+ax+x^2}';key=r'a/x\to1,\quad\frac{-2+3/x^2}{(a/x)^2+a/x+1}\to-\frac23'
   task=limit_card(b,4,i,page,f,p,s.sympify(v),first=first,key=key,formula=r'a^2-b^2=(a-b)(a+b),\quad a^3-b^3=(a-b)(a^2+ab+b^2),\quad a^4-b^4=(a-b)(a+b)(a^2+b^2)',directions=('+',) if p==s.oo else ('-','+'))
   if i==25:task['prompt']=r'\lim_{x\to\infty}(x+\sqrt[3]{1-x^3})'
   if i==26:task['prompt']=r'\lim_{x\to\infty}(x-\sqrt[3]{4-x^3})'
   if i==30:task['prompt']=r'\lim_{x\to\infty}(\sqrt[3]{x^3-2x^2+3}-x)'

 # Task 5. Infinitesimal equivalents, shifted points and logarithms.
 rows=[
 (s.sin(3*x)**2/(1-s.cos(x)),0,18),
 ((s.cos(4*x)-1)/(x*s.atan(x)),0,-8),
 (((1+s.tan(x))**10-1)/s.asin(5*x),0,2),
 (s.sin(x-2)/(x**3-8),2,R(1,12)),
 (s.atan(x-5)/s.asin(x*x-25),5,R(1,10)),
 ((x-2)*s.cot((x-2)/5),2,5),
 ((x-s.pi/2)*s.tan(x),s.pi/2,-1),
 ((1-s.cos(x-3))/((x-3)*s.tan((x-3)/2)),3,1),
 (s.cos(2*x)/(4*x-s.pi),s.pi/4,-R(1,2)),
 (s.sin(3*s.pi*x)/s.sin(8*s.pi*x),2,R(3,8)),
 (s.tan(5*x)/s.sin(3*x),s.pi,-R(5,3)),
 (s.sin(6*s.pi*x)/s.sin(s.pi*x),1,-6),
 ((s.tan(2*x)-s.sin(2*x))/x**3,0,4),
 ((s.cos(5*x)-s.cos(3*x))/s.atan(x*x),0,-8),
 ((1-2*s.cos(x))/s.sin(x-s.pi/3),s.pi/3,s.sqrt(3)),
 ((2**s.asin(x)-1)/(3**s.atan(x)-1),0,s.log(2)/s.log(3)),
 ((s.exp(2*x)-s.exp(-2*x))/s.log(1+3*s.sin(x)),0,R(4,3)),
 ((s.exp(4*x*x)-s.exp(x*x))/s.log(1+3*s.asin(x)**2),0,1),
 ((4**(4*x*x)-4**(x*x))/s.log(s.cos(x)),0,-6*s.log(4)),
 (s.asin(x/(x+1))/s.log(1-2*x/(3+x*x)),0,-R(3,2)),
 (((1+s.atan(x)**2)**R(1,4)-1)/s.sin(3*x)**2,0,R(1,36)),
 ((s.log(5-2*x)-s.log(5))/s.asin(3*x),0,-R(2,15)),
 ((s.log(3-x)-s.log(2))/s.sin(x-1),1,-R(1,2)),
 ((2**(3-x)-4)/((2-x)**R(1,3)-1),1,12*s.log(2)),
 ((7**(x-1)-7)/(5**(3-x)-5),2,-7*s.log(7)/(5*s.log(5))),
 ((s.exp(x-1)-1)/(s.sqrt(x)-1),1,2),
 (s.sin(1/x)/s.tan(s.pi/x),s.oo,1/s.pi),
 (((1+6/x**2)**R(1,3)-1)/(s.cos(3/x)-1),s.oo,-R(4,9)),
 (s.log(s.cos(1/x))/(s.atan(3*x)*s.tan(1/x)**2),s.oo,-1/s.pi),
 (((2**(-x)+1)*(2**(1/x)-1))/((3**(-x)+2)*(3**(1/x)-1)),s.oo,s.log(2)/(2*s.log(3)))]
 formula=r'\sin u\sim u,\ \tan u\sim u,\ \arcsin u\sim u,\ \arctan u\sim u,\quad 1-\cos u\sim u^2/2,\quad a^u-1\sim u\ln a,\quad\ln(1+u)\sim u'
 for i,(f,p,v) in enumerate(rows,1):
  q=s.Symbol('h',positive=True)
  if i==30:
   limit_card(b,5,i,15,f,p,s.sympify(v),topic='Эквивалентности · пособие',formula=formula,
    first=r'\frac{1+2^{-x}}{2+3^{-x}}\to\frac12,\quad 2^{1/x}-1\sim\frac{\ln2}{x},\quad3^{1/x}-1\sim\frac{\ln3}{x}',
    key=r'\frac12\cdot\frac{\ln2/x}{\ln3/x}=\frac{\ln2}{2\ln3}',directions=('+',))
   continue
  transformed=f.subs(x,p+q) if p!=s.oo else f.subs(x,1/q)
  numerator,denominator=s.fraction(s.together(transformed))
  leadnum=numerator.as_leading_term(q);leadden=denominator.as_leading_term(q)
  limit_card(b,5,i,14 if i<=12 else 15,f,p,s.sympify(v),topic='Эквивалентности · пособие',formula=formula,
   first=r'h='+('1/x' if p==s.oo else 'x-('+tex(p)+')')+r'\to0,\quad f='+tex(transformed),
   key=r'f\sim\frac{'+tex(leadnum)+'}{'+tex(leadden)+'}='+tex(s.cancel(leadnum/leadden)),
   directions=('+',) if p==s.oo else ('-','+'),
   notes=['Все эквивалентности применяются при u→0. Разность сначала преобразуем; отдельно заменять слагаемые нельзя.','Переносим точку стремления в ноль или вводим h=1/x.','Выделяем первые ненулевые члены числителя и знаменателя, сокращаем их общую степень h.',''])

 powers(b)

def powers(b):
 # For each item: base, exponent, point, limiting logarithm.
 C=s.cos(x);S=s.sin(x);T=s.tan(x)
 rows=[
 ((2*x-2)/(3*x+4),x,s.oo,-s.oo),((2*x-2)/(3*x+4),x,-s.oo,s.oo),((2*x-2)/(2*x+3),x,s.oo,-R(5,2)),
 ((x*x-2)/(x*x+3),3/(x+1),s.oo,0),((x*x-2)/(x*x+3),x+1,s.oo,0),((x*x-2)/(x*x+3),3*x/(x+1),s.oo,0),
 (6-5/C**2,x*x,0,0),(6-5/C**2,1/x**2,0,-5),(6-11/(2*C**2),1/x**2,0,-s.oo),
 ((1-s.cos(2*x))/(2*x*x),1/x**2,0,-R(1,3)),((1-s.cos(2*x))/x**2,1/x**2,0,s.oo),((1-s.cos(2*x))/(2*x*x),1/(x*x+1),0,0),
 (1+S+x*x,1/x**2,0,'DNE'),(1+x+x*x,1/(1+x),0,0),(1+C+x*x,-1/x**2,0,-s.oo),
 (s.cos(s.pi*x/3),1/(x*x+1),0,0),(s.cos(s.pi*x/3),1/x**2,0,-s.pi**2/18),(s.sin(s.pi*x/3),x/(x*x+2),0,0),
 ((3+5*x)/(3+2*x),1/S,0,1),((3+5*x)/(3+2*x),-x*x,0,0),((3+5*x*x)/(3+2*x*x),-1/x**2,0,-1),
 ((1+2**x)/(1+3**x),1/x,0,s.log(R(2,3))/2),((1+2**x)/(1+3**x),(2*x+3)/(2*x+1),0,0),((1+2**x)/(1+3**x),1/x**2,0,'DNE'),
 (s.sin(2*x)/x,-1/x**2,0,-s.oo),(S/x,-1/x**2,0,R(1,6)),(S/x,(2*x+3)/(x+1),0,0),
 (2-2**(-x*x),-x*x,s.oo,-s.oo),(2-2**(-x*x),1/x**2,0,s.log(2)),(2-2**(-x*x),1/(x-1)**2,1,s.oo),
 (2-s.cos(1/x),x*x*s.atan(x),s.oo,s.pi/4),(2-s.cos(1/x),x*x*s.atan(x),-s.oo,-s.pi/4),(2-C,1/s.atan(x)**2,0,R(1,2)),
 ((4-x)/2,s.atan(1/(x-2))**2,2,0),((4-x)/2,1/s.atan(x-2),2,-R(1,2)),((5-x)/2,s.atan(x-2)**2,2,0),
 ((x-7)/(x+1),-1/(x**R(1,3)-2)**2,8,s.oo),((2*x-7)/(x+1),1/(x**R(1,3)-2),8,R(4,3)),(s.cos(x-8),s.sin(x-8)/(x-8),8,0),
 (s.tan(s.pi/6-x),1/x**2,0,-s.oo),(s.tan(s.pi/4-x),(s.exp(x)-1)/x**2,0,-2),(T,(2*x+3)/(-2*x+3),0,-s.oo),
 (s.tan(x/3),1/C**2,s.pi/2,-s.oo),(s.tan(x/2),1/C,s.pi/2,-1),(T,s.pi/(2*x),s.pi/2,s.oo),
 ((x+2*S)/x,1/x,s.oo,0),((2*x+S)/x,-1/x**2,s.oo,0),((x+2*S)/x,1/x**2,0,s.oo),
 ((2*x-s.atan(x))/(2*x+s.atan(x)),3*x,s.oo,-3*s.pi/2),((2*x-s.atan(x))/(2*x+s.atan(x)),2*x+2,0,-2*s.log(3)),((2-s.atan(x))/(2+s.atan(x)),-3/(x-2)**2,2,s.oo),
 (1+T**2,1/s.log(s.cos(2*x)),0,-R(1,2)),(1+s.atan(x)**2,-s.log(x)**2,s.oo,-s.oo),(1+s.atan(x)**2,s.log(s.cos(2*x)),0,0),
 (4-4**x,(3*x+S)/x,0,4*s.log(3)),(2-2**x,3*x/S**2,0,-3*s.log(2)),(2-2**x,(3*x*x+S)/x,s.oo,'invalid'),
 (3-3**(S**2),5/(s.tan(5*x)*s.sin(2*x)),s.pi,s.oo),(3-3**S,3*x*x/T**2,0,3*s.log(2)),(3-3**(s.sin(s.pi*x)**2),-1/(x-1)**2,1,-s.oo)]
 for index,row in enumerate(rows):
  num=index//3+1;letter='abc'[index%3];number=str(num)+letter
  directions=('+',) if number in ('6c','14c') else ('-',) if number=='15c' else ('-','+')
  note='У предела в пособии не указана сторона; вещественное основание положительно только справа. Рассматриваем естественную область x>0.' if number in ('6c','14c') else 'Вещественное основание положительно около π/2 только слева.' if number=='15c' else ''
  power_card(b,6,number,15+(num+3)//4,*row,directions=directions,note=note)
 rows=[
 ((x-2)/(x+1),x,s.oo,-3),((x-1)/(x+3),x+2,s.oo,-4),((5*x**3+2)/(5*x**3),s.sqrt(x),s.oo,0),
 ((x*x-2*x-3)/(x*x+2*x+1),2*x,s.oo,-8),((3+5*x)/(3+2*x),1/S,0,1),(1+x+x*x,1/(2*x),0,R(1,2)),
 (2-C,1/x**2,0,R(1,2)),(1-s.sin(3*x),1/s.tan(5*x),0,-R(3,5)),(6-5/C**2,1/x**2,0,-5),
 (1+T**2,1/s.log(s.cos(2*x)),0,-R(1,2)),(s.cos(2*x),1/s.tan(3*x)**2,0,-R(2,9)),
 (C,1/s.sin(2*x)**2,2*s.pi,-R(1,8)),((1+2**x)/(1+3**x),1/S,0,s.log(R(2,3))/2),
 (1-x*s.sin(3*x),1/s.log(C),0,6),((x+2)/(x*x+2),1/s.sin(3*x),0,R(1,6)),
 ((x+s.sqrt(x*x+1))/x,s.sqrt(x*x+3),s.oo,s.oo),((3*x-1)/(x+1),1/(s.sqrt(x)-1),1,2),
 (s.sin(2*x)/s.tan(2*x),1/(1-C),0,-4),(s.tan(s.pi/4-x),(s.exp(x)-1)/x**2,0,-2),
 (2-s.exp(x*x),1/(1-s.cos(s.pi*x)),0,-2/s.pi**2),(2-2**x,3*x/S**2,0,-3*s.log(2)),
 ((2*x-7)/(x+1),1/(x**R(1,3)-2),8,R(4,3)),(s.tan(x/2),1/C,s.pi/2,-1),
 (S/s.sin(1),1/s.log(2-x),1,-s.cot(1)),(2*s.exp((x-1)**2)-1,s.pi**2/s.log(s.sin(s.pi*x/2)),1,-16),
 (2-2**(S**2),5/(s.tan(5*x)*s.sin(2*x)),s.pi,-s.log(2)/2),((4-x)/2,2/s.atan(x-2),2,-1),
 (2-s.cos(1/x),x*x*s.atan(x),s.oo,s.pi/4),((2*x-1)/x,s.log(3+2*x)/s.log(3-2*x),1,-s.log(5)/2),
 (2-(x-1)/x,s.sin(s.pi/(2*x))*s.log(2-(x-1)/x),s.oo,0)]
 for i,row in enumerate(rows,1):power_card(b,7,i,21 if i<=10 else 22 if i<=21 else 23,*row)
