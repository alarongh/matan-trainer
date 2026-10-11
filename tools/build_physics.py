from pathlib import Path
import json,re,math
import sympy as s
from physics_problems import SPECS,a
from physics_formulas import FORMULAS
from physics_theory import THEORY
ROOT=Path(__file__).resolve().parents[1]
sections={1:'Кинематика и колебания',2:'Криволинейное движение',3:'Динамика точки',4:'Динамика вращения',5:'Импульс и столкновения',6:'Работа и энергия',7:'Момент импульса',8:'Качение и вращение',9:'Молекулярная физика',10:'Термодинамика'}
constants={'g':s.Rational('9.8'),'r':s.Rational('8.31'),'k':s.Rational('1.38e-23'),'na':s.Rational('6.02e23'),'c':s.Integer(300000000)}
index=json.loads((ROOT/'data/physics-source-index.json').read_text(encoding='utf8'));tasks=[];verification=[]
def expr(value,variables=(),g=None):
 scope={**constants,'sqrt':s.sqrt,'cos':s.cos,'sin':s.sin,'ln':s.log,'exp':s.exp,'abs':s.Abs,'pi':s.pi}
 scope.update({v:s.Symbol(v,real=True) for v in variables})
 if g is not None:scope['g']=s.Rational(str(g))
 return s.sympify(value.replace('^','**'),locals=scope)
def ans(value,variables=()):return s.sstr(expr(value,variables)).replace('**','^').replace('log(','ln(').replace('Abs(','abs(')
def step(title,note='',tex='',**kw):return {'title':title,'blocks':[{'note':note,'tex':tex,**kw}]}
def unittex(unit):return r'\;\text{'+unit+'}' if unit else ''
def output(value,unit,variables=()):
 e=expr(value,variables);return (s.latex(e) if variables else s.latex(s.N(e,7)))+unittex(unit)
def description(row):
 text=row['text'].replace('*','').strip()
 # Visually checked superscripts lost by PDF text extraction. Ordinary 102 m/s in 5.7 stays unchanged.
 changes={'4.1':{'1024':'10²⁴','106':'10⁶'},'7.2':{'1024':'10²⁴','106':'10⁶'},'9.5':{'1020':'10²⁰'},'9.18':{'1013':'10¹³'}}
 for old,new in changes.get(row['number'],{}).items():text=text.replace(old,new)
 text=re.sub(r'м/с\s*2','м/с²',text);text=re.sub(r'кг[·×]м\s*2','кг·м²',text)
 return text
by_number={}
for row in index:
 number=row['number']
 if number=='10.28':number+='a' if row['occurrence']==1 else 'b'
 by_number.setdefault(number,[]).append(row)
