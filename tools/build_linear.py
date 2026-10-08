"""Independent linear-algebra bank. Does not read or write the calculus bank."""
import json,re,shutil,math
from pathlib import Path
import sympy as s
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
INPUT=Path(r'C:/Users/alaron/Downloads/AyuGram Desktop')
FILES={'linear-ticket':'Образец_билета_Линейная_алгебра_1_семестр_2025_26.pdf','linear-essentials':'Это надо знать к экзамену 2026.pdf','linear-questions':'Вопросы на сессию.pdf'}
for slug,name in FILES.items():shutil.copyfile(INPUT/name,ROOT/'sources'/f'{slug}.pdf')
pages={slug:[p.extract_text() for p in PdfReader(INPUT/name).pages] for slug,name in FILES.items()}
example_pages={int(m[1]):i+1 for i,p in enumerate(pages['linear-essentials']) for m in re.finditer(r'Пример\s*3\.(\d+)\.',p)}
tasks=[];verification=[];issues=[];demo_map={}
x,y,z,t=s.symbols('x y z t',real=True)
def tx(v):return s.latex(v,mat_delim='(',mat_str='matrix')
def ans(v):return s.sstr(s.simplify(v)).replace('**','^').replace('I','i').replace('E','e')
def vec(v):return '('+';'.join(ans(a) for a in v)+')'
def mat(v):return '; '.join(' '.join(ans(v[i,j]) for j in range(v.cols)) for i in range(v.rows))
def block(note='',tex='',graph=None):return {**{'note':note,'tex':tex},**({'graph':graph} if graph else {})}
def stage(title,note='',tex='',graph=None):return {'title':title,'blocks':[block(note,tex,graph)]}
def steps(formula,first,key,last,notes=None,graph=None):
 notes=notes or ['Используем определение и основные формулы.','Подставляем исходные данные.','Выполняем вычисления, сохраняя знаки.','Проверяем результат по исходному условию.']
 return [stage('Нужные формулы',notes[0],formula),stage('Первое преобразование',notes[1],first),stage('Ключевой шаг',notes[2],key),stage('Ответ и проверка',notes[3],last,graph)]
def field(id,label,value,kind='number',**kw):return dict(id=id,label=label,answer=value if isinstance(value,str) else ans(value),kind=kind,**kw)
def source(file,page,label):return dict(file=file,page=page,label=label)
def add(n,group,topic,prompt,value,stages,kind='number',file='linear-essentials',page=None,label=None,**kw):
 id=f'la-example-{n:02}' if isinstance(n,int) else n
 label=label or (f'Пособие · пример 3.{n}' if isinstance(n,int) else id)
 page=page or example_pages[n]
 task=dict(id=id,group=group,topic=topic,prompt=prompt,answer=value if isinstance(value,str) else ans(value),stages=stages,kind=kind,origin='source',meta=label,sources=[source(file,page,label)],note='',instruction='Введи только итоговый ответ. Решение откроется по шагам.')
 task.update(kw)
 tasks.append(task);return task
def fields(n,group,topic,prompt,values,stages,**kw):
 return add(n,group,topic,prompt,json.dumps({f['id']:f['answer'] for f in values},ensure_ascii=False),stages,kind='fields',fields=values,**kw)
def verify(id,method,passed):
 assert passed,(id,method);verification.append(dict(id=str(id),method=method,passed=True))
def issue(task,reason):task['note']='Особенность исходной записи: пояснение есть в разборе.';issues.append(dict(id=task['id'],reason=reason));task['stages'][-1]['blocks'].append(block(reason))
def demo(task,group,variant,page):
 key=f'{group}.{variant}';assert key not in demo_map;demo_map[key]=task['id'];task['sources'].append(source('linear-ticket',page,f'Образец · №{group} · вариант {variant}'));return task
def dm(n,group,variant,page):return demo(next(v for v in tasks if v['id']==f'la-example-{n:02}'),group,variant,page)
def points_prompt(**points):return r',\quad '.join(k+tx(s.Tuple(*v)) for k,v in points.items())
def graph_points(points,labels=None):
 return dict(type='points',points=[[float(s.re(v)),float(s.im(v))] if not isinstance(v,(list,tuple,s.MatrixBase)) else [float(v[0]),float(v[1])] for v in points],labels=labels or [f'z{i+1}' for i in range(len(points))],axes=['Re z','Im z'])
def curve_graph(kind,h,k,a,b=0,vertical=False):return dict(type=kind,h=float(h),k=float(k),a=float(a),b=float(b),vertical=vertical,axes=['x','y'])

# 1. Matrices: every result is checked by substitution into the original equation.
def matrix_equation(n,A,B,C=None,right=False,**kw):
 A=s.Matrix(A);B=s.Matrix(B);C=s.Matrix(C) if C is not None else None;D=C-B if C is not None else B
 inv=A.inv();X=D*inv if right else inv*D;eq=('XA' if right else 'AX')+('+B=C' if C is not None else '=B')
 prompt=r'\begin{gathered}'+eq+r'\\A='+tx(A)+r',\quad B='+tx(B)+(r',\quad C='+tx(C) if C is not None else '')+r'\end{gathered}'
 formula=r'A^{-1}=\frac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix},\quad '+('X=(C-B)A^{-1}' if right and C is not None else 'X=A^{-1}(C-B)' if C is not None else 'X=BA^{-1}' if right else 'X=A^{-1}B')
 key=('C-B=' if C is not None else 'B=')+tx(D)+r',\quad X='+('('+tx(D)+')'+tx(inv) if right else tx(inv)+'('+tx(D)+')')
 task=fields(n,1,'Матричное уравнение '+eq,prompt,[field('inverse','Обратная матрица A⁻¹',mat(inv),'matrix'),field('result','Матрица X',mat(X),'matrix')],steps(formula,r'\det A='+tx(A.det())+r',\quad A^{-1}='+tx(inv),key,r'X='+tx(X),['Порядок множителей важен: для AX умножаем слева, для XA справа.','Определитель не равен нулю, обратная матрица существует.','Из каждого элемента C вычитаем соответствующий элемент B, затем умножаем матрицы.','Подстановка даёт исходную правую часть. Ввод матриц: элементы через пробел, строки через ;.']),**kw)
 verify(task['id'],'A*Ainv=I; substitution into matrix equation',A*inv==s.eye(A.rows) and (X*A if right else A*X)==D);return task
def matrix_product(n,A,B,mode,**kw):
 A=s.Matrix(A);B=s.Matrix(B);L,R={'ATBT':(A.T,B.T),'BTAT':(B.T,A.T),'ATB':(A.T,B)}[mode];C=L*R;expr={'ATBT':'A^TB^T','BTAT':'B^TA^T','ATB':'A^TB'}[mode]
 task=add(n,1,'Транспонирование и умножение',r'\begin{gathered}A='+tx(A)+r',\quad B='+tx(B)+r'\\C='+expr+r'\end{gathered}',mat(C),steps(r'(AB)^T=B^TA^T,\quad c_{ij}=\sum_k l_{ik}r_{kj}',r'L='+tx(L)+r',\quad R='+tx(R),r'c_{11}='+tx(sum(L[0,k]*R[k,0] for k in range(L.cols))),r'C='+tx(C)),kind='matrix',**kw)
 verify(task['id'],'all entries recomputed as row-column dot products',all(C[i,j]==sum(L[i,k]*R[k,j] for k in range(L.cols)) for i in range(C.rows) for j in range(C.cols)));return task
