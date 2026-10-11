from textbook_common import *

def populate(b):
 L=s.log;S=s.sin;C=s.cos;T=s.tan;Q=s.cot;E=s.exp;P=s.pi
 rows=[
 (L(x)/x,s.oo,0),(L(x*x+3)/(x**4+x*x+1),s.oo,0),(L(1+3**x)/L(1+2**x),s.oo,L(3)/L(2)),
 (L(1+3**x)/L(1+2**x),-s.oo,0),(L(x*x+E(x))/L(x**4+E(2*x)),s.oo,R(1,2)),
 (L(Q(x))/L(x),0,-1),(L(1+x*x)/L(P/2-s.atan(x)),s.oo,-2),
 (L(x)/(1+2*L(S(x))),0,R(1,2)),(P/x/Q(P*x/2),0,P*P/2),
 (L(C(2*x))/S(x)**2,P,-2),((2**x-x*x)/(2-x),2,4-4*L(2)),
 (1/x-1/(E(x)-1),0,R(1,2)),(T(P*x)/(4**x-4),1,P/(4*L(4))),
 (L(x)-s.sqrt(x),s.oo,-s.oo),(E(x)-x*x,s.oo,s.oo),
 (L(T(x))/(P/4-x),P/4,-2),(L(x)*L(x-1),1,0),
 (L(s.sqrt(1+4*x)-2)/(x-2),2,R(2,3)),(None,2,None),
 (L(T(x))/(1-Q(x)),P/4,1),(x*L(x)**2,0,0),(x**3*E(-x),s.oo,0),
 ((1-x)*T(P*x/2),1,2/P),(x*2**x/3**x,s.oo,0),(C(x/2)*L(P-x),P,0),
 (1/S(x)-1/x,0,0),(1/(x-1)-1/L(x),1,-R(1,2)),(1/T(x)-1/S(x),0,0),
 (x/Q(x)-P/(2*C(x)),P/2,-1),(E(1/x)/x**2,0,0)]
 for i,(f,p,v) in enumerate(rows,1):
  if i==19:
   task=b.invalid('textbook-15-19',4,'Область вложенного логарифма',r'\lim_{x\to2-0}(2-x)\ln\ln(2-x)',
    'Сначала проверь вещественную область определения.',
    'При x→2− величина 2−x лежит между 0 и 1. Поэтому ln(2−x)<0, и внешний натуральный логарифм не определён. Исходная запись требует уточнения.',36,ref(15,i,36),
    r'0<2-x<1\Rightarrow\ln(2-x)<0')
   task['sources']=[source(36,'Задача 15, пример 19','textbook')]
   continue
  direction=('-',) if i in (25,30) else ('+',) if i in (6,8,17,21) else ('-','+')
  # The stages show a genuine derivative quotient for finite 0/0 cases.
  num,den=s.fraction(s.together(f))
  first=tex(s.together(f))
  try:
   if p not in (s.oo,-s.oo) and num.subs(x,p)==0 and den.subs(x,p)==0:
    first=r'\frac{'+tex(s.diff(num,x))+'}{'+tex(s.diff(den,x))+'}'
  except:pass
  task=limit_card(b,15,i,35 if i<=14 else 36,f,p,s.sympify(v),formula=r'\lim f/g=\lim f^\prime/g^\prime\quad(0/0\text{ или }\infty/\infty,\ \text{при условиях Лопиталя})',
   first=first,directions=direction,topic='Предел · правило Лопиталя')
  task['instruction']='Введи значение предела. В разборе неопределённость преобразуется в дробь перед применением Лопиталя.'
  if direction!=('-','+') and p not in (s.oo,-s.oo):
   task['prompt']=limtex(f,x,p,'-0' if direction==('-',) else '+0')
 powers=[
 (1-x,C(P*x/2),1,0), (2-x,T(P*x/2),1,2/P),
 (2*s.acos(x)/P,1/x,0,-2/P),(x,S(x),0,0),(T(x),2*x-P,P/2,0),
 (L(x),1/L(2*x),s.oo,0),(T(P*x/4),T(P*x/2),1,-1),
 (x+2**x,1/x,s.oo,L(2)),(2*s.acos(3*x)/P,1/x,0,-6/P),(L(x),1/x,s.oo,0),
 (P-x,C(x/2),P,0),(Q(x),1/L(x),0,-1),(2*s.atan(x)/P,x,s.oo,-2/P),
 (T(x),S(x),0,0),(x,1/L(E(x)-1),0,1),(2*s.acos(x)/P,1/s.asin(x),0,-2/P),
 (1/x,s.asin(x),0,0),(Q(P*x/4),T(P*x/2),1,1),(P-2*s.atan(x),1/x,s.oo,0),
 (2-x/3,T(P*x/6),3,2/P),(Q(x),S(x),0,0),(L(1/x),x,0,0),
 (2*s.acos(x)/P,1/S(2*x),0,-1/P),(T(x),T(2*x),P/4,-1),(1/x,T(x),0,0),
 (E(x)+x,1/x,0,2),(2*s.atan(1/x)/P,1/S(x),0,-2/P),(x*Q(x),-1/x**2,0,R(1,3)),
 (2-x/2,T(P*x/4),2,2/P),(L(2*x),1/L(x),s.oo,0)]
 for i,row in enumerate(powers,1):
  dirs=('-',) if i in (1,5,11) else ('+',) if i in (4,12,14,15,17,21,22,25,27) else ('-','+')
  task=power_card(b,16,i,36 if i<=6 else 37,*row,directions=dirs)
  if dirs!=('-','+'):
   task['prompt']=task['prompt'].replace(r'\to '+tex(row[2]),r'\to '+tex(row[2])+('-0' if dirs==('-',) else '+0'))
   if i==5:task['note']='Рассматриваем подход слева: около π/2 только там tan x>0 для обычной вещественной степени.'
 taylor(b)