for number,rows in by_number.items():
 spec=SPECS[number];row=rows[0];group=int(number.split('.')[0]);variables=spec.get('variables',[])
 task={'id':'ph-problem-'+number.replace('.','-'),'group':group,'topic':sections[group]+' · '+number,'prompt':r'\text{'+('Разбери условие' if spec.get('review') else 'Найди итоговый ответ')+'}', 'description':description(row),'meta':'Задача '+number.replace('a',' (нагрев)').replace('b',' (вода)'),'origin':'source','kind':'number','sources':[{'file':r['file'],'page':r['page'],'label':('Д/з '+('1' if r['file'].endswith('-1') else '2') if 'homework' in r['file'] else 'Список задач')+' · '+r['number']+(' · второй пункт с этим номером' if r['occurrence']>1 else '')} for r in rows]}
 task['note']=spec.get('note','')+(' В оригинале для этой задачи требуется пояснительный рисунок.' if row['drawing'] else '')
 stages=[step('Нужные формулы','Выбери систему отсчёта и согласуй знаки.',spec['formula']),step('Постановка и преобразование',spec['reason'])]
 if spec.get('review'):
  task.update(kind='review',answer='',instruction='Разбери неоднозначность на бумаге и сверь рассуждение по этапам.',checklist=['Указал, каких данных или соглашений не хватает.','Различил возможные трактовки и их результаты.','Проверил физический смысл и единицы.'])
  stages.extend([step('Ключевой шаг','',spec['key']),step('Вывод',spec['conclusion'])])
 elif 'values' in spec:
  values=[];calcs=[];outs=[]
  for i,(label,value,unit) in enumerate(spec['values']):
   field={'id':'v'+str(i+1),'label':label+' ('+unit+')','kind':'number','answer':ans(value),'unit':unit,'tolerance':0.005}
   if 'g' in value:field['acceptedAnswers']=[ans(str(expr(value,g=gg))) for gg in [9.81,10]]
   values.append(field);calcs.append(r'x_{'+str(i+1)+'}='+s.latex(expr(value)));outs.append(r'x_{'+str(i+1)+r'}\approx '+output(value,unit))
  task.update(kind='fields',fields=values,answer=json.dumps({v['id']:v['answer'] for v in values}),instruction='Введи все итоговые значения в указанных единицах. КПД вводится долей, например 0,25.')
  stages.extend([step('Подстановка в СИ','Поля в порядке перечисленных результатов.',r'\begin{gathered}'+r'\\'.join(calcs)+r'\end{gathered}'),step('Ответ','',r'\begin{gathered}'+r'\\'.join(outs)+r'\end{gathered}')])
 else:
  unit=spec['unit'];value=spec['ans'];task.update(answer=ans(value,variables),unit=unit,tolerance=0.005,instruction='Введи итоговый ответ в единицах: '+unit+'.'+(' Выражение через '+', '.join(variables)+'.' if variables else ''))
  if variables:task.update(kind='expression',variables=variables)
  else:task['acceptedAnswers']=[ans(str(expr(value,g=gg))) for gg in [9.81,10]] if 'g' in value else []
  task['acceptedAnswers']=task.get('acceptedAnswers',[])+[ans(v,variables) for v in spec.get('accepted',[])]
  stages.extend([step('Подстановка и вычисление','Перевод единиц выполнен до вычислений.',s.latex(expr(value,variables)),**({'physicsDiagram':spec['diagram']} if spec.get('diagram') else {})),step('Ответ','Приближение округлено; в проверке допускается округление до 0,5%.',r'\boxed{'+output(value,unit,variables)+r'}')])
 task['stages']=stages;tasks.append(task)
 verification.append({'id':task['id'],'sourceNumber':number,'method':'Derived from the explicitly displayed physical law and SI substitution; ambiguous conditions are self-review.','answers':spec.get('ans',spec.get('values',spec.get('conclusion'))),'manual':bool(spec.get('review'))})
# The exam's five parameterized tasks, with A, B, C interpreted as multipliers.
demo=[('2*a/45','м/с²',[2],['a'],'Диаметр D=5A м, за 30 с путь 2D. Найди ускорение.','v=2D/30, R=D/2, a_n=v²/R.'),('5*(g-b)','Н',[3],['b'],'Тело массой 5 кг падает с ускорением B м/с². Найди сопротивление.','5g−F=5B.'),('4*b*c','кг·м/с',[5],['b','c'],'Сила 4B Н действует C секунд. Найди изменение импульса.','Δp=FΔt; заданная масса 2B кг здесь не нужна.'),('b*na/0.001','атомов',[9],['b'],'Найди число атомов в B кг водорода.','Молярная масса атомов H — 0,001 кг/моль; N=BN_A/0,001.'),('sqrt(14*0.03*c/(5*g*sin(pi/6)^2))','с',[2],['c'],'Сплошной шар из покоя скатывается под 30°; центр масс понизился на 3C см. Найди время.','a=5g sin30°/7, s=0,03C/sin30°, t=√(2s/a).')]
for i,(value,unit,groups,variables,text,reason) in enumerate(demo,1):
 tasks.append({'id':f'ph-exam-{i}','group':groups[0],'topic':f'Демонстрационный экзамен · №{i}','meta':f'Экзамен · №{i}','description':text,'prompt':r'A,B,C\in\{1,\ldots,9\}','origin':'source','kind':'expression','variables':variables,'unit':unit,'answer':ans(value,variables),'instruction':'Введи выражение через '+', '.join(variables)+' в единицах '+unit+'.','note':'Заглавные параметры в поле можно писать строчными. Принято: 5A означает 5×A, 4B — 4×B, 3C — 3×C. Для задачи о шаре используется качение без потерь энергии.','sources':[{'file':'physics-exam','page':1,'label':f'Экзамен · №{i}'}],'stages':[step('Нужные связи',reason),step('Перевод единиц','Параметры A, B, C — числа от 1 до 9, а не номера единиц измерения.'),step('Выражение через параметры','',s.latex(expr(value,variables))),step('Ответ','',output(value,unit,variables))]})
