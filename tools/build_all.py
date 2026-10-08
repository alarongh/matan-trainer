import sys,json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import build_bank
from bank_common import Bank
from content_limits import populate as limits
from content_calculus import populate as calculus
from content_theory import populate as theory
from content_applications import populate as applications
root=Path(__file__).resolve().parents[1];bank=Bank(root)
for name,fn in [('limits',limits),('calculus',calculus),('theory',theory),('applications',applications)]:
 fn(bank);print(name,len(bank.tasks),flush=True)
# Cross-reference the worked ticket without duplicating identical cards.
from bank_common import source
worked={'demo-limit-1':4,'demo-limit-2':5,'demo-limit-3':5,'advanced-limit-21':6,'demo-derivative-1':6,'demo-derivative-2':7,'demo-derivative-3':7,'demo-implicit':8,'demo-inflection-1':9,'demo-inflection-2':11,'demo-inflection-3':10,'demo-asymptote-1':11,'demo-asymptote-2':13,'demo-asymptote-3':14,'demo-asymptote-4':14,'demo-partial-1':15,'demo-partial-2':16,'demo-electric':18}
for id,page in worked.items():bank.find(id)['sources'].append(source(page,'Разбор соответствующего варианта','solutions'))
from verify_extended import verify
verify(bank)
ids=[v['id'] for v in bank.tasks];assert len(ids)==len(set(ids))
sections={'1':'Чётность и ОДЗ','2':'Последовательности','3':'Замечательный предел','4':'Пределы функций','5':'Теория','6':'Производные и касательные','7':'Точки перегиба','8':'Асимптоты','9':'Частные производные','10':'Практические задачи'}
coverage=json.loads((root/'data/coverage.json').read_text(encoding='utf8'))
coverage.update(total=len(bank.tasks),source=sum(v['origin']=='source' for v in bank.tasks),extra=sum(v['origin']=='extra' for v in bank.tasks),groups={g:sum(v['group']==int(g) for v in bank.tasks) for g in sections},sections=sections,sourceIssues=bank.issues)
coverage['notes']=['Все десять номеров демобилета представлены интерактивно.','Все пронумерованные упражнения банка включены, исходные номера и повторы сохранены.','К 28 темам теоретического списка добавлены авторские вопросы для проверки понимания; они помечены отдельно.','Печатные ошибки и неоднозначности не исправляются молча: соответствующие карточки содержат пояснения.','История старых карточек №1–3 сохраняется: их идентификаторы не изменены.']
for name,value in [('tasks',bank.tasks),('coverage',coverage),('verification',bank.verification)]:
 (root/f'data/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
print(json.dumps({'total':coverage['total'],'groups':coverage['groups'],'source':coverage['source'],'extra':coverage['extra'],'issues':len(bank.issues)},ensure_ascii=False),flush=True)
