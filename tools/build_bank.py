import sys,json,shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

import sympy as s
def latex(expr):return s.latex(expr,inv_trig_style='full')
ROOT=Path(__file__).resolve().parents[1]; (ROOT/'data').mkdir(exist_ok=True);(ROOT/'sources').mkdir(exist_ok=True)
files=[Path(title) for title in ['Задачи для подготовки к экзамену. Мат. анализ 1 семестр.pdf','Математический_анализ_1_сем_25_26_разбор_билета 28.11.2025.pdf','Математический_анализ_1сем_25-26_демо.pdf','Теоретические вопросы к экзамену.pdf']]
tasks=[]; checks=[]
def block(note='',tex=''):return {'note':note,'tex':tex}
def stage(title,*blocks):return {'title':title,'blocks':list(blocks)}
def source(file,page,number):return {'file':file,'page':page,'label':number}
def add(id,group,topic,tex,answer,stages,src=None,origin='source',kind='number',note=''):
 tasks.append(dict(id=id,group=group,topic=topic,prompt=tex,answer=answer,stages=stages,sources=src or [],origin=origin,kind=kind,note=note))

# All 30 functions, visually transcribed from page 2 of the task bank.
P=[
(r'\frac{x^2}{\sqrt{x^2-1}}','1',r'D=(-\infty,-1)\cup(1,+\infty)',r'f(-x)=\frac{(-x)^2}{\sqrt{(-x)^2-1}}=f(x)','Знаменатель содержит корень: x² − 1 строго больше нуля.'),
(r'\frac{2^x-1}{2^x+1}','2',r'D=\mathbb R',r'f(-x)=\frac{2^{-x}-1}{2^{-x}+1}=\frac{1-2^x}{1+2^x}=-f(x)','Умножь числитель и знаменатель на 2ˣ; 2ˣ + 1 всегда положительно.'),
(r'\frac{\sin x}{x}','1',r'D=\mathbb R\setminus\{0\}',r'f(-x)=\frac{-\sin x}{-x}=f(x)','Два минуса в дроби сокращаются.'),
(r'\sqrt{x^2-3x+5}+\sqrt{x^2+3x+5}','1',r'D=\mathbb R',r'x^2\pm3x+5=(x\pm3/2)^2+11/4>0;\quad f(-x)=f(x)','При замене x на −x корни меняются местами.'),
(r'\frac{x-1}{x-1}','3',r'D=\mathbb R\setminus\{1\}',r'-1\in D,\qquad 1\notin D','После сокращения исключённая точка x = 1 сохраняется. ОДЗ несимметрична.'),
(r'\sqrt{x-1}\cdot\sqrt{x+1}','3',r'D=[1,+\infty)',r'x-1\ge0,\quad x+1\ge0\quad\Longrightarrow\quad x\ge1','Оба корня должны существовать одновременно. ОДЗ несимметрична.'),
(r'\frac{x^2}{\sqrt{3-x}+\sqrt{3+x}}','1',r'D=[-3,3]',r'f(-x)=\frac{x^2}{\sqrt{3+x}+\sqrt{3-x}}=f(x)','На концах отрезка один корень равен нулю, другой положителен.'),
(r'\frac{3x+2}{x^2-x+1}+\frac{3x-2}{x^2+x+1}','2',r'D=\mathbb R',r'f(-x)=-\frac{3x-2}{x^2+x+1}-\frac{3x+2}{x^2-x+1}=-f(x)','Оба знаменателя положительны: их дискриминанты равны −3.'),
(r'\cos(x-\pi/2)-x^2','3',r'D=\mathbb R',r'f(x)=\sin x-x^2,\qquad f(-x)=-\sin x-x^2','При x = π/2 обе части ненулевые; сумма ненулевой нечётной и ненулевой чётной частей не обладает чётностью.'),
(r'x^2+\frac{1+\cos x}{2}','1',r'D=\mathbb R',r'f(-x)=x^2+\frac{1+\cos x}{2}=f(x)','Оба слагаемых чётные.'),
(r'x^2e^{-x}','3',r'D=\mathbb R',r'f(-x)=x^2e^x;\quad f(-1)=e,\quad f(1)=e^{-1}','Значения при ±1 не равны и не противоположны.'),
(r'\frac{4x}{4+x^2}','2',r'D=\mathbb R',r'f(-x)=\frac{-4x}{4+x^2}=-f(x)','Знаменатель всегда положителен.'),
(r'\frac{x}{3}-\frac3x','2',r'D=\mathbb R\setminus\{0\}',r'f(-x)=-\frac{x}{3}+\frac3x=-f(x)','ОДЗ симметрична, оба слагаемых нечётные.'),
(r'\frac{\sqrt{1-x^2}}{|x|}','1',r'D=[-1,0)\cup(0,1]',r'f(-x)=\frac{\sqrt{1-x^2}}{|x|}=f(x)','Условия: −1 ≤ x ≤ 1 и x ≠ 0.'),
(r'\sqrt{x-1}\cdot\sqrt{x+1}','3',r'D=[1,+\infty)',r'x\ge1,\quad x\ge-1\quad\Longrightarrow\quad x\ge1','В источнике повторяется пример 6. Сохраняем исходный номер.'),
(r'x(x+1)(x-1)','2',r'D=\mathbb R',r'f(x)=x^3-x,\qquad f(-x)=-x^3+x=-f(x)','Раскрой (x + 1)(x − 1) по разности квадратов.'),
(r'\frac{x^3}{2(x+1)^2}','3',r'D=\mathbb R\setminus\{-1\}',r'1\in D,\qquad-1\notin D','ОДЗ несимметрична: знаменатель обращается в ноль при −1.'),
(r'x-\sqrt[3]{x^2}','3',r'D=\mathbb R',r'f(-x)=-x-\sqrt[3]{x^2};\quad f(1)=0,\ f(-1)=-2','Кубический корень из x² чётный; при ±1 уже видно нарушение обоих равенств.'),
(r'\frac{2x}{\sqrt{x^2+1}}','2',r'D=\mathbb R',r'f(-x)=\frac{-2x}{\sqrt{x^2+1}}=-f(x)','Подкоренное выражение строго положительно.'),
(r'\frac{x^3(x^2-1)}{x^2-1}','2',r'D=\mathbb R\setminus\{-1,1\}',r'f(x)=x^3\ (x\ne\pm1),\qquad f(-x)=-f(x)','После сокращения остаются две симметричные исключённые точки.'),
(r'\frac{\sqrt{\sin^2x}}{1+\cos2x}','1',r'D=\mathbb R\setminus\{\pi/2+\pi k:k\in\mathbb Z\}',r'\sqrt{\sin^2x}=|\sin x|,\quad1+\cos2x=2\cos^2x;\quad f(-x)=f(x)','Числитель и знаменатель чётные; исключённые точки симметричны.'),
(r'\frac{1-\cos x}{1+\cos x}','1',r'D=\mathbb R\setminus\{(2k+1)\pi:k\in\mathbb Z\}',r'f(-x)=\frac{1-\cos x}{1+\cos x}=f(x)','Знаменатель не равен нулю.'),
(r'x\sin x','1',r'D=\mathbb R',r'f(-x)=(-x)(-\sin x)=f(x)','Произведение двух нечётных функций чётно.'),
(r'\frac{\cos2x-x^2}{\sin x}','2',r'D=\mathbb R\setminus\{\pi k:k\in\mathbb Z\}',r'f(-x)=\frac{\cos2x-x^2}{-\sin x}=-f(x)','Чётный числитель делится на нечётный знаменатель; ОДЗ симметрична.'),
(r'\frac{x-1}{x-1}','3',r'D=\mathbb R\setminus\{1\}',r'-1\in D,\qquad1\notin D','В источнике повторяется пример 5. Исключённая точка остаётся после сокращения.'),
(r'\frac{x}{2}\tan^2x','2',r'D=\mathbb R\setminus\{\pi/2+\pi k:k\in\mathbb Z\}',r'f(-x)=\frac{-x}{2}(-\tan x)^2=-f(x)','Квадрат тангенса чётный, множитель x нечётный.'),
(r'\sin x+x','2',r'D=\mathbb R',r'f(-x)=-\sin x-x=-f(x)','Сумма двух нечётных функций нечётна.'),
(r'3^{\cos x}','1',r'D=\mathbb R',r'f(-x)=3^{\cos(-x)}=3^{\cos x}=f(x)','Аргумент показательной функции чётный.'),
(r'3-\cos(\pi/2+x)\sin(\pi-x)','1',r'D=\mathbb R',r'f(x)=3+\sin^2x,\qquad f(-x)=f(x)','Используй cos(π/2 + x) = −sin x и sin(π − x) = sin x.'),
(r'\frac12\cos2x\sin(3\pi/2-2x)+3','1',r'D=\mathbb R',r'f(x)=3-\frac12\cos^22x,\qquad f(-x)=f(x)','Используй sin(3π/2 − 2x) = −cos 2x.'),
]
for i,(expr,answer,domain,minus,note) in enumerate(P,1):
 label={'1':'Функция чётная.','2':'Функция нечётная.','3':'Функция ни чётная, ни нечётная.'}[answer]
 src=[source('bank',2,f'Задача 2, пример {i}')]
 if i==4:src += [source('demo',1,'№1'),source('solutions',1,'№1')]
 add(f'parity-{i:02}',1,'Чётность и ОДЗ',r'f(x)='+expr,answer,[
 stage('Формулы и порядок проверки',block('Сначала исходная ОДЗ и её симметрия, затем подстановка −x.',r'f(-x)=f(x)\ \text{или}\ f(-x)=-f(x)'),block('Для чётного корня подкоренное ≥ 0; знаменатель ≠ 0. После сокращения исключения сохраняются.')),
 stage('Область определения',block(note,domain)),
 stage('Проверка симметрии и подстановка',block('',minus)),
 stage('Ответ',block(label,r'\boxed{'+answer+'}')),
 ],src,kind='choice')