# Formula recall: every official topic, plus the three demo-specific variants.
demo_links={'m18':['1 · №1','2 · №3'],'g36':['1 · №2'],'radius':['1 · №3'],'angular-scalar':['1 · №4'],'g26':['1 · №5','2 · №9'],'m31':['1 · №6','2 · №4'],'g35':['1 · №7'],'full-accel':['1 · №8'],'m34':['1 · №9','2 · №5'],'m35':['1 · №10'],'m02':['2 · №1'],'m05':['2 · №2'],'g05':['2 · №6'],'g18':['2 · №7'],'g31':['2 · №8'],'g40':['2 · №10']}
for i,f in enumerate(FORMULAS):
 right=f['layout']
 for n,p in enumerate(f['parts']):right=right.replace('@'+str(n)+'@',p)
 option_tex=[right,*f['wrong'][:2]];rotation=i%3;option_tex=option_tex[rotation:]+option_tex[:rotation];correct=option_tex.index(right)+1
 tag=f['id'][2:];is_gas=tag.startswith('g');official=bool(re.fullmatch('[mg]\\d{2}',tag));sources=[]
 if official:sources.append({'file':'physics-topics','page':(2 if is_gas and int(tag[1:])<=27 else 3 if is_gas else 1 if int(tag[1:])<=33 else 2),'label':('МКТ и термодинамика' if is_gas else 'Механика')+' · тема '+str(int(tag[1:]))})
 sources.extend({'file':'physics-credit','page':1,'label':'Зачётный билет '+label} for label in demo_links.get(tag,[]))
 task={'id':'ph-formula-'+tag,'group':f['groups'][0],'topic':f['title'],'meta':('Формулы МКТ · ' if is_gas else 'Формулы механики · ')+tag,'origin':'source','kind':'choice','prompt':f['left']+r'=\;?','description':f['conditions'],'instruction':'Выбери правильную правую часть формулы. Для самостоятельного воспроизведения используй «Учить формулы».','answer':str(correct),'options':[{'value':str(n+1),'label':'Вариант '+str(n+1),'tex':v} for n,v in enumerate(option_tex)],'sources':sources,'note':'','stages':[step('Физический смысл',f['tip']),step('Условия применимости',f['conditions']),step('Собираем формулу','',f['left']+'='+right),step('Проверь обозначения',f['tip'])]};tasks.append(task)
program=json.loads((ROOT/'data/physics-program-index.json').read_text(encoding='utf8'));assert len(program)==len(THEORY)==22
for row,(group,formula,reason,end) in zip(program,THEORY):
 n=row['number'];tasks.append({'id':f'ph-theory-{n:02}','group':group,'topic':f'Экзаменационный вопрос {n}','meta':f'Программа · вопрос {n}','description':row['text'],'prompt':r'\text{Устное объяснение и вывод}','origin':'source','kind':'review','answer':'','instruction':'Объясни своими словами, выполни вывод на бумаге, затем сверь по этапам. Автоматической оценки устного ответа нет.','checklist':['Назвал определения и физический смысл величин.','Воспроизвёл связи и объяснил основные шаги вывода.','Указал условия применимости и ограничения.'],'sources':[{'file':'physics-program','page':row['page'],'label':f'Программа · №{n}'}],'note':'Подсказки — опорный конспект, а не полная замена лекции.','stages':[step('Опорные формулы','',formula),step('Рассуждение и вывод',reason),step('Вывод и границы модели',end),step('Самопроверка','Закрой разбор и объясни вопрос без чтения. Проверь себя по исходной программе и соответствующей лекции.')]})