matrix_equation(1,[[1,-2],[1,-3]],[[1,4,-1],[1,6,0]])
matrix_equation(2,[[2,1],[4,3]],[[2,-4],[4,1],[2,-6]],right=True)
matrix_product(3,[[2,3],[-4,2],[2,2]],[[-2,-2,-2],[-1,-3,3]],'ATBT')
matrix_product(4,[[2,3],[-4,2],[2,2]],[[-2,-2,-2],[-1,-3,3]],'BTAT')
matrix_product(5,[[1,-2,-4],[-3,3,2]],[[-2,-3,2],[-1,0,1]],'ATB')
matrix_product(6,[[2,3,2],[-1,4,-5]],[[1,-1],[-2,3],[3,2]],'BTAT')
for n,right,B,C in [(7,False,[[-1,4],[3,1]],[[7,2],[6,-6]]),(8,True,[[-1,4],[3,1]],[[7,2],[6,-6]]),(9,True,[[-1,4],[3,1],[0,-2]],[[0,2],[6,-6],[5,1]])]:matrix_equation(n,[[2,-1],[-4,3]],B,C,right)

# 2. Vector geometry.
def vector_problem(n,mode,A,B,C,D=None,**kw):
 A,B,C=map(s.Matrix,[A,B,C]);u=B-A;v=C-A;cross=u.cross(v)
 if mode in ['cos','angle']:
  result=s.simplify(u.dot(v)/(u.norm()*v.norm()));target=s.acos(result) if mode=='angle' else result
  formula=r'\cos\varphi=\frac{u\cdot v}{|u||v|}';key=r'u\cdot v='+tx(u.dot(v))+r',\quad |u||v|='+tx(s.simplify(u.norm()*v.norm()));last=(r'\varphi=' if mode=='angle' else r'\cos\varphi=')+tx(target)
  title='Угол треугольника' if mode=='angle' else 'Косинус угла треугольника'
 elif mode=='area':
  target=s.simplify(cross.norm()/2);formula=r'S=\frac12|u\times v|';key=r'u\times v='+tx(cross)+r',\quad |u\times v|='+tx(cross.norm());last='S='+tx(target);title='Площадь треугольника'
 else:
  w=s.Matrix(D)-A;det=s.Matrix.hstack(u,v,w).det();target=abs(det)/6 if mode=='volume' else ('1' if det==0 else '2');formula=r'\Delta=(u\times v)\cdot w,\quad V=\frac{|\Delta|}{6},\quad \Delta=0\iff\text{компланарны}';key=r'w='+tx(w)+r',\quad\Delta='+tx(det);last='V='+tx(target) if mode=='volume' else r'\Delta='+tx(det)+r'\ne0\Rightarrow\text{не компланарны}';title='Объём тетраэдра' if mode=='volume' else 'Компланарность векторов'
 prompt=points_prompt(A=A,B=B,C=C,**({'D':D} if D else {}));task=add(n,2,title,prompt,target,steps(formula,'u='+tx(u)+r',\quad v='+tx(v),key,last),**kw)
 if mode=='coplanar':task.update(kind='choice',options=[dict(value='1',label='Компланарны'),dict(value='2',label='Не компланарны')],instruction='Проверь компланарность векторов AB, AC, AD.')
 elif mode=='angle':task['instruction']='Найди угол при первой указанной вершине. Ответ в радианах: pi/2 (90°).'
 elif mode=='cos':task['instruction']='Найди косинус угла при первой указанной вершине.'
 elif mode=='area':task['instruction']='Найди площадь треугольника ABC.'
 else:task['instruction']='Найди объём тетраэдра ABCD.'
 verify(task['id'],'vector identity: cross norm squared = Gram determinant',s.simplify(cross.dot(cross)-(u.dot(u)*v.dot(v)-u.dot(v)**2))==0);return task
vector_problem(10,'angle',[-1,0,2],[0,2,1],[-3,2,4]) # First point is C in the original condition.
tasks[-1]['prompt']=points_prompt(A=[0,2,1],B=[-3,2,4],C=[-1,0,2]);tasks[-1]['instruction']='Найди внутренний угол C треугольника ABC. Вводи радианы: pi/2 = 90°.'
vector_problem(11,'cos',[1,1,1],[1,2,3],[-1,2,1])
vector_problem(12,'area',[1,2,3],[3,4,5],[2,4,7])
vector_problem(13,'coplanar',[5,1,-4],[1,2,-1],[3,3,-4],[2,2,2])
vector_problem(14,'volume',[5,1,-4],[1,2,-1],[3,3,-4],[2,2,2])

# 3. Lines, planes and orthogonal projections.
def plane(n,P,N,prompt,**kw):
 P,N=map(s.Matrix,[P,N]);expr=s.expand(N.dot(s.Matrix([x,y,z])-P));equation=ans(expr)+'=0'
 task=add(n,3,'Уравнение плоскости',prompt,equation,steps(r'A(x-x_0)+B(y-y_0)+C(z-z_0)=0',r'n='+tx(N)+r',\quad M_0='+tx(P),tx(expr)+'=0',tx(expr)+'=0'),kind='equation',variables=['x','y','z'],**kw)
 task['instruction']='Составь уравнение плоскости. Допускается любая равносильная запись.';verify(task['id'],'given point lies in plane and gradient is the normal',expr.subs(dict(zip([x,y,z],P)))==0 and s.Matrix([s.diff(expr,v) for v in [x,y,z]])==N);return task
def line(n,P,d,prompt,**kw):
 P,d=map(s.Matrix,[P,d]);value=';'.join(axis+'='+ans(P[i]+t*d[i]) for i,axis in enumerate(['x','y','z']))
 task=add(n,3,'Уравнение прямой в пространстве',prompt,value,steps(r'r=r_0+t\,s,\quad \frac{x-x_0}{s_x}=\frac{y-y_0}{s_y}=\frac{z-z_0}{s_z}',r'r_0='+tx(P)+r',\quad s='+tx(d),r'r='+tx(P)+'+t'+tx(d),r'\begin{cases}'+r'\\'.join(axis+'='+tx(P[i]+t*d[i]) for i,axis in enumerate(['x','y','z']))+r'\end{cases}'),kind='line3',**kw)
 task['instruction']='Введи канонические или параметрические уравнения. Например x=1+2t; y=3-t; z=4t.';verify(task['id'],'parametric direction is nonzero',d!=s.zeros(3,1));return task
plane(15,[-3,1,1],[2,-1,4],r'M_0(-3;1;1),\quad \frac{x-1}{2}=\frac{y+2}{-1}=\frac{z-3}{4}')
tasks[-1]['description']='Плоскость проходит через M₀ и перпендикулярна данной прямой.'
line(16,[-7,-3,2],[1,-4,-5],r'A(-7;-3;2),\quad x-4y-5z+8=0');tasks[-1]['description']='Прямая проходит через A перпендикулярно плоскости.'
line(17,[-1,2,3],[6,-4,-2],points_prompt(A=[-1,2,3],B=[5,-2,1]));tasks[-1]['description']='Составь уравнения прямой AB.'
plane(18,[1,1,1],s.Matrix([-5,1,-2]).cross(s.Matrix([-3,1,2])),points_prompt(A=[1,1,1],B=[-4,2,-1],C=[-2,2,3]));tasks[-1]['description']='Плоскость проходит через три заданные точки.'
def projection_line(n,P,Q,d,prompt,reflect=False,**kw):
 P,Q,d=map(s.Matrix,[P,Q,d]);tau=s.simplify((P-Q).dot(d)/d.dot(d));H=Q+tau*d;R=2*H-P;result=R if reflect else H
 task=add(n,3,'Симметрия относительно прямой' if reflect else 'Проекция точки на прямую',prompt,vec(result),steps(r't_0=\frac{(P-Q)\cdot s}{s\cdot s},\quad H=Q+t_0s,\quad P^*=2H-P',r'Q='+tx(Q)+r',\quad s='+tx(d),r't_0='+tx(tau)+r',\quad H='+tx(H),(r'P^*=' if reflect else 'H=')+tx(result)),kind='vector',**kw)
 task['instruction']='Найди симметричную точку. Ввод: (x;y;z).' if reflect else 'Найди ортогональную проекцию. Ввод: (x;y;z).'
 verify(task['id'],'projection lies on line; residual is perpendicular',s.simplify((P-H).dot(d))==0);return task