n=s.symbols('n',positive=True);R=s.Rational
def root(v,k=2):return v**R(1,k)
# Expressions match the printed originals, including duplicates 3/22 and 6/35.
E={
1:root(n*n+n)-n,2:(3*n+2*root(27*n**3+n,3))/(4*n+root(n*n+5)),3:(5**n-2)*(2**n+5)/(10**n+1),4:(root(n*n+1)+n)**2/root(n**6+1,3),
5:(root(n**3-2*n*n+1)+root(n**4+1,3))/(root(n**6+6*n**5+2,4)-root(n**7+3*n**3+1,5)),
6:(root(n**5+2,4)-root(n*n+1,3))/(root(n**4+2,5)-root(n**3+1)),
7:2*(1-R(1,2)**(n+1))/(R(3,2)*(1-R(1,3)**(n+1))),8:n*(n+1)/2/n**2,9:n*(n+1)/2/(n+2)-n/2,
10:(10*n**3-root(n*n+2))/(root(4*n**6+3)-n),11:(root(n+2)-root(n*n+2))/(root(4*n**4+1,4)-root(n**4-1,3)),
12:(4*n*n-7)/(2*n*n-root(9*n*n+5*n**3+4)),13:root(n*n+2*n)-n,14:root(n*n+3*n)/(7*n+2),
15:(root(n*n+n)-root(9*n*n+2*n))/(root(n**3+1,3)-root(8*n**3+2,3)),16:(root(n+7)-root(2*n*n-3))/(root(2*n*n-1,3)-root(n**4+2,4)),
17:(3*n+7)/root(3*n*n+n+1,3),18:root(4*n*n+7*n)/(3*n+1),19:(2*n*n-3*n+1)/(n*root(9*n*n+7)),20:root(9*n*n+7*n)/(n+3),
21:(3*n+s.sin(2*n))/(4*n+root(n*n+5)),22:(5**n-2)*(2**n+5)/(10**n+1),23:root(n*n+4*n)-root(n*n+n),
24:(n*n-s.sin(2*n))/(2*n*n+root(n**3+1)),25:(n+s.sin(n))/n,26:(3**n+2**(1/n))/(3**(n+1)+4**(1/n)),
27:(2*n*n+s.sin(5*n))/(n*n+root(4*n**4+5*n)),28:(6**n+5)/((2**n+3)*(3**n+2)),29:root(4*n*n+3*n)-root(4*n*n-3*n),30:((2*n+5)/(2*n))**n,
31:(root(n*n+1)+n)**2/root(8*n**6+1,3),32:(root(n**3+1)+n)/(n**R(3,2)+1),33:(root(n**4+10,4)+2*n)**2/root(3*n**4+1),
34:(1-14**(-n+1))/(1-14**(-n-1)),35:(root(n**5+2,4)-root(n*n+1,3))/(root(n**4+2,5)-root(n**3+1)),
36:((n+2)**3-(n-2)**3)/(95*n**3+39*n),37:(2*n-1)/(5*n+7)-(1+2*n**3)/(2+5*n**3),38:root(n+2)-root(n),
39:n**R(3,2)*(root(n**3+1)-root(n*n-2)),40:(2**n+3**n)/(2**n-3**n)}
answers={1:'1/2',2:'9/5',3:'1',4:'4',5:'1',6:'0',7:'4/3',8:'1/2',9:'-1/2',10:'5',11:'0',12:'2',13:'1',14:'1/7',15:'2',16:'sqrt(2)',17:'infinity',18:'2/3',19:'2/3',20:'3',21:'3/5',22:'1',23:'3/2',24:'1/2',25:'1',26:'1/3',27:'2/3',28:'1',29:'3/2',30:'exp(5/2)',31:'2',32:'1',33:'3*sqrt(3)',34:'1',35:'0',36:'0',37:'0',38:'0',39:'infinity',40:'-1'}

