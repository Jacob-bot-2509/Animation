from pathlib import Path
import json,sys,copy
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as c
p=O/'current-complete-signatures.jsonl';ss=list(map(json.loads,p.read_text('utf-8').splitlines()));before=copy.deepcopy(ss)
for s in ss:
 if s['id']=='eval-linalg-030-s2':s['decisive_steps']=['按输入顺序逐次投影','非零缩放保持各阶段正交方向']
 if s['id']=='eval-prob-001-s2':s['decisive_steps']=['公平开门附加规则下的条件概率演示','任意合法主持人规则下W={C≠I}','按初选分布求全概率'];s['key_conditions']=['车门均匀且独立于初选','主持人知情且只开未选羊门','总提供换门机会']
 if s['id']=='eval-prob-001-s3':s['decisive_steps']=['按I=i分行加权枚举q_i/3','W={C≠I}','全概率求和2/3'];s['key_conditions']=['车门均匀且独立于初选','初选分布任意','合法开羊门并总提供换门机会']
p.write_text(''.join(json.dumps(s,ensure_ascii=False,sort_keys=True)+'\n'for s in ss),encoding='utf-8',newline='\n')
(O/'signature-descriptor-changes.json').write_bytes(c.encoded([{'before':a,'after':b}for a,b in zip(before,ss)if a!=b]))
print(json.dumps({'updated_descriptors':sum(a!=b for a,b in zip(before,ss))}))