projection_line(19,[1,0,-1],[-1,3,0],[1,2,3],r'P(1;0;-1),\quad \frac{x+1}{1}=\frac{y-3}{2}=\frac z3',True)
def intersection(n,P,d,Q,e,prompt,**kw):
 P,d,Q,e=map(s.Matrix,[P,d,Q,e]);u=s.Symbol('u');solution=s.solve(list(P+t*d-Q-u*e),[t,u]);result=P+solution[t]*d if t in solution else None
 val=vec(result) if result is not None else 'none'
 task=add(n,3,'Пересечение прямых',prompt,val,steps(r'P+t\,s_1=Q+u\,s_2',r'P+t\,s_1='+tx(P+t*d)+r',\quad Q+u\,s_2='+tx(Q+u*e),r't='+tx(solution.get(t,s.Symbol('t')))+r',\quad u='+tx(solution.get(u,s.Symbol('u'))) if result is not None else r'\text{Система для }t,u\text{ несовместна}',tx(result) if result is not None else r'\text{Прямые не пересекаются}'),kind='points',**kw)
 task['instruction']='Найди точку пересечения: (x;y;z). Если пересечения нет, введи «нет».'
 verify(task['id'],'all three coordinate equations solved together',result is None or s.simplify(result-Q-solution[u]*e)==s.zeros(3,1));return task
intersection(20,[1,-2,3],[1,2,4],[-2,-1,-2],[3,-2,4],r'\frac{x-1}{1}=\frac{y+2}{2}=\frac{z-3}{4},\quad\frac{x+2}{3}=\frac{y+1}{-2}=\frac{z+2}{4}')
P=s.Matrix([3,1,-1]);N=s.Matrix([1,2,3]);q=s.Rational(N.dot(P)-30,N.dot(N));H=P-q*N;R=2*H-P
fields(21,3,'Проекция и симметрия относительно плоскости',r'M(3;1;-1),\quad x+2y+3z-30=0',[field('projection','Проекция H',vec(H),'vector'),field('reflection','Симметричная точка M*',vec(R),'vector')],steps(r'H=M-\frac{n\cdot M+D}{n\cdot n}n,\quad M^*=2H-M',r'n='+tx(N)+r',\quad n\cdot M-30=-28',r'H='+tx(H),r'H='+tx(H)+r',\quad M^*='+tx(R)))
verify(21,'plane projection and reflection',N.dot(H)==30 and (P-H).cross(N)==s.zeros(3,1) and R+P==2*H)
projection_line(22,[0,3,-4],[0,4,4],[-1,3,7],r'P(0;3;-4),\quad \begin{cases}x-2y+z+4=0\\2x+3y-z-8=0\end{cases}')
verify(22,'direction is cross product of plane normals',s.Matrix([1,-2,1]).cross(s.Matrix([2,3,-1]))==s.Matrix([-1,3,7]))

# 4. Conics and quadrics. Equations are accepted up to a nonzero factor.
def conic(n,kind,h,k,a2,b2,prompt,vertical=False,extra=None,identify=False,**kw):
 U=(y-k) if vertical else (x-h);V=(x-h) if vertical else (y-k)
 if kind=='parabola':
  coeff=s.sympify(a2);eq=ans(V**2)+'='+ans(coeff*U);eps=None;formula=r'v^2=4fu,\quad F=(f,0),\quad d:u=-f';key=r'4f='+tx(coeff);g=curve_graph(kind,h,k,coeff,vertical=vertical)
 else:
  c2=a2-b2 if kind=='ellipse' else a2+b2;eps=s.simplify(s.sqrt(c2/a2));eq=ans(U**2/a2+V**2/b2 if kind=='ellipse' else U**2/a2-V**2/b2)+'=1'
  formula=r'\frac{u^2}{a^2}+\frac{v^2}{b^2}=1,\ c^2=a^2-b^2,\ \varepsilon=c/a' if kind=='ellipse' else r'\frac{u^2}{a^2}-\frac{v^2}{b^2}=1,\ c^2=a^2+b^2,\ \varepsilon=c/a'
  key=r'a^2='+tx(a2)+r',\quad b^2='+tx(b2)+r',\quad c^2='+tx(c2);g=curve_graph(kind,h,k,s.sqrt(a2),s.sqrt(b2),vertical)
 vals=[field('equation','Каноническое уравнение',eq,'equation',variables=['x','y'])]
 if identify:vals.insert(0,field('type','Тип: 1 эллипс, 2 гипербола, 3 парабола',str({'ellipse':1,'hyperbola':2,'parabola':3}[kind]),'choice',options=[dict(value=str(i)) for i in [1,2,3]]))
 if eps is not None:vals.append(field('eccentricity','Эксцентриситет ε',eps))
 vals.append(field('center','Вершина' if kind=='parabola' else 'Центр',vec([h,k]),'vector'))
 vals.extend(extra or [])
 task=fields(n,4,'Канонический вид кривой' if identify else {'ellipse':'Эллипс','hyperbola':'Гипербола','parabola':'Парабола'}[kind],prompt,vals,steps(formula,r'u='+tx(U)+r',\quad v='+tx(V),key,r'\begin{gathered}'+s.latex(s.Eq(s.sympify(eq.split('=')[0].replace('^','**')),s.sympify(eq.split('=')[1].replace('^','**'))))+ (r'\\\varepsilon='+tx(eps) if eps is not None else '')+r'\end{gathered}',graph=g),**kw)
 task['instruction']='Введи уравнение и характеристики. Равносильные уравнения принимаются. Чертёж откроется в конце разбора.'
 verify(task['id'],'conic parameters satisfy focal identity',kind=='parabola' or s.simplify((eps**2)*a2-(a2-b2 if kind=='ellipse' else a2+b2))==0);return task