# Each exercise has its own intermediate expressions, not a generic final answer.
S={
1:('Сопряжённое',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\frac{n^2+n-n^2}{\sqrt{n^2+n}+n}',r'\frac1{\sqrt{1+1/n}+1}',r'\frac1{1+1}=\frac12'),
2:('Степени и корни',r'\sqrt[k]{n^p}=n^{p/k}\quad(n>0)',r'\sqrt[3]{27n^3+n}=n\sqrt[3]{27+1/n^2}',r'\frac{3+2\sqrt[3]{27+1/n^2}}{4+\sqrt{1+5/n^2}}',r'\frac{3+2\cdot3}{4+1}=\frac95'),
3:('Показательные функции',r'a^nb^n=(ab)^n;\quad |q|<1\Rightarrow q^n\to0',r'(5^n-2)(2^n+5)=10^n+5\cdot5^n-2\cdot2^n-10',r'\frac{1+5/2^n-2/5^n-10/10^n}{1+1/10^n}',r'\frac{1+0-0-0}{1+0}=1'),
4:('Квадрат скобки и корни',r'\sqrt[k]{n^p}=n^{p/k}',r'(\sqrt{n^2+1}+n)^2=n^2(\sqrt{1+1/n^2}+1)^2',r'\frac{(\sqrt{1+1/n^2}+1)^2}{\sqrt[3]{1+1/n^6}}',r'(1+1)^2=4'),
5:('Корни разных порядков',r'\sqrt[k]{n^p}=n^{p/k}',r'n^{3/2},\ n^{4/3};\qquad n^{6/4},\ n^{7/5}',r'\frac{\sqrt{1-2/n+1/n^3}+n^{-1/6}\sqrt[3]{1+1/n^4}}{\sqrt[4]{1+6/n+2/n^6}-n^{-1/10}\sqrt[5]{1+3/n^4+1/n^7}}',r'\frac{1+0}{1-0}=1'),
6:('Корни разных порядков',r'\sqrt[k]{n^p}=n^{p/k}',r'n^{5/4}-n^{2/3};\qquad n^{4/5}-n^{3/2}',r'\frac{n^{-1/4}\sqrt[4]{1+2/n^5}-n^{-5/6}\sqrt[3]{1+1/n^2}}{n^{-7/10}\sqrt[5]{1+2/n^4}-\sqrt{1+1/n^3}}',r'\frac{0-0}{0-1}=0'),
7:('Геометрические суммы',r'1+q+\cdots+q^n=\frac{1-q^{n+1}}{1-q}',r'S_1=2(1-2^{-(n+1)}),\quad S_2=\frac32(1-3^{-(n+1)})',r'\frac{2(1-2^{-(n+1)})}{(3/2)(1-3^{-(n+1)})}',r'\frac2{3/2}=\frac43'),
8:('Арифметическая сумма',r'1+2+\cdots+n=\frac{n(n+1)}2',r'\frac1{n^2}\cdot\frac{n(n+1)}2',r'\frac{1+1/n}{2}',r'\frac12'),
9:('Сумма с последующим вычитанием',r'1+2+\cdots+n=\frac{n(n+1)}2',r'\frac{n(n+1)}{2(n+2)}-\frac n2=\frac{n(n+1)-n(n+2)}{2(n+2)}',r'-\frac{n}{2(n+2)}=-\frac1{2+4/n}',r'-\frac12'),
10:('Старшие степени',r'\sqrt{n^6}=n^3\quad(n>0)',r'\sqrt{4n^6+3}=n^3\sqrt{4+3/n^6}',r'\frac{10-n^{-2}\sqrt{1+2/n^2}}{\sqrt{4+3/n^6}-1/n^2}',r'\frac{10}{2}=5'),
11:('Корни разных порядков',r'\sqrt[k]{n^p}=n^{p/k}',r'\sqrt{n+2}\sim n^{1/2},\ \sqrt{n^2+2}\sim n;\quad\sqrt[3]{n^4-1}\sim n^{4/3}',r'\frac{n^{-5/6}\sqrt{1+2/n}-n^{-1/3}\sqrt{1+2/n^2}}{n^{-1/3}\sqrt[4]{4+1/n^4}-\sqrt[3]{1-1/n^4}}',r'\frac{0-0}{0-1}=0'),
12:('Сравнение степеней',r'\sqrt{n^p}=n^{p/2}',r'\sqrt{9n^2+5n^3+4}=n^{3/2}\sqrt{5+9/n+4/n^3}',r'\frac{4-7/n^2}{2-n^{-1/2}\sqrt{5+9/n+4/n^3}}',r'\frac42=2'),
13:('Сопряжённое',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\frac{2n}{\sqrt{n^2+2n}+n}',r'\frac2{\sqrt{1+2/n}+1}',r'\frac22=1'),
14:('Вынос n из корня',r'\sqrt{n^2}=n\quad(n>0)',r'\sqrt{n^2+3n}=n\sqrt{1+3/n}',r'\frac{\sqrt{1+3/n}}{7+2/n}',r'\frac17'),
15:('Разности с разными ведущими коэффициентами',r'\sqrt{n^2}=n,\quad\sqrt[3]{n^3}=n',r'\frac{n\sqrt{1+1/n}-n\sqrt{9+2/n}}{n\sqrt[3]{1+1/n^3}-n\sqrt[3]{8+2/n^3}}',r'\frac{\sqrt{1+1/n}-\sqrt{9+2/n}}{\sqrt[3]{1+1/n^3}-\sqrt[3]{8+2/n^3}}',r'\frac{1-3}{1-2}=2'),
16:('Корни разных порядков',r'\sqrt[k]{n^p}=n^{p/k}',r'n^{1/2}-\sqrt2\,n;\qquad 2^{1/3}n^{2/3}-n',r'\frac{n^{-1/2}\sqrt{1+7/n}-\sqrt{2-3/n^2}}{n^{-1/3}\sqrt[3]{2-1/n^2}-\sqrt[4]{1+2/n^4}}',r'\frac{0-\sqrt2}{0-1}=\sqrt2'),
17:('Неравные порядки роста',r'\sqrt[3]{n^2}=n^{2/3}',r'\frac{n(3+7/n)}{n^{2/3}\sqrt[3]{3+1/n+1/n^2}}',r'n^{1/3}\cdot\frac{3+7/n}{\sqrt[3]{3+1/n+1/n^2}}',r'n^{1/3}\to+\infty\quad\Rightarrow\quad+\infty'),
18:('Вынос n из корня',r'\sqrt{n^2}=n\quad(n>0)',r'\frac{n\sqrt{4+7/n}}{n(3+1/n)}',r'\frac{\sqrt{4+7/n}}{3+1/n}',r'\frac23'),
19:('Старшие степени',r'\sqrt{9n^2+7}=n\sqrt{9+7/n^2}',r'\frac{n^2(2-3/n+1/n^2)}{n^2\sqrt{9+7/n^2}}',r'\frac{2-3/n+1/n^2}{\sqrt{9+7/n^2}}',r'\frac23'),
20:('Вынос n из корня',r'\sqrt{n^2}=n\quad(n>0)',r'\frac{n\sqrt{9+7/n}}{n(1+3/n)}',r'\frac{\sqrt{9+7/n}}{1+3/n}',r'3'),
21:('Ограниченный синус',r'|\sin(2n)|\le1\quad\Rightarrow\quad\frac{\sin(2n)}n\to0',r'\frac{3n+\sin(2n)}{n(4+\sqrt{1+5/n^2})}',r'\frac{3+\sin(2n)/n}{4+\sqrt{1+5/n^2}}',r'\frac3{4+1}=\frac35'),
23:('Разность двух корней',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\frac{3n}{\sqrt{n^2+4n}+\sqrt{n^2+n}}',r'\frac3{\sqrt{1+4/n}+\sqrt{1+1/n}}',r'\frac32'),
24:('Ограниченный синус и корень',r'\frac{\sin(2n)}{n^2}\to0,\quad\frac{n^{3/2}}{n^2}=n^{-1/2}\to0',r'\sqrt{n^3+1}=n^{3/2}\sqrt{1+1/n^3}',r'\frac{1-\sin(2n)/n^2}{2+n^{-1/2}\sqrt{1+1/n^3}}',r'\frac12'),
25:('Ограниченный синус',r'|\sin n|\le1\quad\Rightarrow\quad\frac{\sin n}n\to0',r'\frac{n+\sin n}{n}',r'1+\frac{\sin n}{n}',r'1+0=1'),
26:('Показательные функции и корни n-й степени',r'\sqrt[n]{a}\to1\quad(a>0)',r'3^{n+1}=3\cdot3^n',r'\frac{1+2^{1/n}/3^n}{3+4^{1/n}/3^n}',r'\frac13'),
27:('Ограниченный синус и старшая степень',r'\frac{\sin(5n)}{n^2}\to0,\quad\sqrt{n^4}=n^2',r'\sqrt{4n^4+5n}=n^2\sqrt{4+5/n^3}',r'\frac{2+\sin(5n)/n^2}{1+\sqrt{4+5/n^3}}',r'\frac2{1+2}=\frac23'),
28:('Произведение показательных функций',r'2^n3^n=6^n',r'(2^n+3)(3^n+2)=6^n+2\cdot2^n+3\cdot3^n+6',r'\frac{1+5/6^n}{1+2/3^n+3/2^n+6/6^n}',r'1'),
29:('Разность двух корней',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\frac{6n}{\sqrt{4n^2+3n}+\sqrt{4n^2-3n}}',r'\frac6{\sqrt{4+3/n}+\sqrt{4-3/n}}',r'\frac6{2+2}=\frac32'),
30:('Второй замечательный предел в последовательности',r'\left(1+\frac an\right)^n\to e^a',r'\frac{2n+5}{2n}=1+\frac5{2n}',r'\lim_{n\to\infty}n\cdot\frac5{2n}=\frac52',r'e^{5/2}'),
31:('Квадрат скобки и кубический корень',r'\sqrt[3]{8n^6}=2n^2',r'(\sqrt{n^2+1}+n)^2=n^2(\sqrt{1+1/n^2}+1)^2',r'\frac{(\sqrt{1+1/n^2}+1)^2}{\sqrt[3]{8+1/n^6}}',r'\frac42=2'),
32:('Сравнение степеней',r'\sqrt{n^3}=n^{3/2}',r'\frac{n^{3/2}\sqrt{1+1/n^3}+n}{n^{3/2}+1}',r'\frac{\sqrt{1+1/n^3}+n^{-1/2}}{1+n^{-3/2}}',r'1'),
33:('Квадрат скобки и корни',r'\sqrt[4]{n^4}=n,\quad\sqrt{n^4}=n^2',r'\frac{n^2(\sqrt[4]{1+10/n^4}+2)^2}{n^2\sqrt{3+1/n^4}}',r'\frac{(\sqrt[4]{1+10/n^4}+2)^2}{\sqrt{3+1/n^4}}',r'\frac9{\sqrt3}=3\sqrt3'),
34:('Отрицательные показатели',r'14^{-n+1}=14\left(\frac1{14}\right)^n\to0',r'14^{-n-1}=\frac1{14}\left(\frac1{14}\right)^n\to0',r'\frac{1-14^{-n+1}}{1-14^{-n-1}}\to\frac{1-0}{1-0}',r'1'),
36:('Разность кубов скобок',r'(a\pm b)^3=a^3\pm3a^2b+3ab^2\pm b^3',r'(n+2)^3-(n-2)^3=12n^2+16',r'\frac{12/n+16/n^3}{95+39/n^2}',r'0'),
37:('Разность рациональных дробей',r'\lim(a_n-b_n)=\lim a_n-\lim b_n\quad\text{при конечных пределах}',r'\frac{2n-1}{5n+7}=\frac{2-1/n}{5+7/n}',r'\frac{1+2n^3}{2+5n^3}=\frac{1/n^3+2}{2/n^3+5}',r'\frac25-\frac25=0'),
38:('Разность квадратных корней',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\sqrt{n+2}-\sqrt n=\frac2{\sqrt{n+2}+\sqrt n}',r'\sqrt{n+2}+\sqrt n\to+\infty',r'\frac2{+\infty}\to0'),
39:('Разные порядки роста',r'\sqrt{n^3}=n^{3/2},\quad\sqrt{n^2}=n',r'n^{3/2}\left(n^{3/2}\sqrt{1+1/n^3}-n\sqrt{1-2/n^2}\right)',r'n^3\left(\sqrt{1+1/n^3}-n^{-1/2}\sqrt{1-2/n^2}\right)',r'n^3(1+o(1))\to+\infty'),
40:('Наибольшее основание',r'\left(\frac23\right)^n\to0',r'\frac{2^n+3^n}{2^n-3^n}\cdot\frac{3^{-n}}{3^{-n}}',r'\frac{(2/3)^n+1}{(2/3)^n-1}',r'\frac{0+1}{0-1}=-1'),
}
S[22]=S[3];S[35]=S[6]
for i in range(1,41):
 topic,formula,first,second,last=S[i]
 src=[source('bank',4,f'Задача 3, пример {i}')]
 if i==5:src +=[source('demo',1,'№2, вариант с корнями'),source('solutions',2,'№2, вариант с корнями')]
 add(f'sequence-{i:02}',2,topic,r'\lim_{n\to\infty}\left('+latex(E[i])+r'\right)',answers[i],[
 stage('Нужные формулы',block('',formula),block('Работаем при положительных n. Сравнивай показатели степеней точно; ∞ − ∞ и 0/0 требуют преобразований.')),
 stage('Первое преобразование',block('',first)),stage('Ключевое сокращение или сравнение',block('',second)),stage('Переход к пределу',block('',last),block('Ответ исходной задачи.',r'\boxed{'+latex(s.sympify(answers[i].replace('infinity','oo')))+'}'))],src)
 checks.append((f'sequence-{i:02}',E[i],n,s.oo,answers[i]))

# Keep printed prompts intact: a CAS must not simplify away the problem itself.
printed={
1:r'\sqrt{n^2+n}-n',2:r'\frac{3n+2\sqrt[3]{27n^3+n}}{4n+\sqrt{n^2+5}}',3:r'\frac{(5^n-2)(2^n+5)}{10^n+1}',4:r'\frac{(\sqrt{n^2+1}+n)^2}{\sqrt[3]{n^6+1}}',
5:r'\frac{\sqrt{n^3-2n^2+1}+\sqrt[3]{n^4+1}}{\sqrt[4]{n^6+6n^5+2}-\sqrt[5]{n^7+3n^3+1}}',6:r'\frac{\sqrt[4]{n^5+2}-\sqrt[3]{n^2+1}}{\sqrt[5]{n^4+2}-\sqrt{n^3+1}}',
7:r'\frac{1+\frac12+\frac14+\cdots+\frac1{2^n}}{1+\frac13+\frac19+\cdots+\frac1{3^n}}',8:r'\frac1{n^2}(1+2+3+\cdots+n)',9:r'\frac{1+2+3+\cdots+n}{n+2}-\frac n2',10:r'\frac{10n^3-\sqrt{n^2+2}}{\sqrt{4n^6+3}-n}',
11:r'\frac{\sqrt{n+2}-\sqrt{n^2+2}}{\sqrt[4]{4n^4+1}-\sqrt[3]{n^4-1}}',12:r'\frac{4n^2-7}{2n^2-\sqrt{9n^2+5n^3+4}}',13:r'\sqrt{n^2+2n}-n',14:r'\frac{\sqrt{n^2+3n}}{7n+2}',
15:r'\frac{\sqrt{n^2+n}-\sqrt{9n^2+2n}}{\sqrt[3]{n^3+1}-\sqrt[3]{8n^3+2}}',16:r'\frac{\sqrt{n+7}-\sqrt{2n^2-3}}{\sqrt[3]{2n^2-1}-\sqrt[4]{n^4+2}}',17:r'\frac{3n+7}{\sqrt[3]{3n^2+n+1}}',18:r'\frac{\sqrt{4n^2+7n}}{3n+1}',19:r'\frac{2n^2-3n+1}{n\sqrt{9n^2+7}}',20:r'\frac{\sqrt{9n^2+7n}}{n+3}',
21:r'\frac{3n+\sin2n}{4n+\sqrt{n^2+5}}',22:r'\frac{(5^n-2)(2^n+5)}{10^n+1}',23:r'\sqrt{n^2+4n}-\sqrt{n^2+n}',24:r'\frac{n^2-\sin2n}{2n^2+\sqrt{n^3+1}}',25:r'\frac{n+\sin n}{n}',26:r'\frac{3^n+\sqrt[n]{2}}{3^{n+1}+\sqrt[n]{4}}',27:r'\frac{2n^2+\sin5n}{n^2+\sqrt{4n^4+5n}}',28:r'\frac{6^n+5}{(2^n+3)(3^n+2)}',29:r'\sqrt{4n^2+3n}-\sqrt{4n^2-3n}',30:r'\left(\frac{2n+5}{2n}\right)^n',
31:r'\frac{(\sqrt{n^2+1}+n)^2}{\sqrt[3]{8n^6+1}}',32:r'\frac{\sqrt{n^3+1}+n}{n^{1.5}+1}',33:r'\frac{(\sqrt[4]{n^4+10}+2n)^2}{\sqrt{3n^4+1}}',34:r'\frac{1-14^{-n+1}}{1-14^{-n-1}}',35:r'\frac{\sqrt[4]{n^5+2}-\sqrt[3]{n^2+1}}{\sqrt[5]{n^4+2}-\sqrt{n^3+1}}',36:r'\frac{(n+2)^3-(n-2)^3}{95n^3+39n}',37:r'\frac{2n-1}{5n+7}-\frac{1+2n^3}{2+5n^3}',38:r'\sqrt{n+2}-\sqrt n',39:r'n^{3/2}(\sqrt{n^3+1}-\sqrt{n^2-2})',40:r'\frac{2^n+3^n}{2^n-3^n}'
}
for task in tasks:
 if task['id'].startswith('sequence-'):
  task['prompt']=r'\lim_{n\to\infty}\left('+printed[int(task['id'].split('-')[1])]+r'\right)'

# Two distinct demo variants absent from the printed bank.
for id,expr,ans,topic,formula,first,second,last,variant in [
 ('demo-sequence-1',root(4*n*n+5*n)-root(4*n*n-3*n),'2','Разность двух корней',r'(\sqrt A-\sqrt B)(\sqrt A+\sqrt B)=A-B',r'\frac{8n}{\sqrt{4n^2+5n}+\sqrt{4n^2-3n}}',r'\frac8{\sqrt{4+5/n}+\sqrt{4-3/n}}',r'\frac8{2+2}=2','разность корней'),
 ('demo-sequence-3',(2**n+5)*(5**n+2)/(10**n+1),'1','Произведения показательных функций',r'2^n5^n=10^n',r'(2^n+5)(5^n+2)=10^n+2\cdot2^n+5\cdot5^n+10',r'\frac{1+2/5^n+5/2^n+10/10^n}{1+1/10^n}',r'1','показательные функции')]:
 add(id,2,topic,r'\lim_{n\to\infty}\left('+latex(expr)+r'\right)',ans,[stage('Формулы',block('',formula)),stage('Преобразование',block('',first)),stage('Сокращение',block('',second)),stage('Ответ',block('',last))],[source('demo',1,'№2, '+variant),source('solutions',1 if id.endswith('1') else 2,'№2, '+variant)])
 checks.append((id,expr,n,s.oo,ans))

x=s.symbols('x',real=True)
baseform=r'L=\lim(A-1)B;\quad A\to1,\ A>0\quad\Longrightarrow\quad A^B\to e^L'
equiv=r'\sin t\sim t,\ \tan t\sim t,\ 1-\cos t\sim t^2/2,\ \ln(1+t)\sim t,\ e^t-1\sim t\quad(t\to0)'
def power_task(id,A,B,point,L,first,product,calc,src=None,topic='Второй замечательный предел',origin='extra',note=''):
 add(id,3,topic,r'\lim_{x\to'+latex(point)+r'}\left('+latex(A)+r'\right)^{'+latex(B)+'}',s.sstr(s.exp(L)),[
 stage('Нужные формулы',block('Проверь, что основание стремится к 1. Все углы в радианах.',baseform),block('',equiv)),
 stage('Выделить единицу',block('Выпиши основание минус один. Сохрани все множители и знак.',first)),
 stage('Вычислить показатель у e',block('Умножаем всю добавку к единице на исходный показатель.',product),block('Упрощаем выражение до перехода к пределу.',calc)),
 stage('Ответ исходного предела',block('Полученное число становится показателем у e.',r'L='+latex(L)+r',\qquad\boxed{e^{'+latex(L)+'}}'))
 ],src,origin=origin,note=note)
 checks.append((id,(A-1)*B,x,point,s.sstr(L)))

power_task('demo-power-1',(2*x+4)/(2*x+5),3*x,s.oo,-R(3,2),r'A-1=-\frac1{2x+5}',r'L=\lim_{x\to\infty}\frac{-3x}{2x+5}',r'\frac{-3}{2+5/x}\to-\frac32',[source('demo',1,'№3, вариант 1'),source('solutions',2,'№3, вариант 1')],origin='source')
power_task('demo-power-2',(2*x+1)/(x+3),1/(x-2),s.Integer(2),R(1,5),r'A-1=\frac{x-2}{x+3}',r'L=\lim_{x\to2}\frac{x-2}{x+3}\frac1{x-2}',r'\frac1{x+3}\to\frac15',[source('demo',1,'№3, вариант 2'),source('solutions',3,'№3, вариант 2')],origin='source')
power_task('demo-power-3',(2*x-s.atan(x))/(2*x+s.acot(x)),3*x,s.oo,-3*s.pi/4,r'A-1=-\frac{\arctan x+\operatorname{arccot}x}{2x+\operatorname{arccot}x}',r'L=\lim_{x\to\infty}-\frac{3x(\pi/2)}{2x+\operatorname{arccot}x}',r'-\frac{3\pi/2}{2+\operatorname{arccot}x/x}\to-\frac{3\pi}{4}',[source('demo',1,'№3, вариант 3')],topic='Арктангенс и арккотангенс',origin='source',note='В демо в знаменателе arccot x. В официальном разборе стоит arctan x: это другой вариант, он сохранён отдельной задачей.')
power_task('solution-power-3',(2*x-s.atan(x))/(2*x+s.atan(x)),3*x,s.oo,-3*s.pi/2,r'A-1=-\frac{2\arctan x}{2x+\arctan x}',r'L=\lim_{x\to\infty}-\frac{6x\arctan x}{2x+\arctan x}',r'-\frac{6\arctan x}{2+\arctan x/x}\to-\frac{3\pi}{2}',[source('solutions',4,'№3, вариант 3')],topic='Арктангенс и арккотангенс',origin='source',note='Точная формула из разбора. Она отличается от третьего варианта демо.')

# Extra training covers the dependencies that were missed in the earlier tutoring.
extra=[
('extra-01',1-3*s.sin(x)**2,1/x**2,0,-3,r'A-1=-3\sin^2x',r'L=\lim\frac{-3\sin^2x}{x^2}',r'-3(\sin x/x)^2\to-3','Синус в основании'),
('extra-02',1-3*s.sin(x)**2,1/s.sin(x)**2,0,-3,r'A-1=-3\sin^2x',r'L=\lim\frac{-3\sin^2x}{\sin^2x}',r'-3','Синус в показателе'),
('extra-03',1-3*s.sin(2*x)**2,1/x**2,0,-12,r'A-1=-3\sin^2(2x)',r'L=-3\lim\frac{\sin^2(2x)}{x^2}',r'\sin(2x)\sim2x\Rightarrow L=-3\cdot4=-12','Сложный аргумент синуса'),
('extra-04',1-3*s.sin(2*x)**2,1/s.sin(x)**2,0,-12,r'A-1=-3\sin^2(2x)',r'L=-3\lim\frac{\sin^2(2x)}{\sin^2x}',r'\frac{\sin^2(2x)}{\sin^2x}\sim\frac{4x^2}{x^2}=4','Синус в основании и показателе'),
('extra-05',1+4*(1-s.cos(x)),1/x**2,0,2,r'A-1=4(1-\cos x)',r'L=4\lim\frac{1-\cos x}{x^2}',r'1-\cos x\sim x^2/2\Rightarrow L=2','Косинус и эквивалентности'),
('extra-06',6-5/s.cos(x)**2,1/x**2,0,-5,r'A-1=5\frac{\cos^2x-1}{\cos^2x}=-5\frac{\sin^2x}{\cos^2x}',r'L=-5\lim\frac{\sin^2x}{x^2\cos^2x}',r'(\sin x/x)^2\to1,\quad\cos^2x\to1','Дробь с косинусом'),
('extra-07',8-7/s.cos(2*x)**2,1/(1-s.cos(x)),0,-56,r'A-1=-7\frac{\sin^2(2x)}{\cos^2(2x)}',r'L=-7\lim\frac{\sin^2(2x)}{(1-\cos x)\cos^2(2x)}',r'\sin^2(2x)\sim4x^2,\quad1-\cos x\sim x^2/2\Rightarrow L=-56','Косинус в основании и показателе'),
('extra-08',5-4/s.cos(3*x)**2,(1+s.cos(x))/(1-s.cos(2*x)),0,-36,r'A-1=-4\frac{\sin^2(3x)}{\cos^2(3x)}',r'L=-4\lim\frac{\sin^2(3x)(1+\cos x)}{\cos^2(3x)(1-\cos2x)}',r'L=-4\cdot\frac{9\cdot2}{1\cdot2}=-36','Смешанная тригонометрия'),
('extra-09',3-2/s.cos(3*x)**2,(1+s.cos(x))/(1-s.cos(2*x)),0,-18,r'A-1=-2\frac{\sin^2(3x)}{\cos^2(3x)}',r'L=-2\lim\frac{\sin^2(3x)(1+\cos x)}{\cos^2(3x)(1-\cos2x)}',r'L=-2\cdot\frac{9\cdot2}{1\cdot2}=-18','Смешанная тригонометрия'),
('extra-10',1+2*s.tan(3*x)**2,1/(1-s.cos(2*x)),0,9,r'A-1=2\tan^2(3x)',r'L=2\lim\frac{\tan^2(3x)}{1-\cos2x}',r'\tan^2(3x)\sim9x^2,\quad1-\cos2x\sim2x^2\Rightarrow L=9','Тангенс и косинус'),
('extra-11',1+s.sin(3*x),1/s.tan(2*x),0,R(3,2),r'A-1=\sin3x',r'L=\lim\frac{\sin3x}{\tan2x}',r'\sin3x\sim3x,\ \tan2x\sim2x\Rightarrow L=3/2','Синус и тангенс'),
('extra-12',1+s.log(1+2*x),1/x,0,2,r'A-1=\ln(1+2x)',r'L=\lim\frac{\ln(1+2x)}x',r'\ln(1+2x)\sim2x\Rightarrow L=2','Логарифм в основании'),
('extra-13',1+3*(s.exp(x)-1),1/x,0,3,r'A-1=3(e^x-1)',r'L=3\lim\frac{e^x-1}{x}',r'e^x-1\sim x\Rightarrow L=3','Экспонента в основании'),
('extra-14',(3*x+1)/(x+3),1/(x-1),1,R(1,2),r'A-1=\frac{2(x-1)}{x+3}',r'L=\lim_{x\to1}\frac{2(x-1)}{(x+3)(x-1)}',r'\frac2{x+3}\to\frac12','Рациональное основание при x → a'),
('extra-15',(4*x-1)/(4*x+3),2*x,s.oo,-2,r'A-1=-\frac4{4x+3}',r'L=\lim_{x\to\infty}\frac{-8x}{4x+3}',r'-\frac8{4+3/x}\to-2','Рациональное основание на бесконечности'),
('extra-16',1+3*s.atan(x),1/x,0,3,r'A-1=3\arctan x',r'L=3\lim\frac{\arctan x}{x}',r'\arctan x\sim x\Rightarrow L=3','Арктангенс около нуля'),
('extra-17',1+2*s.asin(x),1/x,0,2,r'A-1=2\arcsin x',r'L=2\lim\frac{\arcsin x}{x}',r'\arcsin x\sim x\Rightarrow L=2','Арксинус около нуля'),
('extra-18',1+(root(1+x)-1),1/x,0,R(1,2),r'A-1=\sqrt{1+x}-1=\frac{x}{\sqrt{1+x}+1}',r'L=\lim\frac{\sqrt{1+x}-1}{x}',r'\frac1{\sqrt{1+x}+1}\to\frac12','Корень в основании'),
]
for id,A,B,p,L,first,prod,calc,topic in extra:power_task(id,A,B,s.sympify(p),s.sympify(L),first,prod,calc,topic=topic)

for id,expr,ans,prompt,first,second,last in [
 ('extra-log-00',x**x,'1',r'\lim_{x\to0+}x^x',r'\ln y=x\ln x',r'L=\lim_{t\to\infty}-\frac{\ln t}{t}\quad(t=1/x)',r'L=0\Rightarrow e^L=1'),
 ('extra-log-inf0',x**(1/x),'1',r'\lim_{x\to+\infty}x^{1/x}',r'\ln y=\frac{\ln x}{x}',r'\lim_{x\to\infty}\frac{\ln x}{x}=0',r'e^0=1')]:
 add(id,3,'Логарифмирование: 0⁰ и ∞⁰',prompt,ans,[stage('Универсальная формула',block('Основание положительно.',r'A^B=\exp(B\ln A)'),block('Стандартный предел: логарифм растёт медленнее положительной степени.',r'\frac{\ln t}{t}\to0\quad(t\to\infty)')),stage('Логарифмируем',block('',first)),stage('Вычисляем показатель',block('',second)),stage('Возвращаемся к исходному пределу',block('',last))],origin='extra')
 checks.append((id,expr,x,0 if id=='extra-log-00' else s.oo,ans))

# Keep the first hint specific: include every identity actually used below.
needed={
 'demo-power-1':r'\frac ab-1=\frac{a-b}b,\qquad 1/x\to0\ (x\to\infty)',
 'demo-power-2':r'\frac ab-1=\frac{a-b}b\quad(b\ne0)',
 'demo-power-3':r'\arctan x+\operatorname{arccot}x=\pi/2,\quad\arctan x\to\pi/2,\quad\operatorname{arccot}x\to0\ (x\to+\infty)',
 'solution-power-3':r'\arctan x\to\pi/2,\quad\arctan x/x\to0\ (x\to+\infty)',
 'extra-01':r'\sin t\sim t,\quad\sin^2t\sim t^2\ (t\to0)',
 'extra-02':r'\sin t\to0\ (t\to0);\quad\frac{c\sin^2t}{\sin^2t}=c\ (\sin t\ne0)',
 'extra-03':r'\sin(kt)\sim kt,\quad\sin^2(kt)\sim k^2t^2\ (t\to0)',
 'extra-04':r'\sin(kt)\sim kt,\quad\sin^2(kt)\sim k^2t^2\ (t\to0)',
 'extra-05':r'1-\cos t\sim t^2/2\ (t\to0)',
 'extra-06':r'\cos^2t-1=-\sin^2t,\quad\sin t\sim t,\quad\cos t\to1\ (t\to0)',
 'extra-10':r'\tan(kt)\sim kt,\quad1-\cos(kt)\sim k^2t^2/2\ (t\to0)',
 'extra-11':r'\sin(kt)\sim kt,\quad\tan(kt)\sim kt\ (t\to0)',
 'extra-12':r'\ln(1+t)\sim t\ (t\to0)',
 'extra-13':r'e^t-1\sim t\ (t\to0)',
 'extra-14':r'\frac ab-1=\frac{a-b}b\quad(b\ne0)',
 'extra-15':r'\frac ab-1=\frac{a-b}b,\qquad 1/x\to0\ (x\to\infty)',
 'extra-16':r'\arctan t\sim t\ (t\to0)',
 'extra-17':r'\arcsin t\sim t\ (t\to0)',
 'extra-18':r'\sqrt A-\sqrt B=\frac{A-B}{\sqrt A+\sqrt B}\quad(\sqrt A+\sqrt B\ne0)',
}
for id in ['extra-07','extra-08','extra-09']:
 needed[id]=r'\begin{gathered}\cos^2t-1=-\sin^2t,\quad\cos t\to1\\\sin^2(kt)\sim k^2t^2,\quad1-\cos(kt)\sim k^2t^2/2\ (t\to0)\end{gathered}'
for task in tasks:
 if task['id'] in needed:
  task['stages'][0]['blocks'][1]=block('Формулы для этой задачи.',needed[task['id']])

assert len(P)==30 and len(E)==40
ids=[t['id'] for t in tasks];assert len(ids)==len(set(ids))
coverage={'version':1,'total':len(tasks),'source':sum(t['origin']=='source' for t in tasks),'extra':sum(t['origin']=='extra' for t in tasks),'groups':{str(g):sum(t['group']==g for t in tasks) for g in [1,2,3]},'sourceFiles':[{'id':'bank','title':files[0].name},{'id':'demo','title':files[2].name},{'id':'solutions','title':files[1].name},{'id':'theory','title':files[3].name}],'notes':['Сохранены все 30 примеров чётности и 40 пределов последовательностей из банка, включая повторы.','Повторы демо прикреплены как дополнительные источники к тем же карточкам; отличающиеся формулы сохранены отдельно.','Практические задания №4–10 и теоретические вопросы пока доступны в исходных PDF, но не включены в интерактивный тренажёр.','Пример 39 последовательностей сохранён точно по печатной формуле: предел +∞.','Варианты arctan/arccot из демо и arctan/arctan из разбора сохранены отдельно.']}
(ROOT/'data/tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'data/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
# Separate independently computed limits. Persist only readable expressions, never Python code.
verification=[]
for id,expr,var,point,answer in checks:
 expected=s.sympify(answer.replace('infinity','oo'))
 try:
  result=s.limit(expr,var,point)
  ok=result==expected or s.simplify(result-expected)==0
  if not ok:raise AssertionError(f'{id}: expected {expected}, got {result}')
  verification.append({'id':id,'method':'symbolic limit','result':str(result),'passed':True})
 except NotImplementedError:
  # Oscillatory terms are bounded explicitly in their hand-written solutions.
  vals=[float(expr.subs(var,v).evalf()) for v in [10000,1000000]]
  if not all(abs(v-float(expected))<0.02 for v in vals):raise AssertionError((id,vals,expected))
  verification.append({'id':id,'method':'bounded trigonometric term + numerical cross-check','values':vals,'passed':True})
(ROOT/'data/verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(coverage,ensure_ascii=False,indent=2))
