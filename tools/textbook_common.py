"""Source-specific builders; expressions are transcribed, not OCR-parsed."""
from bank_common import *
import mpmath as mp

def tex(expr):
 return s.latex(expr,inv_trig_style='full',ln_notation=True)

def ans(v):
 if v == 'DNE': return v
 if isinstance(v,s.Basic):
  v=v.replace(lambda q:q.is_Pow and q.exp.is_Rational and q.exp.q==3,
   lambda q:s.Function('cbrt')(q.base)**q.exp.p)
 return answer(v).replace('atan(', 'arctan(').replace('asin(', 'arcsin(').replace('acos(', 'arccos(').replace('log(', 'ln(').replace('Abs(', 'abs(')

def ref(section,number,page):
 return f'Учебное пособие · задача {section} · пример {number} · стр. {page}'

def add(b,section,number,page,group,topic,prompt,value,steps,**kw):
 id=f'textbook-{section:02}-{number}'
 task=b.add(id,group,topic,prompt,value,steps,page,ref(section,number,page),**kw)
 task['sources']=[source(page,f'Задача {section}, пример {number}','textbook')]
 return task

def record(b,task,method,details):
 b.verification.append({'id':task['id'],'method':method,'result':details,'passed':True})

def limtex(expr,var,point,direction=''):
 p=tex(point)+direction
 return r'\lim_{'+tex(var)+r'\to '+p+'}'+tex(expr)

def numeric_limit(expr,var,point,expected,directions=('-', '+'),power=False):
 """Independent high precision checks of convergence; not a symbolic proof."""
 if expected=='DNE':return None
 stable=expr.replace(lambda v:v.func==s.log and v.args[0].is_Add and s.Integer(1) in v.args[0].args,
  lambda v:s.Function('logone')(v.args[0]-1))
 fn=s.lambdify(var,stable,[{'logone':mp.log1p},'mpmath'])
 with mp.workdps(100):
  target=mp.mpf(str(s.N(expected,95))) if expected not in (s.oo,-s.oo) else None
  results=[]
  for direction in directions:
   samples=[]
   for k in ((7,13,21) if point in (s.oo,-s.oo) else (5,9,13)):
    v=(mp.mpf(10)**k if point==s.oo else -mp.mpf(10)**k if point==-s.oo else mp.mpf(str(s.N(point,95)))+(-1 if direction=='-' else 1)*mp.mpf(10)**(-k))
    try:
     z=fn(v)
     if abs(mp.im(z))>mp.mpf('1e-30'): continue
     samples.append(mp.re(z))
    except (ValueError,ZeroDivisionError):continue
   if not samples: continue
   last=samples[-1]
   if target is not None:
    error=abs(last-target)
    if error >= mp.mpf('2e-5')*max(1,abs(target)):
     exact=s.limit(expr,var,point,dir=direction)
     assert s.simplify(exact-expected)==0,(expr,point,expected,direction,mp.nstr(last,15),exact)
     results.append('symbolic slow-convergence confirmation: '+str(exact))
   else:
    sign=1 if expected==s.oo else -1
    assert sign*last>20 and (len(samples)<2 or sign*last>sign*samples[0]),(expr,point,expected,mp.nstr(last,15))
   results.append(mp.nstr(last,12))
  assert results,(expr,point,'no valid samples')
  return ', '.join(results)

def limit_card(b,section,number,page,expr,point,value,group=4,topic='Предел из пособия',formula=None,first=None,key=None,var=x,directions=('-', '+'),notes=None):
 prompt=limtex(expr,var,point)
 formula=formula or r'\frac{P(x)}{Q(x)}=\frac{P(x)/x^m}{Q(x)/x^m},\quad a^2-b^2=(a-b)(a+b)'
 first=first or tex(s.factor(expr))
 key=key or (limtex(s.cancel(expr),var,point)+r'='+tex(value))
 steps=four(formula,first,key,r'\boxed{'+tex(value)+'}',notes or ['Выбираем преобразование по виду выражения.','Преобразуем выражение до подстановки.','Вычисляем предел уже после сокращения или выделения главных членов.',''])
 task=add(b,section,number,page,group,topic,prompt,ans(value),steps)
 evidence=numeric_limit(expr,var,point,value,directions)
 if evidence:record(b,task,'mpmath, 100 digits, three shrinking distances (numerical corroboration)',evidence)
 return task