conic(23,'hyperbola',2,-2,s.Integer(5),s.Integer(4),r'F_1(2;1),\quad F_2(2;-5),\quad b=2',True)
conic(24,'ellipse',-2,-3,s.Integer(100),s.Integer(36),r'F_1(-10;-3),\quad F_2(6;-3),\quad a=10')
conic(25,'parabola',-1,2,-24,0,r'F(-7;2),\quad d:x-5=0')
conic(26,'hyperbola',0,0,s.Integer(5),s.Integer(4),r'F_1(0;3),\quad F_2(0;-3),\quad b=2',True,extra=[field('directrices','Директрисы', 'y=-5/3; y=5/3','lines')])
conic(27,'ellipse',0,0,s.Integer(100),s.Integer(36),r'F_1(-8;0),\quad F_2(8;0),\quad a=10')
conic(28,'parabola',0,0,-28,0,r'F(-7;0),\quad d:x-7=0')
conic(29,'ellipse',0,0,s.Integer(9),s.Integer(4),r'9x^2+4y^2-36=0',True,extra=[field('distance','Расстояние между фокусами',2*s.sqrt(5))],identify=True)
conic(30,'hyperbola',-1,2,s.Integer(16),s.Integer(9),r'9x^2-16y^2+18x+64y-199=0',identify=True)
roots=s.solve(4*(3*t)**2-5*(2-2*t)**2-20*(-1+2*t),t);intersections=[s.Matrix([3*r,2-2*r,-1+2*r]) for r in roots]
add(31,4,'Пересечение прямой и поверхности',r'4x^2-5y^2-20z=0,\quad \frac x3=\frac{y-2}{-2}=\frac{z+1}{2}','|'.join(vec(v) for v in intersections),steps(r'x=3t,\quad y=2-2t,\quad z=-1+2t',r'36t^2-5(2-2t)^2-20(-1+2t)=0',r'16t^2=0\Rightarrow t=0',r'M=(0;2;-1)'),kind='points')
verify(31,'substitution into quadric and repeated root',roots==[0] and all(s.simplify(4*v[0]**2-5*v[1]**2-20*v[2])==0 for v in intersections))
fields(32,4,'Сечение поверхности плоскостью',r'4x^2-5y^2-120z=0,\quad y=-6',[field('surface','Поверхность: 1 эллипсоид, 2 гиперболический параболоид, 3 конус','2','choice',options=[dict(value=str(i)) for i in [1,2,3]]),field('curve','Кривая: 1 эллипс, 2 гипербола, 3 парабола','3','choice',options=[dict(value=str(i)) for i in [1,2,3]]),field('equation','Уравнение сечения в координатах x,z','x^2=30(z+3/2)','equation',variables=['x','z']),field('focus','Фокус в пространстве (x;y;z)','(0;-6;6)','vector')],steps(r'v^2=4fu,\quad F=(0,f)',r'y=-6\Rightarrow 4x^2-180-120z=0',r'x^2=30(z+3/2),\quad f=30/4',r'F=(0;-6;6)',notes=['По знакам квадратов определяем тип поверхности, затем исследуем сечение.','В сечении фиксируем y=-6.','Получено уравнение параболы с вершиной (0;-3/2) в координатах (x,z).','Поверхность - гиперболический параболоид; сечение - парабола. Фокус в пространстве F=(0;-6;6).']),description='Определи тип поверхности и кривой сечения, найди её каноническое уравнение и фокус в пространстве.')
issue(tasks[-1],'В пособии фокус F(0;6) записан в координатах сечения (x,z). В пространстве у него три координаты: (0;-6;6).')
verify(32,'focus of translated parabola',s.Rational(-3,2)+s.Rational(30,4)==6)

# 5. Complex numbers. i is never confused with a real variable.
def complex_value(n,expr,prompt=None,**kw):
 value=s.expand_complex(expr);task=add(n,5,'Действия с комплексными числами',prompt or tx(expr),ans(value),steps(r'i^2=-1,\quad i^3=-i,\quad z\overline z=|z|^2',tx(expr),r'\Re z='+tx(s.re(value))+r',\quad\Im z='+tx(s.im(value)),'z='+tx(value)),kind='complex',**kw)
 verify(task['id'],'exact complex arithmetic',s.simplify(expr-value)==0);return task
complex_value(33,(2-4*s.I**3)/(1-s.I)*s.conjugate(-1-3*s.I),r'\frac{2-4i^3}{1-i}\cdot\overline{(-1-3i)}')
v=s.expand_complex((3-4*s.I)/(2+s.I))
fields(34,5,'Действительная и мнимая части',r'z=\frac{3-4i}{2+i}',[field('real','Re z',s.re(v)),field('imaginary','Im z',s.im(v))],steps(r'\frac{a+bi}{c+di}=\frac{(a+bi)(c-di)}{c^2+d^2}',r'z=\frac{(3-4i)(2-i)}5',r'z=\frac{2-11i}{5}',r'\Re z=2/5,\quad\Im z=-11/5'))
def polar(n,values,**kw):
 vals=[];lines=[]
 for i,v in enumerate(values):
  r=s.simplify(s.Abs(v));phi=s.arg(v);vals +=[field(f'r{i}','Модуль '+(f'z{i+1}' if len(values)>1 else 'r'),r),field(f'phi{i}','Главный аргумент '+(f'z{i+1}' if len(values)>1 else 'φ'),phi)]
  lines.append(r'z_'+str(i+1)+'='+tx(r)+r'\left(\cos('+tx(phi)+r')+i\sin('+tx(phi)+r')\right)='+tx(r)+'e^{i('+tx(phi)+')}' )
  verify(str(n)+f'.{i}','polar representation reconstructs number',s.simplify(r*(s.cos(phi)+s.I*s.sin(phi))-v)==0)
 return fields(n,5,'Тригонометрическая и показательная формы',r',\quad '.join('z_'+str(i+1)+'='+tx(v) for i,v in enumerate(values)),vals,steps(r'z=r(\cos\varphi+i\sin\varphi)=re^{i\varphi},\quad r=\sqrt{a^2+b^2}',r'\varphi=\operatorname{Arg}z\in(-\pi;\pi]',r'\text{Сначала определяем четверть, затем аргумент.}',r'\begin{gathered}'+r'\\'.join(lines)+r'\end{gathered}',graph=graph_points(values)),description='Вместо переписывания формы введи её параметры: модуль и главное значение аргумента в радианах.')
polar(35,[-2+2*s.I]);polar(36,[3,-3,3*s.I,-3*s.I,3-s.I*s.sqrt(3)])
def complex_roots(n,poly,roots,prompt=None,formula=None,key=None,**kw):
 roots=[s.expand_complex(v) for v in roots];value='; '.join(ans(v) for v in roots)
 task=add(n,5,'Корни комплексного уравнения',prompt or tx(poly)+'=0',value,steps(formula or r'z^n=r e^{i\varphi}\Rightarrow z_k=\sqrt[n]{r}\,e^{i(\varphi+2\pi k)/n}',tx(poly)+'=0',key or r'\text{Перебираем все различные значения }k=0,\ldots,n-1',r'\begin{gathered}'+r'\\'.join('z_'+str(i+1)+'='+tx(v) for i,v in enumerate(roots))+r'\end{gathered}',graph=graph_points(roots)),kind='complex-set',**kw)
 task['instruction']='Введи все корни через ; в любом порядке, например -2+3i; -2-3i. Чертёж и формы записи появятся в разборе.'
 polar_forms=[r'z_'+str(i+1)+'='+tx(s.simplify(s.Abs(v)))+r'[\cos('+tx(s.arg(v))+r')+i\sin('+tx(s.arg(v))+r')]' for i,v in enumerate(roots)]
 task['stages'][-1]['blocks'].insert(0,block('Тригонометрические формы тех же корней.',r'\begin{gathered}'+r'\\'.join(polar_forms)+r'\end{gathered}'))
 for root in roots:verify(task['id'],'each root substituted into polynomial',s.simplify(s.expand(poly.subs(z,root)))==0)
 verify(task['id'],'number of distinct roots equals degree',len(set(roots))==s.degree(poly,z));return task
