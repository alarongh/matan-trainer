"""Idempotent addition to the existing bank. Install sympy and mpmath to rebuild."""
import sys,json
from pathlib import Path
from bank_common import Bank
root=Path(__file__).resolve().parents[1]

def populate(bank):
 bank.tasks=[t for t in bank.tasks if not t['id'].startswith('textbook-')]
 bank.verification=[v for v in bank.verification if not v['id'].startswith('textbook-')]
 bank.issues=[v for v in bank.issues if not v['id'].startswith('textbook-')]
 from textbook_limits import populate as limits
 limits(bank);print('textbook limits',len(bank.tasks),flush=True)
 # Other source sections are loaded explicitly below.
 for module in ('textbook_calculus','textbook_advanced','textbook_graphs','textbook_applications','textbook_remaining'):
  __import__(module).populate(bank);print(module,len(bank.tasks),flush=True)
 new=[t for t in bank.tasks if t['id'].startswith('textbook-')]
 assert len(new)==1017 and len({t['id'] for t in bank.tasks})==len(bank.tasks)
 return bank

def coverage_update(bank,coverage):
 new=[t for t in bank.tasks if t['id'].startswith('textbook-')]
 coverage['sections']['11']='Остальные задания пособия'
 coverage.update(total=len(bank.tasks),source=sum(t['origin']=='source' for t in bank.tasks),extra=sum(t['origin']=='extra' for t in bank.tasks),groups={str(g):sum(t['group']==g for t in bank.tasks) for g in range(1,12)})
 coverage['sourceFiles']=[f for f in coverage['sourceFiles'] if f['id']!='textbook']+[{'id':'textbook','title':'Математический анализ (1 семестр). Учебное пособие · МИРЭА, 2019'}]
 coverage['textbook']={'cards':len(new),'exercises':837,'sections':{str(i):sum(t['id'].startswith(f'textbook-{i:02}-') for t in new) for i in range(1,27)},'scope':'Все варианты и подпункты практических задач 1–26. Полное исследование графиков и разрывы — письменная самопроверка с разбором; доказательства и геометрический смысл также требуют сверки на бумаге.','excluded':[],'reviewCards':sum(t['kind']=='review' for t in new)}
 issues=[i for i in coverage.get('sourceIssues',[]) if not i['id'].startswith('textbook-')]+bank.issues
 coverage['sourceIssues']=list({i['id']:i for i in issues}.values())
 note='Добавлены упражнения учебного пособия с исходной нумерацией и страницами; новые карточки доступны в фильтре «Учебное пособие».'
 if note not in coverage['notes']:coverage['notes'].append(note)
 return coverage

if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8')
 bank=Bank(root)
 populate(bank)
 coverage=coverage_update(bank,json.loads((root/'data/coverage.json').read_text(encoding='utf8')))
 for name,value in [('tasks',bank.tasks),('coverage',coverage),('verification',bank.verification)]:
  (root/f'data/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
 print(json.dumps(coverage['textbook'],ensure_ascii=False),flush=True)