def taylor(b):
 L=s.log;S=s.sin;C=s.cos;T=s.tan;E=s.exp;A=s.asin;B=s.atan
 rt=lambda u,k:u**R(1,k)
 # Exact pairs from pages 42–48. sin(x²) and sin²(x) remain distinct.
 rows=[
 ('1a',42,1+T(5*x)-C(x),s.sqrt(1-x*x)-rt(1+x,5),0),
 ('1b',42,E(x)-E(x*x)-S(x),s.sqrt(1+x)-s.sqrt(1+x*x)-L(2+x)+L(2),0),
 ('2a',42,L(1-2*x)+S(3*x),2-E(4*x)-rt(1+x,3),0),
 ('2b',43,E(x)-C(x)+s.sqrt(1+2*x*x)-s.sqrt(1+2*x),L(2+x)-L(2+x*x)-S(x)/2,0),
 ('3a',43,x*E(x)-L(1-x),C(2*x)-s.sqrt(1-x*x),0),
 ('3b',43,rt(1+x,3)-s.sqrt(1+2*x)+L(3+2*x)-L(3),C(2*x)-C(3*x),0),
 ('4a',43,1-S(x*x)-C(3*x),x*(rt(1+x,4)-E(2*x)),0),
 ('4b',43,S(x)+S(x*x)+L(1-x),s.sqrt(4+x)-s.sqrt(4+x*x)-L(4+x)+L(4),0),
 ('5a',43,L(1+x)-x*s.sqrt(1-x)+R(5,8)*x*x,T(x)-x-x*x/3,0),
 ('5b',43,C(x)-E(x)+L(1+x),rt(8+x,3)-rt(8+x*x,3)+L(12),0),
 ('6a',43,rt(x**5+x**4,5)-rt(x**5-x**4,5),s.Integer(1),s.oo),
 ('6b',43,C(2*x)-s.sqrt(1+2*x)+S(x),E(2*x)-rt(1+3*x,3)-S(x),0),
 ('7a',43,x*x*C(1/x)-rt(x*x+1,4),s.Integer(1),s.oo),
 ('7b',44,(1+x)**200-(1+x)**100-L(1+100*x),s.sqrt(1+200*x)-s.sqrt(1+100*x)-L(1+50*x),0),
 ('8a',44,S(4*x*x)-L(1-3*x*x),1-C(x/2),0),
 ('8b',44,(1+x)**100-s.sqrt(1+200*x),L(1+10*x)-S(10*x),0),
 ('9a',44,x*T(3*x)-S(x)**2,x*x*E(x*x/4)+C(5*x)-1,0),
 ('9b',44,rt(1+9*x,3)-C(x)-L(1+3*x),rt(1+16*x,4)-C(2*x)-L(1+4*x),0),
 ('10a',44,x+S(2*x),L(1-3*x)+x*E(x),0),
 ('10b',44,E(3*x)-E(2*x)-E(x)+s.sqrt(1+x*x),x+C(3*x)-C(2*x)-C(x)+s.sqrt(1-2*x),0),
 ('11a',44,x-S(3*x),E(x)-s.sqrt(1-x),0),
 ('11b',44,C(x)-E(3*x)+B(3*x),x*S(x)+L(1-2*x)+B(2*x),0),
 ('12a',44,E(x*x)-C(2*x),S(x)-L(1+x),0),
 ('12b',45,rt(1+100*x,100)+S(x)-B(2*x)-C(x),(1+x/100)**100+B(x)-S(2*x)-C(x/10),0),
 ('13a',45,rt(1+2*x,3)-C(x),L(1-x)-L(1+x),0),
 ('13b',45,E(x)-rt(1+20*x,5)+S(3*x),E(3*x)-rt(1+12*x,4)+L(1-5*x*x),0),
 ('14a',45,E(2*x)-E(5*x),S(3*x)+L(1-x),0),
 ('14b',45,S(x)+A(x)+rt(1-6*x,3)-C(3*x),S(x)-A(x)-rt(1-6*x,3)+E(-2*x),0),
 ('15a',45,x*C(x)-S(2*x),1-rt(1+2*x,4),0),
 ('15b',45,S(2*x)+C(3*x)-A(x)-rt(1+17*x,17),S(2*x)-C(3*x)-A(x)+rt(1-15*x,15),0),
 ('16a',45,2-C(x)-E(x*x),x-L(1+x),0),
 ('16b',45,E(x)+E(2*x)-2*C(x)-3*S(x),s.sqrt(1+2*x)+rt(1-3*x,3)-2*C(x),0),
 ('17a',45,E(-x)-s.sqrt(1+2*x),E(x)-s.sqrt(1-2*x),0),
 ('17b',46,A(2*x)+rt(1-8*x,4)-C(3*x),B(2*x)+rt(1-10*x,5)-C(5*x),0),
 ('18a',46,E(x)-s.sqrt(1+2*x),E(-x)-s.sqrt(1-2*x),0),
 ('18b',46,L(2+x)-L(2)-s.sqrt(1+x)+C(2*x),L(3+x)-L(3)-rt(1+x,3)+C(3*x),0),
 ('19a',46,(1+x)**5-s.sqrt(1+10*x),L(1+7*x)-S(7*x),0),
 ('19b',46,L(1+2*x)-S(x)-E(x)+C(3*x),L(1+5*x)-S(2*x)-E(3*x)+C(6*x),0),
 ('20a',46,E(x)-C(x)-L(1+x),E(2*x)-(1+x)**2,0),
 ('20b',46,L(1+3*x)-B(x)-E(2*x)+C(2*x),L(1+5*x)-A(2*x)-E(3*x)+C(6*x),0),
 ('21a',46,L(1+8*x)-S(x),C(x)+x-1,0),
 ('21b',46,3*x+C(2*x)+S(2*x)-C(5*x)-S(5*x),E(2*x)-E(5*x)-L(1+2*x)+L(1+5*x),0),
 ('22a',46,(1+x)**10-(1+x)**9,1+S(2*x)-E(x),0),
 ('22b',47,(1+x)**10-rt(1+10*x,10)-L(1+9*x),C(2*x)-S(10*x)-E(-10*x),0),
 ('23a',47,E(x)-C(x)-S(x),x-L(1+x),0),
 ('23b',47,B(2*x)-s.sqrt(1+6*x)+L(1+x)+C(2*x),A(3*x)-s.sqrt(1+6*x)+L(1-2*x)+C(x),0),
 ('24a',47,L(1-x)+L(1+x),E(x)-s.sqrt(1+2*x),0),
 ('24b',47,E(3*x)-rt(1+9*x,3)+L(1-2*x*x),E(4*x)-rt(1+16*x,4)+L(1-9*x*x),0),
 ('25a',47,(1+x)**2-s.sqrt(1+4*x),C(x)-E(x*x),0),
 ('25b',47,S(2*x)+C(3*x)-E(4*x)-L(1-2*x),B(4*x)+s.sqrt(1+4*x)-E(6*x),0),
 ('26a',47,1+25*x-(1+x)**24,L(1-x)+S(2*x),0),
 ('26b',47,A(x)+S(2*x)+L(1-3*x),B(x)+C(2*x)-E(x),0),
 ('27a',47,E(x)-S(x)-1,L(1+x)+L(1-x),0),
 ('27b',48,s.sqrt(1+2*x)-rt(1+3*x,3)+L(1-x*x),C(2*x)-C(3*x)+E(2*x*x)-E(3*x*x),0),
 (28,48,s.sqrt(1+4*x)-C(x)+L(1-2*x),s.sqrt(4+x)-2*C(x)-S(x/4),0),
 (29,48,rt(1+9*x,3)-E(x)-L(1+2*x),C(2*x)+S(3*x)-E(3*x),0),
 (30,48,A(x)+rt(1+16*x,4)-E(5*x),B(x)+rt(1+9*x,3)-E(4*x),0)]
 for number,page,num,den,p in rows:
  if number=='6a':
   v=R(2,5);first=r'x[(1+1/x)^{1/5}-(1-1/x)^{1/5}]';key=r'x[(1+\frac1{5x}+o(1/x))-(1-\frac1{5x}+o(1/x))]\to\frac25'
  elif number=='7a':
   # This is a printed divergent limit, not a constant after cancellation.
   v=s.oo;first=r'x^2-\frac12+o(1)-\sqrt{x}(1+o(1))';key=r'x^2-\sqrt x-\frac12+o(1)\to+\infty'
  else:
   pn=s.series(num,x,0,7).removeO().expand();pd=s.series(den,x,0,7).removeO().expand()
   ln=pn.as_leading_term(x);ld=pd.as_leading_term(x)
   v=s.limit(ln/ld,x,0)
   first=r'\begin{gathered}N(x)='+tex(pn)+r'+O(x^7)\\D(x)='+tex(pd)+r'+O(x^7)\end{gathered}'
   # Only show terms through the first nonzero order, avoiding walls of unused coefficients.
   order=max(s.degree(ln,x),s.degree(ld,x)) if ln!=0 and ld!=0 else 3
   pn=s.series(num,x,0,int(order)+1);pd=s.series(den,x,0,int(order)+1)
   first=r'\begin{gathered}N(x)='+tex(pn)+r'\\D(x)='+tex(pd)+r'\end{gathered}'
   key=r'\frac{N(x)}{D(x)}\sim\frac{'+tex(ln)+'}{'+tex(ld)+'}='+tex(s.cancel(ln/ld))
   if v in (s.oo,-s.oo):
    left=s.limit(ln/ld,x,0,dir='-');right=s.limit(ln/ld,x,0,dir='+')
    if left!=right:
     v='DNE';key+=r'\quad L_-='+tex(left)+r',\ L_+='+tex(right)
  task=limit_card(b,19,number,page,num/den,p,v,formula=r'e^u=1+u+u^2/2+\cdots,\ \ln(1+u)=u-u^2/2+\cdots,\ \sin u=u-u^3/6+\cdots,\ (1+u)^\alpha=1+\alpha u+\alpha(\alpha-1)u^2/2+\cdots',
   first=first,key=key,topic='Предел · разложение Тейлора',directions=('+',) if p==s.oo else ('-','+'))
  if p==0:record(b,task,'exact rational Taylor coefficients, first nonzero numerator/denominator terms',str(ln)+' / '+str(ld))
  if v=='DNE':
   for direction,result in [('-',left),('+',right)]:record(b,task,'one-sided divergent Taylor limit, numerical corroboration',numeric_limit(num/den,x,0,result,(direction,)))
   task['stages'][-1]['blocks']=[block('Односторонние пределы различаются.',r'\text{Двусторонний предел не существует.}')]