complex_roots(37,z**2+4*z+13,[-2+3*s.I,-2-3*s.I],formula=r'z=-p/2\pm\sqrt{p^2/4-q}',key=r'z=-2\pm\sqrt{-9}=-2\pm3i')
complex_roots(38,z**4-6*z**2+36,[a*3/s.sqrt(2)+b*s.I*s.sqrt(s.Rational(3,2)) for a,b in [(1,1),(-1,1),(-1,-1),(1,-1)]],formula=r'w=z^2,\quad w^2-6w+36=0',key=r'w=3\pm3\sqrt3i,\quad |w|=6')
def complex_power(n,base,degree,prompt,**kw):
 value=s.expand_complex(base**degree);radius=s.simplify(s.Abs(base)**degree);phi=s.arg(value)
 task=fields(n,5,'Степень комплексного числа',prompt,[field('value','Алгебраическая форма',ans(value),'complex'),field('modulus','Модуль результата',radius),field('argument','Главный аргумент результата',phi)],steps(r'[r(\cos\varphi+i\sin\varphi)]^n=r^n(\cos n\varphi+i\sin n\varphi)',r'r='+tx(s.Abs(base))+r',\quad\varphi='+tx(s.arg(base)),r'r^n='+tx(radius)+r',\quad n\varphi='+tx(degree*s.arg(base))+r'\equiv'+tx(phi)+r'\pmod{2\pi}',r'z='+tx(radius)+r'[\cos('+tx(phi)+r')+i\sin('+tx(phi)+r')]='+tx(value),graph=graph_points([value])),**kw)
 verify(task['id'],'De Moivre and exact integer power agree',s.simplify(radius*(s.cos(phi)+s.I*s.sin(phi))-value)==0);return task
complex_power(39,s.sqrt(3)-3*s.I,16,r'(\sqrt3-3i)^{16}')
issue(tasks[-1],'В рамке итогового ответа примера 3.39 пропущена мнимая единица i перед √3/2. В предыдущей строке решения она есть. Правильно 12^8·(-1/2+i√3/2).')
complex_value(40,(s.sqrt(3)-s.I)**5,r'(\sqrt3-i)^5')
complex_roots(41,z**4+1,[s.cos(s.pi/4+s.pi*k/2)+s.I*s.sin(s.pi/4+s.pi*k/2) for k in range(4)],key=r'z_k=\cos(\pi/4+\pi k/2)+i\sin(\pi/4+\pi k/2),\quad k=0,1,2,3')
complex_roots(42,z**3+27,[-3,s.Rational(3,2)+3*s.sqrt(3)*s.I/2,s.Rational(3,2)-3*s.sqrt(3)*s.I/2],key=r'z_k=3[\cos(\pi/3+2\pi k/3)+i\sin(\pi/3+2\pi k/3)]')
complex_roots(43,z**3-64*s.I,[2*s.sqrt(3)+2*s.I,-2*s.sqrt(3)+2*s.I,-4*s.I],key=r'z_k=4[\cos(\pi/6+2\pi k/3)+i\sin(\pi/6+2\pi k/3)]')

# 6. Gaussian elimination, ranks and general/particular solutions.
def gauss(n,A,b,solve=False,**kw):
 A=s.Matrix(A);b=s.Matrix(b);aug=A.row_join(b);echelon=aug.echelon_form();ra=A.rank();rb=aug.rank();state=1 if ra<rb else 2 if ra==A.cols else 3
 vals=[field('rank','Ранг A',ra),field('augmented','Ранг (A|b)',rb),field('type','Тип: 1 несовместна, 2 единственная, 3 бесконечно много',str(state),'choice',options=[dict(value=str(i)) for i in [1,2,3]])]
 last=r'\operatorname{rank}A='+str(ra)+r',\quad\operatorname{rank}(A|b)='+str(rb)
 if solve and ra==rb:
  sol,params=A.gauss_jordan_solve(b);sol=sol.subs({p:t for p in params});part=sol.subs(t,0)
  vals.extend([field('general','Общее решение (x₁;x₂;x₃), параметр t',vec(sol),'affine'),field('particular','Любое частное решение (x₁;x₂;x₃)',vec(part),'system-point',matrix=[list(map(int,A.row(i))) for i in range(A.rows)],rhs=list(map(int,b)))])
  last+=r'\\X='+tx(sol)+r',\quad X_0='+tx(part);verify(n,'general solution and particular satisfy all equations',s.simplify(A*sol-b)==s.zeros(A.rows,1))
 task=fields(n,6,'Метод Гаусса и совместность СЛАУ',r'\begin{cases}'+r'\\'.join(tx(sum(A[i,j]*s.Symbol('x_'+str(j+1)) for j in range(A.cols)))+'='+tx(b[i]) for i in range(A.rows))+r'\end{cases}',vals,steps(r'\operatorname{rank}A=\operatorname{rank}(A|b)\iff\text{совместна}',r'(A|b)='+tx(aug),r'(A|b)\sim'+tx(echelon),r'\begin{gathered}'+last+r'\end{gathered}',notes=['Одинаковые преобразования выполняем над всей строкой расширенной матрицы.','Добавляем столбец правых частей.','Убираем элементы под ведущими. Ранг равен числу ненулевых строк ступенчатой матрицы.','При равных рангах и r<n есть n-r свободных переменных. Общее решение не зависит от выбора параметризации.']),**kw)
 verify(task['id'],'ranks preserved by echelon reduction',aug.rank()==echelon.rank());return task
gauss(44,[[-1,1,2],[-1,3,-2],[2,-5,2]],[3,10,-18])
gauss(45,[[-1,1,2],[-1,3,-2],[2,-5,-1]],[3,1,0])
gauss(46,[[1,-3,2],[2,-5,8],[4,-9,20]],[-7,-8,-10],True)

# 7. Applied vector and electrical problems.
def mechanics(n,F,A,B,moment=False,**kw):
 F,A,B=map(s.Matrix,[F,A,B]);r=B-A;result=r.cross(F) if moment else F.dot(r)
 task=add(n,7,'Момент силы' if moment else 'Работа силы',r'F='+tx(F)+r',\quad '+points_prompt(O=A,P=B) if moment else r'F='+tx(F)+r',\quad '+points_prompt(A=A,B=B),vec(result) if moment else result,steps(r'M_O=\overrightarrow{OP}\times F' if moment else r'W=F\cdot\overrightarrow{AB}',r'r='+tx(r),(r'r\times F=' if moment else r'F\cdot r=')+tx(result),('M_O=' if moment else 'W=')+tx(result)),kind='vector' if moment else 'number',**kw)
 task['instruction']='Найди момент силы относительно O: (Mx;My;Mz).' if moment else 'Найди работу силы на перемещении A → B.'
 verify(task['id'],'moment orthogonal to lever and force' if moment else 'dot product recomputed coordinatewise',result.dot(F)==0 and result.dot(r)==0 if moment else result==sum(F[i]*r[i] for i in range(3)));return task
mechanics(47,[2,-4,5],[3,2,-1],[4,-2,3],True)
mechanics(48,[2,-1,-4],[1,-2,3],[5,-6,1])
mechanics(49,[3,0,4],[0,0,0],[2,-1,-1]);tasks[-1]['prompt']=r'F_1=(1;-1;1),\quad F_2=(2;1;3),\quad O=(0;0;0),\quad M=(2;-1;-1)';tasks[-1]['stages'][1]['blocks'].insert(0,block('Сначала складываем силы.',r'F=F_1+F_2=(3;0;4)'))
def electric(n,value,name,**kw):
 result=s.expand_complex(1/value);other='Y' if name=='Z' else 'Z';vals=[field('complex',f'{other} = 1/{name}',ans(result),'complex'),field('active','Активная составляющая |Re|',abs(s.re(result))),field('reactive','Реактивная составляющая |Im|',abs(s.im(result)))]
 task=fields(n,7,'Комплексное сопротивление и проводимость',name+'='+tx(value),vals,steps(r'\frac1{a+bi}=\frac{a-bi}{a^2+b^2}',other+r'=\frac{'+tx(s.conjugate(value))+'}{'+tx(s.re(value)**2+s.im(value)**2)+'}',other+'='+tx(result),r'|\Re|='+tx(abs(s.re(result)))+r',\quad|\Im|='+tx(abs(s.im(result)))),**kw)
 verify(task['id'],'reciprocal product equals one',s.simplify(result*value)==1);return task
