from bank_common import *

def verify(b):
 # Independent geometry checks: points lie on the curve and have the required slope.
 cases=[(4,x*x,[(2,4)],4),(5,x*x*(x-2)**2,[(0,0),(1,1),(2,0)],0),(6,1/(1+x*x),[(0,1)],0),(7,1/x,[(2,R(1,2)),(-2,-R(1,2))],-R(1,4)),(9,s.exp(x)+s.exp(-x),[(s.log(2),R(5,2))],R(3,2)),(10,s.sqrt(3*x+1),[(1,2)],R(3,4)),(34,(4**x-2**(x+1))/s.log(4),[(1,0)],2)]
 for i,f,points,k in cases:
  for px,py in points:
   b.verify(f'tangent-{i:02}','point lies on source curve',f.subs(x,px),py)
   b.verify(f'tangent-{i:02}','required tangent slope',s.diff(f,x).subs(x,px),k)
 for i,f,p,k,c in [(11,-3*x*x+2,1,-6,5),(12,3*x**3+4,2,36,-44),(13,x*x/2-3*x+1,4,1,-7),(14,2*x*x-4*x+3,0,-4,3),(14,2*x*x-4*x+3,R(5,2),6,-R(19,2)),(15,5*x**3-1,1,15,-11),(16,2*x*x-1,1,4,-3),(19,x*x-6*x+3,2,-2,-1)]:
  b.verify(f'tangent-{i:02}','line slope vs derivative',s.diff(f,x).subs(x,p),k)
  b.verify(f'tangent-{i:02}','line passes through tangency point',f.subs(x,p),k*p+c)
 b.verify('tangent-08','tangent passes through M for p=1/2', (1-R(1,2))+(3-R(1,2))*(2-1),3)
 b.verify('tangent-39','triangle determinant',abs(s.det(s.Matrix([[3,3],[5,R(5,2)]])))/2,R(15,4))
 for i,expected in [(11,18),(12,36),(13,65),(14,21),(15,25)]:
  b.verify(f'practical-{i:02}','rounded maximum vs independent reference',s.Integer(json.loads(b.find(f'practical-{i:02}')['answer'])['temperature']),expected)
 # Independent differentiation of the two mixed-derivative examples.
 z=s.asin(x/s.sqrt(x*x+y*y));d=s.diff(z,x,y)
 b.verify('demo-partial-1','mixed symbolic derivative at M',d.subs({x:0,y:1}),-1)
 b.verify('demo-partial-2','mixed symbolic derivative at M',s.diff(x**(2*y),x,y).subs({x:1,y:1}),2)
 b.verify('demo-parametric','parameter derivative at t=1',((s.diff(s.log(t)/t,t))/(s.diff(t*s.log(t),t))).subs(t,1),1)
 # Validate polynomial asymptotes against independent rational limits.
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
 transforms=standard_transformations+(implicit_multiplication_application,convert_xor)
 for task in [v for v in b.tasks if v['id'].startswith('asymptote-')]:
  prompt=task['prompt'][2:]
  if any(v in prompt for v in ['\\','|','{']):continue
  f=parse_expr(prompt,local_dict={'x':x},transformations=transforms)
  if not f.is_rational_function(x):continue
  lines=task['fields'][0]['answer'].split(';')
  declared=[]
  for line in lines:
   lhs,rhs=line.strip().split('=');a=parse_expr(rhs,local_dict={'x':x},transformations=transforms)
   if lhs=='y':
    for direction in [s.oo,-s.oo]:b.verify(task['id'],'linear asymptote residual at infinity',s.limit(f-a,x,direction),0)
   else:
    declared.append(a);assert abs(s.limit(f,x,a))==s.oo,(task['id'],a)
  num,den=s.fraction(s.cancel(f));poles=[v for v in s.solve(den,x) if v.is_real]
  assert set(poles)==set(declared),(task['id'],poles,declared)