def power_card(b,section,number,page,A,B,point,L,directions=('-', '+'),note='',u_equiv=None):
 """L is the checked limiting logarithm; exp(L) is the final answer."""
 prompt=limtex(s.Pow(A,B,evaluate=False),x,point)
 if L=='invalid':
  task=add(b,section,number,page,3,'Проверка области степени',prompt,'2',four(
   r'a^b=\exp(b\ln a)\quad(a>0)',tex(A),
   r'2-2^x<0\quad(x>1)',r'\text{Вещественная степень не определена на хвосте.}',
   ['Проверяем область определения до применения замечательного предела.','При x→+∞ основание отрицательно.','Произвольная вещественная степень отрицательного основания не определена на всём хвосте.','Печатное условие требует уточнения области или смысла степени.']),
   kind='choice',instruction='Позволяет ли запись вычислять обычный вещественный предел на всём хвосте?',options=[{'value':'1','label':'Да'},{'value':'2','label':'Нет, нужно уточнить условие'}])
  b.issue(task['id'],'При x→+∞ основание отрицательно; обычная вещественная степень на хвосте не определена.')
  return task
 u=s.factor(A-1)
 logexpr=B*s.log(A)
 result='DNE' if L=='DNE' else s.exp(L)
 try:base=s.limit(A,x,point)
 except:base=None
 baseone=base==1
 formula=r'\begin{gathered}a^b=e^{b\ln a}\ (a>0),\quad\ln(1+u)\sim u\ (u\to0)\\a^h-1\sim h\ln a,\quad\sin h\sim h,\quad1-\cos h\sim h^2/2\quad(h\to0)\end{gathered}'
 first=r'A(x)=1+u(x),\quad u(x)='+tex(u) if baseone else r'L=\lim '+tex(B)+r'\ln\left('+tex(A)+r'\right)'
 keyexpr=s.factor(u*B) if baseone else logexpr
 key=limtex(keyexpr,x,point)
 if baseone and point not in (s.oo,-s.oo):
  h=s.Symbol('h',positive=True)
  try:
   leading=u.subs(x,point+h).as_leading_term(h)
   exp_leading=B.subs(x,point+h).as_leading_term(h)
   factor=s.simplify(keyexpr.subs(x,point+h))
   key=r'\begin{gathered}h=x-('+tex(point)+r')\to0,\quad u\sim '+tex(leading)+r'\\uB\sim\left('+tex(leading)+r'\right)\left('+tex(exp_leading)+r'\right)\\L='+limtex(factor,h,0)+r'\end{gathered}'
  except (ValueError,NotImplementedError):pass
 if u_equiv:
  key=r'\begin{gathered}'+u_equiv+r'\\ L='+key+r'\end{gathered}'
 if L=='DNE':
  left=numeric_limit(logexpr,x,point,-s.oo,('-',)) if str(number) in ('5a',) else numeric_limit(logexpr,x,point,s.oo,('-',))
  right=numeric_limit(logexpr,x,point,s.oo,('+',)) if str(number) in ('5a',) else numeric_limit(logexpr,x,point,-s.oo,('+',))
  key+=r'\quad L_-\ne L_+'
  last=r'\text{Двусторонний предел не существует.}'
 else:
  key+=r'='+tex(L)
  last=r'\boxed{'+tex(result)+'}'
 steps=four(formula,first,key,last,[
  'Сначала проверяем знак основания и его предел. Обозначим предел всего выражения через M, а предел его логарифма через L.',
  'Если основание стремится к 1, вычитаем из него 1. В остальных случаях используем логарифм основания.',
  'При u→0 можно заменить ln(1+u) на u в произведении. Константы сохраняются; к нулю уходят только бесконечно малые слагаемые.',
  'Возвращаемся от логарифма: M=e^L. При разных односторонних пределах общего ответа нет.'])
 task=add(b,section,number,page,3,'Степенной предел · пособие',prompt,ans(result),steps,note=note)
 if L=='DNE':record(b,task,'one-sided logarithms, 100-digit numerical divergence corroboration',left+' / '+right)
 else:
  ev=numeric_limit(logexpr,x,point,L,directions)
  record(b,task,'limiting logarithm, 100-digit numerical corroboration',ev)
 return task

def derivative_card(b,section,number,page,f,var=x,logarithmic=False):
 raw=s.diff(f,var)
 derivative=s.factor(raw)
 if logarithmic:
  intermediate=s.diff(s.log(f),var).expand()
  first=r'\ln|y|='+tex(s.expand_log(s.log(f),force=True))
  key=r'\frac{y^\prime}{y}='+tex(intermediate)
  formula=r'(\ln|y|)^\prime=\frac{y^\prime}{y},\quad(u^v)^\prime=u^v\left(v^\prime\ln u+v\frac{u^\prime}{u}\right)\ (u>0)'
 else:
  first=r'y^\prime='+tex(raw)
  key=r'y^\prime='+tex(derivative)
  formula=r'(uv)^\prime=u^\prime v+uv^\prime,\quad (u/v)^\prime=(u^\prime v-uv^\prime)/v^2,\quad F(u)^\prime=F^\prime(u)u^\prime'
 task=add(b,section,number,page,6,'Логарифмическое дифференцирование' if logarithmic else 'Производная · пособие',r'y='+tex(f),ans(derivative),
  four(formula,first,key,r'\boxed{y^\prime='+tex(derivative)+'}',[
   'Работаем внутри области определения исходной функции.','Дифференцируем внешнюю функцию и умножаем на производную внутренней; произведения и дроби разбираем отдельно.',
   'Приводим подобные слагаемые и выносим общие множители. При логарифмическом способе умножаем результат на исходную функцию.',
   'Ответ — выражение для производной.']),kind='expression',variables=[str(var)],instruction="Введи y′ как выражение. Используй arctan, arcsin, cot; переменная "+str(var)+'.')
 # Independent finite difference at a valid source-domain point.
 fn=s.lambdify(var,f,'mpmath');df=s.lambdify(var,derivative,'mpmath');valid=0
 with mp.workdps(60):
  for sample in [.03,.17,.37,.83,1.29,2.17,3.41,4.73,6.19,10.1]:
   try:
    p=mp.mpf(str(sample));v=fn(p)
    if abs(mp.im(v))>mp.mpf('1e-30'):continue
    numeric=mp.diff(fn,p);exact=df(p)
    assert abs(numeric-exact)<mp.mpf('1e-30')*max(1,abs(exact)),(task['id'],sample)
    valid+=1
   except (ValueError,ZeroDivisionError):continue
 assert valid,(task['id'],'no derivative verification samples')
 record(b,task,'symbolic differentiation + independent mpmath numerical derivative',f'{valid} domain-valid samples')
 return task