electric(50,3+5*s.I,'Z');issue(tasks[-1],'В итоговой строке примера 3.50 ошибочно указано -3i/34. Правильно Y=(3-5i)/34, как следует из самого вычисления.')
electric(51,3-2*s.I,'Y')

# 8 and 10. Matching: separate answer field for each numbered item.
def matching(n,group,topic,left,right,correct,formula,explanation,letters=None,**kw):
 letters=letters or list('АБВГДЕ');labels={letter:text for letter,text in zip(letters,right)}
 vals=[field(str(i+1),f'{i+1}. {title}',str(letters.index(v)+1)) for i,(title,v) in enumerate(zip(left,correct))]
 description='\n'.join(f'{letters.index(k)+1} ({k}) - {v}' for k,v in labels.items())
 task=fields(n,group,topic,r'\text{Установи соответствие}',vals,steps(formula,r'\text{Проверяем каждый пункт отдельно.}',explanation,r',\quad '.join(str(i+1)+r'\mapsto\text{'+v+'}' for i,v in enumerate(correct))),description=description,**kw)
 task['instruction']='В каждом поле укажи номер подходящего варианта: '+', '.join(f'{i+1} = {v}' for i,v in enumerate(letters[:len(right)]))+'.';return task
matching(52,8,'Уравнения поверхностей',['x²/7 + z²/9 = y','x² + y²/4 - z²/3 = 0','x²/5 - y²/3 + z²/4 = 1'],['Конус','Эллиптический параболоид','Параболический цилиндр','Однополостный гиперболоид'],['Б','А','Г'],r'++=\text{линейная координата}\Rightarrow\text{параболоид}',r'++-=0\Rightarrow\text{конус},\quad ++-=1\Rightarrow\text{однополостный гиперболоид}')
matching(53,8,'Геометрические объекты прямой',['Направляющий вектор','Вектор нормали','Точка прямой'],['(-3;2)','(5;1)','(1;-5)','(3;2)'],['В','Б','А'],r'\frac{x+3}{1}=\frac{y-2}{-5},\quad s=(1;-5)',r'n=(5;1),\quad n\cdot s=0,\quad M=(-3;2)')
issue(tasks[-1],'В пояснении примера 3.53 направляющий вектор ошибочно назван объектом Г. По списку и итоговому ответу он соответствует В.')
matching(54,8,'Аргументы комплексных чисел',['√3 - i√3','-5','-√3 + 3i'],['π','-π/4','2π/3','-π/3'],['Б','А','В'],r'\varphi=\operatorname{Arg}z\in(-\pi;\pi]',r'\varphi_1=-\pi/4,\quad\varphi_2=\pi,\quad\varphi_3=2\pi/3')
matching(55,8,'Направляющие векторы прямых',['(x-3)/2=(y+2)/(-1)=(z-5)/4','x=2+3t, y=-1-2t, z=4+5t','x-y+2z-1=0; 2x+y-z+4=0'],['(3;-2;5)','(2;-1;4)','(-1;5;3)','(-1;-5;3)'],['Б','А','Г'],r's=n_1\times n_2\quad\text{для пересечения плоскостей}',r'(1;-1;2)\times(2;1;-1)=(-1;5;3)')
# Cross product is (-1,5,3), i.e. option В. Preserve source options and use the verified value.
tasks[-1]['fields'][-1]['answer']='3';tasks[-1]['answer']=json.dumps({f['id']:f['answer'] for f in tasks[-1]['fields']},ensure_ascii=False);tasks[-1]['stages'][-1]['blocks'][0]['tex']=r'1\mapsto\text{Б},\quad2\mapsto\text{А},\quad3\mapsto\text{В}'
verify(55,'cross product of normals',s.Matrix([1,-1,2]).cross(s.Matrix([2,1,-1]))==s.Matrix([-1,5,3]))
def theory_choice(n,group,topic,options,correct,formula,key,multi=False,**kw):
 return add(n,group,topic,r'\text{Проверь утверждения}',correct,steps(formula,r'\text{Сопоставляем условия каждого утверждения с определением.}',key,r'\text{Ответ: }'+correct.replace(';',r',\ ')),kind='multi' if multi else 'choice',options=[dict(value=str(i+1),label=o) for i,o in enumerate(options)],instruction='Выбери все верные утверждения.' if multi else 'Выбери ошибочное утверждение.',**kw)
theory_choice(56,9,'Когда существует обратная матрица',['Квадратная матрица обратима тогда и только тогда, когда невырожденна.','Квадратная матрица обратима тогда и только тогда, когда det A = 0.','Квадратная матрица обратима тогда и только тогда, когда ранг равен числу строк.','Квадратная матрица невырожденна тогда и только тогда, когда ранг равен числу столбцов.'],'1;3;4',r'A^{-1}\text{ существует}\iff\det A\ne0\iff\operatorname{rank}A=n',r'\text{Пункт 2 противоречит критерию: определитель должен быть ненулевым.}',True)
theory_choice(57,9,'Свойства векторного произведения',['a×b = -b×a','a×b = b×a','|a×b| = |a||b| cos φ','|a×b| = |a||b| sin φ'],'1;4',r'a\times b=-b\times a,\quad |a\times b|=|a||b|\sin\varphi',r'\cos\varphi\text{ относится к скалярному произведению.}',True)
theory_choice(58,9,'Плоскости и прямые: ошибка в формуле',['Если D=0, плоскость Ax+By+Cz+D=0 проходит через начало координат.','Расстояние до плоскости равно |Ax₀+By₀+Cz₀+D|/√(A²+B²+C²).','Каноническая прямая через M₀: (x+x₀)/m=(y+y₀)/n=(z+z₀)/p.','Плоскость через M₀ с нормалью (A;B;C): A(x-x₀)+B(y-y₀)+C(z-z₀)=0.'],'3',r'\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}',r'\text{В пункте 3 неверные знаки перед координатами исходной точки.}')
theory_choice(59,9,'Фокусы и эксцентриситет гиперболы',['ε = √(a²-b²)/a','ε = √(a²+b²)/a','Расстояние между фокусами равно 2√(a²+b²).','Расстояние между фокусами равно 2√(a²-b²).'],'2;3',r'c^2=a^2+b^2,\quad\varepsilon=c/a,\quad F_1F_2=2c',r'\text{Для гиперболы }\varepsilon>1.',True)
matching(60,10,'Свойства определителя',['Переставить две строки','Прибавить к строке другую строку, умноженную на k','Умножить одну строку на k ≠ 0'],['Определитель не изменится','Определитель умножится на k','Определитель поменяет знак','Определитель уменьшится в k раз'],['В','А','Б'],r'\det(B)=\{-\det A,\ \det A,\ k\det A\}',r'\text{Изменение одной строки и всей матрицы - разные операции.}')
matching(61,10,'Классификация СЛАУ',['Совместная неопределённая','Совместная определённая','Несовместная'],['Единственное решение','Бесконечно много решений','Ровно два решения','Нет решений'],['Б','А','Г'],r'r=\operatorname{rank}A,\quad \bar r=\operatorname{rank}(A|b)',r'r<\bar r\Rightarrow\varnothing;\quad r=\bar r=n\Rightarrow1;\quad r=\bar r<n\Rightarrow\infty')
matching(62,10,'Критерии для векторов',['Два ненулевых вектора ортогональны','Два ненулевых вектора коллинеарны','Три ненулевых вектора компланарны'],['Смешанное произведение равно нулю','Скалярное произведение равно нулю','Векторное произведение равно нулю'],['Б','В','А'],r'a\cdot b=0,\quad a\times b=0,\quad(a,b,c)=0',r'\text{Сначала различаем скалярное, векторное и смешанное произведения.}')
matching(63,10,'Канонические уравнения поверхностей',['Эллипсоид','Однополостный гиперболоид','Двуполостный гиперболоид','Конус'],['x²/a²-y²/b²-z²/c²=1','x²/a²+y²/b²+z²/c²=1','x²/a²+y²/b²=z²/c²','x²/a²+y²/b²-z²/c²=1','x²/a²+y²/b²=2z'],['Б','Г','А','В'],r'+++ =1,\quad ++-=1,\quad +--=1,\quad ++-=0',r'\text{Число отрицательных квадратов и правая часть определяют тип.}')