tasks.sort(key=lambda t:(t['group'],t['id'].startswith('ph-formula'),t['id'].startswith('ph-theory')))
ids=[t['id'] for t in tasks];assert len(ids)==len(set(ids));assert len(by_number)==141
sourcefiles=[{'id':id,'title':title} for id,title in [('physics-problems','Список задач для подготовки'),('physics-homework-1','Домашняя работа №1'),('physics-homework-2','Домашняя работа №2'),('physics-credit','Демонстрационный зачёт: два билета'),('physics-exam','Демонстрационный экзамен'),('physics-topics','80 тем для подготовки к зачёту'),('physics-program','22 вопроса экзаменационной программы')]]
lecture_titles=['Кинематика точки','Криволинейное движение','Динамика точки','Сохранение механической энергии','Динамика твёрдого тела','Сохранение момента импульса','Свободные колебания','Затухающие и вынужденные колебания','Сложение колебаний','Специальная теория относительности','Основы МКТ и термодинамики','Степени свободы и Больцман','Статистика идеального газа','Первое начало термодинамики','Тепловые и холодильные машины','Второе начало термодинамики']
sourcefiles += [{'id':f'physics-lecture-{i:02}','title':f'Лекция {i}: {title}'} for i,title in enumerate(lecture_titles,1)]
coverage={'total':len(tasks),'source':len(tasks),'extra':0,'sections':sections,'groups':{g:sum(t['group']==g for t in tasks) for g in sections},'sourceFiles':sourcefiles,'notes':['Физика · часть 1, 1 семестр 2025–26. Все 125 задач списка и все 141 задачи домашних работ (повторы объединены по номеру; два разных №10.28 сохранены).','83 карточки формул: 80 тем списка и 3 дополнительных формулы демобилетов. Также 5 параметрических задач демонстрационного экзамена и 22 вопроса программы с самопроверкой.','Численные ответы вводятся в указанных единицах; допускается округление до 0,5%. g=9,8 м/с² (также принимаются согласованные расчёты с g=9,81 или 10), R=8,31 Дж/(моль·К), k_B=1,38·10⁻²³ Дж/К, N_A=6,02·10²³ моль⁻¹. Температура: T=t+273,15.','Неоднозначные условия и дополнительные модельные предположения отмечены в карточках. Устные выводы и рисунки требуют самопроверки; они не получают отметку автоматической правильности.','Лекции 1–16 доступны целиком в материалах. Конспекты не заменяют их содержание.'],'sourceIssues':[{'id':t['id'],'reason':t['note'] or t['stages'][-1]['blocks'][0]['note']} for t in tasks if t['id'].startswith('ph-problem') and (t['kind']=='review' or SPECS[t['id'].replace('ph-problem-','').replace('-','.')].get('note'))]}
for name,data in [('physics-tasks',tasks),('physics-coverage',coverage),('physics-verification',verification)]:
 (ROOT/'data'/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(ROOT/'src/physics-formulas.js').write_text('// Generated by tools/build_physics.py. Source topics and model conditions are retained.\nexport const physicsFormulas='+json.dumps(FORMULAS,ensure_ascii=False,indent=1)+';\n',encoding='utf8')
print(f'{len(tasks)} physics cards: {len(by_number)} unique problems, {len(FORMULAS)} formulas, 22 oral outlines, 5 exam tasks.')
