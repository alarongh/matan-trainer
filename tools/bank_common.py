import json
from pathlib import Path
import sympy as s
x=s.Symbol('x',real=True);n=s.Symbol('n',integer=True,positive=True)
t=s.Symbol('t',real=True);y=s.Symbol('y',real=True)
R=s.Rational
def tex(expr):return s.latex(expr,inv_trig_style='full')
def answer(expr):
 if expr==s.oo:return 'infinity'
 if expr==-s.oo:return '-infinity'
 return s.sstr(expr).replace('**','^').replace('E','e')
def block(note='',math=''):return {'note':note,'tex':math}
def stage(title,*blocks):return {'title':title,'blocks':list(blocks)}
def source(page,label,file='bank'):return {'file':file,'page':page,'label':label}
class Bank:
 def __init__(self,root):
  self.root=Path(root);self.tasks=json.loads((self.root/'data/tasks.json').read_text(encoding='utf8'));self.verification=json.loads((self.root/'data/verification.json').read_text(encoding='utf8'));self.issues=[]
 def add(self,id,group,topic,prompt,ans,stages,page,label,kind='number',**kwargs):
  task={'id':id,'group':group,'topic':topic,'prompt':prompt,'answer':ans,'stages':stages,'sources':[source(page,label)],'origin':'source','kind':kind,'note':'','meta':label,**kwargs};self.tasks.append(task);return task
 def find(self,id):return next(v for v in self.tasks if v['id']==id)
 def verify(self,id,method,result,expected):
  assert result==expected or s.simplify(result-expected)==0,(id,result,expected)
  self.verification.append({'id':id,'method':method,'result':str(result),'passed':True})
 def issue(self,id,reason):self.issues.append({'id':id,'reason':reason})
 def invalid(self,id,group,topic,prompt,description,reason,page,label,details=None):
  task=self.add(id,group,topic,prompt,'2',[
   stage('Проверка условия',block('До вычислений нужно проверить область определения и наличие всех аргументов.',details or r'\text{Сначала проверяем, определено ли выражение.}')),
   stage('Проверяем печатную запись',block(reason)),
   stage('Что нужно уточнить',block('Исходная запись сохранена. Произвольная подстановка недостающего аргумента или замена точки меняет задачу.')),
   stage('Вывод',block('По указанному условию требуемый результат однозначно получить нельзя. Для решения исправленного варианта нужно уточнение преподавателя.')),
  ],page,label,kind='choice',description=description,instruction='Можно ли получить требуемый результат по этой печатной записи?',options=[{'value':'1','label':'Да, условие корректно и достаточно.'},{'value':'2','label':'Нет, условие требует уточнения.'}],note='Особенности исходной записи разобраны в подсказках.')
  self.issue(id,reason);return task
 def fields(self,id,group,topic,prompt,fields,stages,page,label,**kwargs):
  return self.add(id,group,topic,prompt,json.dumps({f['id']:f['answer'] for f in fields},ensure_ascii=False),stages,page,label,kind='fields',fields=fields,**kwargs)
def field(id,label,ans,kind='number',**kwargs):return {'id':id,'label':label,'answer':ans,'kind':kind,**kwargs}
def four(formula,first,key,last,notes=None):
 notes=notes or ['','','',''];return [stage('Нужные формулы',block(notes[0],formula)),stage('Первое преобразование',block(notes[1],first)),stage('Ключевой шаг',block(notes[2],key)),stage('Ответ',block(notes[3],last))]