# Exact sample-ticket cross references. Distinct printed conditions remain distinct cards.
for n,g,v,p in [(1,1,1,1),(2,1,2,1),(7,1,5,1),(8,1,6,1),(9,1,8,1),(12,2,2,1),(13,2,3,1),(14,2,4,2),(20,3,2,2),(21,3,3,2),(22,3,4,2),(15,3,5,2),(16,3,6,2),(17,3,7,2),(18,3,8,2),(23,4,1,2),(24,4,2,2),(25,4,3,2),(26,4,4,3),(27,4,5,3),(28,4,6,3),(29,4,7,3),(30,4,8,3),(31,4,9,3),(32,4,10,3),(33,5,1,3),(34,5,2,3),(35,5,3,3),(37,5,4,3),(38,5,5,3),(41,5,7,3),(46,6,1,4),(47,7,1,4),(48,7,2,4),(49,7,3,4),(50,7,4,4),(51,7,5,4),(52,8,2,5),(54,8,4,5),(55,8,5,5),(56,9,1,6),(57,9,2,6),(58,9,3,6),(59,9,4,6),(60,10,1,7),(61,10,2,7),(62,10,3,7),(63,10,4,8)]:dm(n,g,v,p)
def demo_kw(g,v,p):return dict(file='linear-ticket',page=p,label=f'Образец · №{g} · вариант {v}')
demo(matrix_product('la-demo-1-3',[[2,3],[-4,-2],[2,2]],[[-2,-2,-2],[-1,-3,3]],'ATBT',**demo_kw(1,3,1)),1,3,1)
demo(matrix_product('la-demo-1-4',[[2,3],[-4,-2],[2,2]],[[-2,-2,-2],[-1,-3,3]],'BTAT',**demo_kw(1,4,1)),1,4,1)
demo(matrix_equation('la-demo-1-7',[[2,-1],[-4,3]],[[-1,4,0],[3,1,-2]],[[7,2,1],[6,-6,1]],**demo_kw(1,7,1)),1,7,1)
demo(vector_problem('la-demo-2-1','cos',[-1,0,2],[0,2,1],[-3,2,4],**demo_kw(2,1,1)),2,1,1);tasks[-1]['prompt']=points_prompt(A=[0,2,1],B=[-3,2,4],C=[-1,0,2]);tasks[-1]['instruction']='Найди косинус угла C треугольника ABC.'
demo(projection_line('la-demo-3-1',[1,0,-1],[-1,1,0],[1,2,3],r'P(1;0;-1),\quad\frac{x+1}{1}=\frac{y-1}{2}=\frac z3',True,**demo_kw(3,1,2)),3,1,2)
demo(complex_power('la-demo-5-6',3-s.sqrt(3)*s.I,16,r'(3-\sqrt3i)^{16}',**demo_kw(5,6,3)),5,6,3)
A=s.Matrix([[3,-2,1],[0,-4,2],[-1,1,1]]);minor_vals=[A.minor_submatrix(i,j).det() for i,j in [(0,1),(1,1),(2,0)]]
demo(matching('la-demo-8-1',8,'Миноры элементов матрицы',['M₁₂','M₂₂','M₃₁'],['4','2','-2','0'],[list('АБВГ')[[4,2,-2,0].index(v)] for v in minor_vals],r'M_{ij}=\det A_{\widehat i,\widehat j}',r'M_{12}=2,\quad M_{22}=4,\quad M_{31}=0',**demo_kw(8,1,4)),8,1,4);tasks[-1]['prompt']='A='+tx(A)
demo(matching('la-demo-8-3',8,'Объекты прямой на плоскости',['Направляющий вектор','Вектор нормали','Точка прямой'],['(-3;2)','(5;1)','(1;-5)','(3;-2)'],['В','Б','А'],r'\frac{x+3}{1}=\frac{y-2}{-5}',r's=(1;-5),\quad n=(5;1),\quad M=(-3;2)',**demo_kw(8,3,5)),8,3,5)
assert len(demo_map)==56,len(demo_map)

