from bank_common import *
def populate(b):
 # Bank task 4, including the printed constant sin(2) in example 23.
 E={1:(x*x+4*x+3)/(x*x+x-6),2:(x*x+8*x-48)/(x*x-3*x-4),3:(2-s.sqrt(x-3))/(x*x-49),4:(x*x-2*x+1)/(x**3-x),5:(8*x**3-1)/(6*x*x-5*x+1),6:(s.exp(x)-s.exp(-x))/(s.sin(x)*s.cos(x)),7:1/(1-x)-3/(1-x**3),8:(x*x-3*x-1)/(x*x-2*x-3),9:(x*x-7*x-30)/(x*x+2*x-1),10:(x*x-20*x+125)/(x*x-10*x-375),11:(x*x-6*x+8)/(x*x-5*x+6),12:(x*x-9)/(x*x-3*x),13:(x*x+5*x+6)/(x*x+4*x+3),14:(x**3+3*x*x+2*x)/(x*x-x-6),15:(x*x-5*x+6)/(x*x-2*x),16:(x*x-1)/(x*x+3*x+2),17:(x*x-25)/(x-5),18:(x*x-5*x+6)/(x*x-12*x+20),19:(x*x-6*x+8)/(x*x-8*x+12),20:(x*x-7*x+1)/(x*x-8*x+12),22:s.sqrt(4*x*x-x)-s.sqrt(4*x*x-s.cos(x)),23:s.sin(7*s.pi*x)/s.sin(2),24:s.sin(x)/(s.pi*s.pi-x*x),25:s.sqrt(4*x*x+3*x)+2*x,26:x*x*s.log(s.cos(s.pi/x)),27:x+s.sqrt((x**3+2*x*x)/(x+1)),28:s.sqrt(4*x+s.sqrt(x))-2*s.sqrt(x),29:s.asin(s.sqrt(x*x+x)+x),30:s.sqrt(9*x*x+x)+3*x,31:(x**3-10)/(x**3-20*x*x+100*x),32:(x*x-6*x+8)/(x*x-8*x+12),33:(x*x-2*x-3)/(x*x+2*x-6),34:(x*x-10*x+16)/(x*x-3*x-4),35:1/(1-x)-3/(1-x**3),36:(x*x-10*x+16)/(x*x-3*x-40),37:(x*x+x-2)/(x*x-x-6),38:(x*x+9*x+18)/(x*x+7*x+6),39:(x*x+11*x+30)/(x*x+10*x+24),40:(x*x+10*x+21)/(x*x+9*x+14)}
 points={1:-3,2:4,3:7,4:1,5:R(1,2),6:0,7:1,8:5,9:10,10:25,11:2,12:3,13:-3,14:-2,15:2,16:-1,17:5,18:2,19:2,20:2,22:s.oo,23:1,24:s.pi,25:-s.oo,26:s.oo,27:-s.oo,28:s.oo,29:-s.oo,30:-s.oo,31:10,32:2,33:7,34:8,35:1,36:8,37:-2,38:-6,39:-6,40:-7}
 expected={1:R(2,5),2:R(16,5),3:-R(1,56),4:0,5:6,6:2,7:-1,8:R(9,12),9:0,10:'DNE',11:2,12:2,13:R(1,2),14:-R(2,5),15:-R(1,2),16:-2,17:10,18:R(1,8),19:R(1,2),20:'DNE',22:-R(1,4),23:0,24:1/(2*s.pi),25:-R(3,4),26:-s.pi**2/2,27:-R(1,2),28:R(1,4),29:-s.pi/6,30:-R(1,6),31:s.oo,32:R(1,2),33:R(32,57),34:0,35:-1,36:R(6,13),37:R(3,5),38:R(3,5),39:R(1,2),40:R(4,5)}
 for i,expr in E.items():
  point=points[i];id=f'function-limit-{i:02}';ans=expected[i];page=4 if i<=8 else 5
  prompt=r'\lim_{x\to'+tex(point)+r'}\left('+tex(expr)+r'\right)'
  if ans=='DNE':
   left=s.limit(expr,x,point,dir='-');right=s.limit(expr,x,point,dir='+');assert left!=right
   stages=four(r'\lim_{x\to a}f(x)\text{ существует, если оба односторонних предела совпадают.}',tex(s.factor(s.denom(expr))),r'\lim_{x\to'+tex(point)+r'-}f(x)='+tex(left)+r',\quad\lim_{x\to'+tex(point)+r'+}f(x)='+tex(right),r'\boxed{\text{Двусторонний предел не существует}}')
  else:
   result=s.limit(expr.subs(s.cos(x),0) if i==22 else expr,x,point);b.verify(id,'bounded cosine squeeze' if i==22 else 'symbolic limit vs reference',result,ans)
   if expr.is_rational_function(x):
    num,den=s.fraction(s.together(expr));fact=r'\frac{'+tex(s.factor(num))+r'}{'+tex(s.factor(den))+'}';reduced=tex(s.cancel(expr));formula=r'a^2-b^2=(a-b)(a+b),\quad\frac{(x-a)P(x)}{(x-a)Q(x)}=\frac{P(x)}{Q(x)}\ (x\ne a)'
    key=reduced if s.cancel(expr)!=expr else r'x\to'+tex(point)+r',\quad f(x)='+tex(expr)
   elif expr.has(s.sqrt) or i in [3,22,25,27,28,29,30]:
    formula=r'\sqrt A-\sqrt B=\frac{A-B}{\sqrt A+\sqrt B},\quad\sqrt{x^2}=|x|'
    if i==3:fact=r'-\frac1{(\sqrt{x-3}+2)(x+7)}';key=r'-\frac1{(2+2)(7+7)}'
    elif i==22:fact=r'\frac{-x+\cos x}{\sqrt{4x^2-x}+\sqrt{4x^2-\cos x}}';key=r'\frac{-1+\cos x/x}{\sqrt{4-1/x}+\sqrt{4-\cos x/x^2}}'
    elif i==25:fact=r'\frac{3x}{\sqrt{4x^2+3x}-2x}';key=r'\frac3{-\sqrt{4+3/x}-2}'
    elif i==27:fact=r'\frac{x^2/(x+1)}{\sqrt{(x^3+2x^2)/(x+1)}-x}';key=r'\frac{x/(x+1)}{-\sqrt{(x+2)/(x+1)}-1}'
    elif i==28:fact=r'\frac{\sqrt x}{\sqrt{4x+\sqrt x}+2\sqrt x}';key=r'\frac1{\sqrt{4+1/\sqrt x}+2}'
    elif i==29:fact=r'\sqrt{x^2+x}+x=\frac{x}{\sqrt{x^2+x}-x}';key=r'\frac1{-\sqrt{1+1/x}-1}\to-\frac12'
    else:fact=r'\frac{x}{\sqrt{9x^2+x}-3x}';key=r'\frac1{-\sqrt{9+1/x}-3}'
   else:
    formula=r'\sin u\sim u,\quad e^u-e^{-u}\sim2u,\quad\ln\cos u\sim-u^2/2\quad(u\to0)'
    if i==6:fact=r'\frac{e^x-e^{-x}}x\frac{x}{\sin x}\frac1{\cos x}';key=r'2\cdot1\cdot1'
    elif i==23:fact=r'\sin(7\pi x)\to\sin7\pi=0';key=r'\sin2\ne0'
    elif i==24:fact=r'\sin x=-\sin(x-\pi),\quad\pi^2-x^2=-(x-\pi)(x+\pi)';key=r'\frac{\sin(x-\pi)}{x-\pi}\frac1{x+\pi}'
    else:fact=r'u=\pi/x\to0,\quad x^2\ln\cos(\pi/x)=\pi^2\frac{\ln\cos u}{u^2}';key=r'\ln\cos u\sim-u^2/2'
   stages=four(formula,fact,key,r'\boxed{'+tex(ans)+'}')
  b.add(id,4,'Предел без Лопиталя',prompt,ans if isinstance(ans,str) else answer(ans),stages,page,f'Банк · задача 4 · пример {i}',instruction='Вычисли предел без правила Лопиталя. Если двустороннего предела нет, введи «нет».')
 b.invalid('function-limit-21',4,'Проверка печатного условия',r'\lim_{x\to0}\frac{\ln\cos}{\ln\cos4x}','В числителе напечатано «ln cos» без аргумента.','Не указан аргумент косинуса в числителе.',5,'Банк · задача 4 · пример 21')
 # Bank task 6. Missing arguments remain explicit source issues.
 H={1:(1-x)/s.log(x),2:(s.log(1-x)+s.tan(s.pi*x/2))/s.cot(s.pi*x),3:(s.pi-2*s.atan(x))*s.log(x),6:1/x-1/(s.exp(x)-1),7:(s.exp(x)-s.exp(-x)-2*x)/(x-s.sin(x)),8:(s.exp(x)-s.exp(-x))/(s.sin(x)*s.cos(x)),9:(s.exp(s.tan(x))-s.exp(x))/(s.tan(x)-x),10:(s.exp(x)-x**3/6-x*x/2-x-1)/(s.cos(x)+x*x/2-1),11:x*s.exp(x/2)/(x+s.exp(x)),13:(x-s.pi/2)*s.tan(x),15:s.sqrt(x)*s.log(x)**2,16:1/x-1/(s.exp(x)-1),17:x*(s.exp(1/x)-1),18:s.cot(x)-1/x,19:s.log(x)/s.log(s.sin(x)),20:(x-s.sin(x))/(x-s.tan(x)),31:(s.exp(x*x)-1)/(s.cos(x)-1),32:s.cos(x)*s.log(x-s.pi)/s.log(s.exp(x)-s.exp(s.pi)),33:(s.exp(3*x)-3*x-1)/s.sin(5*x)**2,34:(s.sin(3*x)-3*x*s.exp(x)+3*x*x)/(s.atan(x)-s.sin(x)-x**3/6),35:(s.exp(s.tan(x))-s.exp(x))/(s.tan(x)-x),36:(s.tan(x)-s.sin(x))/x**3,37:s.log(x)/(1+2*s.log(s.sin(x))),38:s.cos(x)*s.log(x-3)/s.log(s.exp(x)-s.exp(3)),39:(x**3-4*x*x+5*x-2)/(x**3-5*x*x+7*x-3),40:s.tan(s.pi*x/2)/s.log(1-x)}
 HP={1:1,2:1,3:s.oo,6:0,7:0,8:0,9:0,10:0,11:s.oo,13:s.pi/2,15:0,16:0,17:s.oo,18:0,19:0,20:0,31:0,32:s.pi,33:0,34:0,35:0,36:0,37:0,38:3,39:1,40:1}
 HA={1:-1,2:-2,3:0,6:R(1,2),7:2,8:2,9:1,10:1,11:0,13:-1,15:0,16:R(1,2),17:1,18:0,19:1,20:-R(1,2),31:-2,32:-1,33:R(9,50),34:18,35:1,36:R(1,2),37:R(1,2),38:s.cos(3),39:R(1,2),40:-s.oo}
 for i,expr in H.items():
  point=HP[i];id=f'advanced-limit-{i:02}';direction='-' if i in [2,40] else '+';a=HA[i]
  result=s.limit(expr,x,point,dir=direction);b.verify(id,'symbolic limit vs reference',result,a)
  if point in [s.oo,-s.oo]:
   formula=r'\frac{\ln x}{x}\to0,\quad\frac{x^m}{e^{cx}}\to0\ (c>0),\quad e^u-1\sim u'
   first={3:r'\pi-2\arctan x=2\arctan(1/x)\sim2/x',11:r'\frac{xe^{x/2}}{x+e^x}=\frac{xe^{-x/2}}{1+xe^{-x}}',17:r'u=1/x,\quad x(e^{1/x}-1)=\frac{e^u-1}{u}'}[i]
   key={3:r'2\ln x/x\to0',11:r'xe^{-x/2}\to0,\quad xe^{-x}\to0',17:r'(e^u-1)/u\to1'}[i]
  elif i in [19,32,37,38]:
   formula=r'\sin u\sim u,\quad e^u-1\sim u,\quad\ln(uv)=\ln u+\ln v\ (u,v>0)'
   first={19:r'\ln\sin x=\ln x+\ln(\sin x/x)',32:r'u=x-\pi\to0+,\quad\ln(e^x-e^\pi)=\pi+\ln u+\ln((e^u-1)/u)',37:r'\ln\sin x=\ln x+\ln(\sin x/x)',38:r'u=x-3\to0+,\quad\ln(e^x-e^3)=3+\ln u+\ln((e^u-1)/u)'}[i]
   key={19:r'\frac{\ln x}{\ln x+o(1)}\to1',32:r'\cos x\to-1,\quad\frac{\ln u}{\ln u+\pi+o(1)}\to1',37:r'\frac{\ln x}{1+2\ln x+o(1)}\to\frac12',38:r'\cos x\to\cos3,\quad\frac{\ln u}{\ln u+3+o(1)}\to1'}[i]
  elif i==40:formula=r'\tan(\pi x/2)\sim\frac2{\pi(1-x)}';first=r'u=1-x\to0+,\quad\frac{2}{\pi u\ln u}';key=r'u\ln u\to0-'
  elif i==15:formula=r'\frac{\ln^m u}{u^c}\to0\ (u\to\infty,\ c>0)';first=r'u=1/\sqrt x\to+\infty';key=r'\sqrt x\ln^2x=4\ln^2u/u\to0'
  elif i==2:formula=r'\tan(\pi x/2)\sim-\frac2{\pi(x-1)},\quad\cot(\pi x)\sim\frac1{\pi(x-1)}';first=r'u=x-1\to0-,\quad u\ln(-u)\to0';key=r'\frac{\pi u\ln(-u)-2}{1}\to-2'
  elif i==39:formula=r'\text{Раскладываем многочлены на множители.}';first=r'\frac{(x-1)^2(x-2)}{(x-1)^2(x-3)}';key=r'\frac{x-2}{x-3}\to\frac12'
  else:
   formula=r'\begin{gathered}e^u=1+u+u^2/2+u^3/6+\cdots\\\sin u=u-u^3/6+\cdots,\quad\cos u=1-u^2/2+\cdots\\\tan u=u+u^3/3+\cdots,\quad\arctan u=u-u^3/3+\cdots\end{gathered}'
   if i==13:first=r'u=x-\pi/2,\quad u\tan(\pi/2+u)=-u\cot u';key=r'u\cot u\to1'
   else:
    num,den=s.fraction(s.together(expr));u=s.Symbol('u',real=True)
    first=tex(s.series(num.subs(x,point+u),u,0,6))+r'\quad\text{(числитель)}'
    key=tex(s.series(den.subs(x,point+u),u,0,6))+r'\quad\text{(знаменатель)}'
  b.add(id,4,'Эквивалентности, Тейлор и Лопиталь',r'\lim_{x\to'+tex(point)+(r'-' if i in [2,40] else r'+' if i in [15,19,32,37,38] else '')+r'}\left('+tex(expr)+r'\right)',answer(a),four(formula,first,key,r'\boxed{'+tex(a)+'}'),6 if i<=20 else 7,f'Банк · задача 6 · пример {i}',instruction='Вычисли предел. Следи за областью определения и стороной приближения.')
 # Roots have arguments tending to ±1: use the derivative of the real root.
 roots={21:(4,3*x+2,9,6*x+3,3*x+1,-R(1,3),R(1,36)),22:(5,2*x-3,7,3*x-5,x-2,2,-R(1,35)),23:(6,9+2*x,5,x+3,x+4,-4,R(8,15)),24:(5,4*x-1,10,6*x-2,2*x-1,R(1,2),R(1,10)),25:(7,4+x,3,7+2*x,x+3,-3,-R(11,21)),26:(5,2*x-7,3,5-x,x-4,4,R(11,15)),27:(5,5+2*x,6,7+3*x,x+2,-2,-R(1,10)),28:(5,7-2*x,8,2*x-5,x-3,3,-R(13,20)),29:(6,3+2*x,5,4+3*x,x*x-1,-1,R(2,15)),30:(3,5*x-4,4,6-5*x,x*x-1,1,R(35,24))}
 for i,(k,A,m,B,D,p,a) in roots.items():
  sign='+' if i==23 else '-';prompt=r'\lim_{x\to'+tex(p)+r'}\frac{\sqrt['+str(k)+']{'+tex(A)+'}'+sign+r'\sqrt['+str(m)+']{'+tex(B)+'}}{'+tex(D)+'}'
  va=1;vb=-1 if i==23 else 1
  da=s.diff(A,x).subs(x,p)/(k*va**(k-1));db=s.diff(B,x).subs(x,p)/(m*vb**(m-1));result=(da+db if i==23 else da-db)/s.diff(D,x).subs(x,p);b.verify(f'advanced-limit-{i:02}','root derivatives vs reference',result,a)
  b.add(f'advanced-limit-{i:02}',4,'Корни и правило Лопиталя',prompt,answer(a),four(r'(\sqrt[k]{u})^\prime=\frac{u^\prime}{k(\sqrt[k]{u})^{k-1}}',r'\sqrt['+str(k)+']{'+tex(A)+r'}\to1,\quad\sqrt['+str(m)+']{'+tex(B)+r'}\to'+str(vb),r'\frac{'+tex(da)+sign+tex(db)+'}{'+tex(s.diff(D,x).subs(x,p))+'}',r'\boxed{'+tex(a)+'}'),7,f'Банк · задача 6 · пример {i}')
 for i,prompt in {4:r'\lim_{x\to0}\frac{\ln\sin}{\ln\sin x}',5:r'\lim_{x\to1}\left(\frac{x}{x-1}-\frac1{\ln}\right)',12:r'\lim_{x\to1}\left(\frac1{x-1}-\frac1{\ln}\right)',14:r'\lim_{x\to1}\left(\frac1{\ln}-\frac1{x-1}\right)'}.items():b.invalid(f'advanced-limit-{i:02}',4,'Неполная печатная запись',prompt,'В источнике отсутствует аргумент одной из функций.','У логарифма или вложенного синуса не указан аргумент. Разные дополнения дают разные пределы.',6,f'Банк · задача 6 · пример {i}')
 # Demo: three additional valid limits; its fourth variant repeats bank 6.21.
 demo=[('demo-limit-1',r'\lim_{x\to0+}\left(\frac2\pi\arctan\frac1x\right)^{1/\sin x}',s.exp(-2/s.pi),r'\arctan(1/x)=\pi/2-\arctan x\quad(x>0)',r'A-1=-\frac2\pi\arctan x',r'L=-\frac2\pi\lim\frac{\arctan x}{\sin x}=-2/\pi'),('demo-limit-2',r'\lim_{x\to+\infty}\frac{\ln\cos(1/x)}{\arctan^3x\,\tan^2(1/x)}',-4/s.pi**3,r'\ln\cos u\sim-u^2/2,\quad\tan u\sim u',r'u=1/x\to0+,\quad\arctan x\to\pi/2',r'\frac{-u^2/2}{(\pi/2)^3u^2}=-4/\pi^3'),('demo-limit-3',r'\lim_{x\to0+}\frac{\ln\sin2x}{\ln\sin x}',s.Integer(1),r'\sin2x=2\sin x\cos x,\quad\ln(ab)=\ln a+\ln b',r'\ln\sin2x=\ln\sin x+\ln(2\cos x)',r'1+\frac{\ln(2\cos x)}{\ln\sin x}\to1')]
 for id,prompt,a,formula,first,key in demo:
  task=b.add(id,4,'Предел из демобилета',prompt,answer(a),four(formula,first,key,r'\boxed{'+tex(a)+'}'),1,'Демо · №4 · вариант '+id[-1]);task['sources']=[source(1,'№4, вариант '+id[-1],'demo')]
 b.find('advanced-limit-21')['sources'].append(source(2,'№4, вариант с корнями','demo'))