# Two complete independent practice tickets, with verified answers rather than a copied key.
def ticket_kw(ticket,num):return dict(file='linear-essentials',page=(65 if num==10 else 64) if ticket==1 else 66,label=f'Тренировочный билет {ticket} · №{num}')
matrix_product('la-ticket-1-1',[[-2,1,-2],[-1,-3,3]],[[2,4],[-4,-2],[2,2]],'ATBT',**ticket_kw(1,1))
vector_problem('la-ticket-1-2','area',[3,-4,3],[0,2,-3],[2,4,-2],**ticket_kw(1,2))
# Second line is intersection of two planes. Q and its direction are found exactly.
Q=s.Matrix([s.Rational(5,6),s.Rational(17,3),0]);d=s.Matrix([8,-1,-1]).cross(s.Matrix([2,-1,1]))
intersection('la-ticket-1-3',[1,2,-1],[1,5,3],Q,d,r'\frac{x-1}{1}=\frac{y-2}{5}=\frac{z+1}{3},\quad\begin{cases}8x-y-z-1=0\\2x-y+z+4=0\end{cases}',**ticket_kw(1,3))
# A valid point on both planes: solve at z=0 instead of relying on the printed answer key.
verify('ticket1-line-point','point lies on both planes',8*Q[0]-Q[1]-1==0 and 2*Q[0]-Q[1]+4==0)
conic('la-ticket-1-4','ellipse',2,0,s.Integer(100),s.Integer(64),r'F_1(2;-6),\quad F_2(2;6),\quad b=8',True,**ticket_kw(1,4))
complex_roots('la-ticket-1-5',z**4+s.Rational(1,2)-s.I*s.sqrt(3)/2,[s.cos(s.pi/6+s.pi*k/2)+s.I*s.sin(s.pi/6+s.pi*k/2) for k in range(4)],**ticket_kw(1,5))
gauss('la-ticket-1-6',[[1,-1,-2],[2,-2,1],[4,-4,-3]],[3,8,14],True,**ticket_kw(1,6))
issue(tasks[-1],'В таблице ответов к билету 1, №6 приведено частное решение (0;-3,75;0,4), которое не удовлетворяет исходным уравнениям. При x₁=0 правильно x₂=-19/5=-3,8, x₃=2/5=0,4. В карточке принимается любое верное частное решение.')
mechanics('la-ticket-1-7',[3,-2,6],[1,-2,3],[2,2,4],True,**ticket_kw(1,7))
A=s.Matrix([[3,-2,1],[0,-4,3],[-1,1,1]]);cof=[A.cofactor(i,j) for i,j in [(0,0),(0,1),(2,0),(2,2)]]
fields('la-ticket-1-8',8,'Алгебраические дополнения','A='+tx(A),[field(k,k,v) for k,v in zip(['A11','A12','A31','A33'],cof)],steps(r'A_{ij}=(-1)^{i+j}M_{ij}','A='+tx(A),r'A_{11}=-7,\ A_{12}=-3,\ A_{31}=-2,\ A_{33}=-12',r'A_{33}<A_{11}<A_{12}<A_{31}'),**ticket_kw(1,8))
theory_choice('la-ticket-1-9',9,'Взаимное расположение плоскостей',['Плоскости перпендикулярны при n₁·n₂=0.','Плоскости параллельны при n₁·n₂=0.','Плоскости совпадают, если коэффициенты их уравнений пропорциональны.','Параллельность нормалей: n₁×n₂=0.'],'2',r'\alpha\perp\beta\iff n_1\cdot n_2=0,\quad n_1\parallel n_2\iff n_1\times n_2=0',r'\text{Пункт 2 перепутал параллельность и перпендикулярность.}',**ticket_kw(1,9))
issue(tasks[-1],'В условии билета 1 в обеих плоскостях напечатано Cx вместо Cz. Карточка использует нормали (A;B;C), как предполагают варианты ответа. Пропорциональность понимается через общий ненулевой множитель, без деления на нулевые коэффициенты.')
matching('la-ticket-1-10',10,'Преобразования определителя n-го порядка',['Переставить первый и третий столбцы','Умножить на 2 все строки','К первой строке прибавить третью'],['Определитель умножится на 2ⁿ','Определитель поменяет знак','Определитель умножится на 2','Определитель не изменится'],['Б','А','Д'],r'\det(2A)=2^n\det A',r'\text{Каждая из }n\text{ строк даёт свой множитель 2.}',letters=['А','Б','С','Д'],**ticket_kw(1,10))
matrix_equation('la-ticket-2-1',[[1,1],[2,3]],[[5,-1,3],[-2,2,4]],**ticket_kw(2,1))
vector_problem('la-ticket-2-2','cos',[1,2,0],[3,4,4],[2,2,1],**ticket_kw(2,2))
projection_line('la-ticket-2-3',[8,-2,7],[7,-8,6],[2,-2,1],r'M(8;-2;7),\quad\frac{x-7}{2}=\frac{y+8}{-2}=\frac{z-6}{1}',True,**ticket_kw(2,3))
conic('la-ticket-2-4','hyperbola',0,0,s.Integer(9),s.Integer(25),r'25x^2-9y^2+z^2-225=0,\quad z=0',extra=[field('distance','Расстояние между фокусами',2*s.sqrt(34))],**ticket_kw(2,4))
complex_roots('la-ticket-2-5',z**4-2*z**2+4,[a*s.sqrt(s.Rational(3,2))+b*s.I/s.sqrt(2) for a,b in [(1,1),(-1,1),(-1,-1),(1,-1)]],formula=r'w=z^2,\quad w^2-2w+4=0',key=r'w=1\pm i\sqrt3',**ticket_kw(2,5))
gauss('la-ticket-2-6',[[1,-2,2],[2,-2,5],[3,-4,7]],[1,4,5],True,**ticket_kw(2,6))
mechanics('la-ticket-2-7',[3,-1,6],[2,-2,4],[8,4,9],**ticket_kw(2,7))
theory_choice('la-ticket-2-8',8,'Проверка печатного условия',['Все три уравнения задают кривые второго порядка.','Первая запись содержит y³ и требует уточнения.'],'2',r'\deg F=2\quad\text{для кривой второго порядка}',r'2x^2+3y^3+12x-6y+9=0\quad\text{имеет степень 3.}',**ticket_kw(2,8))
tasks[-1]['prompt']=r'\begin{gathered}2x^2+3y^3+12x-6y+9=0\\x^2-4y^2+8x-24y=24\\y^2-2x+4y+2=0\end{gathered}';tasks[-1]['instruction']='Можно ли сопоставить все три записи с кривыми второго порядка?';issue(tasks[-1],'В первой записи билета 2, №8 напечатано y³. Не заменяем его молча на y²: исходное задание требует уточнения. Во второй строке гипербола, в третьей парабола.')
theory_choice('la-ticket-2-9',9,'Коллинеарность и ортогональность',['Для ненулевых векторов коллинеарность равносильна a×b=0.','Для ненулевых векторов ортогональность равносильна a·b=0.','Для ненулевых векторов коллинеарность равносильна a·b=0.'],'3',r'a\parallel b\iff a\times b=0,\quad a\perp b\iff a\cdot b=0',r'\text{В пункте 3 критерий ортогональности подменяет коллинеарность.}',**ticket_kw(2,9))
matching('la-ticket-2-10',10,'Типы поверхностей второго порядка',['x²/12+y²/4-z²/3=1','x²/12-y²/4-z²/3=1','x²/12-z²/3=1'],['Гиперболический цилиндр','Эллиптический параболоид','Однополостный гиперболоид','Двуполостный гиперболоид'],['В','Г','А'],r'++-=1,\quad+--=1,\quad\text{отсутствует координата}\Rightarrow\text{цилиндр}',r'\text{В третьем уравнении отсутствует }y.',**ticket_kw(2,10))

# The 30 official theoretical topics are added below by a separate source module.
from linear_theory import populate
populate(add,steps,stage,field,fields,pages)
assert len({t['id'] for t in tasks})==len(tasks)
for n in range(1,64):assert any(v['id']==f'la-example-{n:02}' for v in tasks)
for ticket in [1,2]:
 for num in range(1,11):assert any(v['id']==f'la-ticket-{ticket}-{num}' for v in tasks)
for task in tasks:
 # Remove duplicate source references attached to demo-only cards.
 task['sources']=list({(v['file'],v['page'],v['label']):v for v in task['sources']}.values())
tasks.sort(key=lambda v:(v['group'],0 if v['id'].startswith('la-example-') else 1 if v['id'].startswith('la-demo-') else 2 if v['id'].startswith('la-ticket-') else 3))
sections={'1':'Матрицы и уравнения','2':'Векторы','3':'Прямые и плоскости','4':'Кривые и поверхности','5':'Комплексные числа','6':'Метод Гаусса и СЛАУ','7':'Практические задачи','8':'Тестовые задачи','9':'Теория и вопросы курса','10':'Сопоставление'}
coverage=dict(total=len(tasks),source=sum(v['origin']=='source' for v in tasks),extra=sum(v['origin']=='extra' for v in tasks),groups={g:sum(v['group']==int(g) for v in tasks) for g in sections},sections=sections,sourceIssues=issues,sourceFiles=[dict(id=k,title=v) for k,v in FILES.items()],demoVariants=demo_map,notes=['Линейная алгебра и аналитическая геометрия, 1 семестр 2025–2026.','Включены все 56 вариантов десяти номеров образца, все 63 примера пособия и оба тренировочных билета.','К каждому из 30 вопросов официального списка добавлена авторская проверка понимания. Она не заменяет устный ответ по всем подпунктам.','Графики открываются в конце разбора. Для матриц, комплексных чисел и уравнений используются отдельные форматы ответа.','Отличающиеся условия образца и пособия сохранены отдельно. Найденные опечатки указаны в карточках.'])
for filename,data in [('linear-tasks',tasks),('linear-coverage',coverage),('linear-verification',verification)]:
 (ROOT/'data'/f'{filename}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
print(json.dumps({'tasks':len(tasks),'groups':coverage['groups'],'demo_variants':len(demo_map),'verified':len(verification),'issues':len(issues)},ensure_ascii=False))
