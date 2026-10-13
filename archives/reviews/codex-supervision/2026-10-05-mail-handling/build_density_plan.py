from pathlib import Path
import json,hashlib,sys,datetime,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from animtrain.kp_rule import kp_signature
assert ROOT.name=='Animation-Model-Training' and OUT.is_relative_to(ROOT)
G=[
('数学分析','导数与切线','calc-derivative-001','隐函数或参数曲线的切线；存在性与多切点分支'),
('数学分析','无穷限反常积分','calc-improper-002 calc-param-improper-003','有限端点与无穷端点；参数收敛范围；比较判别与求值分离'),
('数学分析','二重积分与区域','calc-double-integral-004','换积分次序；非圆形区域；极坐标雅可比与符号变化'),
('数学分析','格林公式','calc-green-005','方向反转；有洞区域；公式适用条件与补边处理'),
('数学分析','函数极限','calc-limit-006','不同函数增长类型；单侧极限与不存在；含参消去主项'),
('数学分析','直角坐标面积与分段','calc-area-007 calc-area-010 calc-area-011 calc-area-013','交点个数改变；交换上下界；绝对值分段与反向按y积分'),
('数学分析','极坐标面积','calc-area-008','多瓣区域；重复描绘与覆盖次数；内外曲线交叠'),
('数学分析','参数曲线面积','calc-area-009','参数非单调；有向面积与实际面积；自交区域分解'),
('数学分析','旋转体体积','calc-vol-012','圆盘与柱壳；空腔；旋转轴平移导致分段'),
('数学分析','交错级数与绝对收敛','calc-series-015','单调性不满足；绝对与条件边界；余项界'),
('数学分析','幂级数收敛域与和函数','calc-series-016 calc-series-018','端点分支；微积分运算合法性；不可直接代值的新的函数结构'),
('数学分析','函数项级数一致收敛','calc-series-017','区间改变；一致与逐点区别；交换极限/积分条件与反例'),
('数学分析','裂项级数与求和','calc-series-019','需重组的分解结构；余项估计；是否可裂项的反例'),
('数学分析','傅立叶展开','calc-series-020','奇偶延拓；分段函数；间断点取值与系数推导'),
('解析几何','直线与平面夹角','geom-020','平行垂直退化分支；逆向构造；从投影重建角度'),
('解析几何','两直线位置与距离','geom-021','相交/平行/异面分支；公垂线足点；条件限制下最短距离'),
('解析几何','平面方程与构造','geom-022','共线导致不唯一；点与方向联合条件；平面族参数'),
('解析几何','点到平面距离与投影','geom-023','多平面约束；反向求平面；投影迭代与可行性'),
('解析几何','柱面与方程的空间意义','geom-024','非坐标方向母线；平面截线；曲线方程与曲面方程辨析'),
('解析几何','二次曲面分类与截面','geom-025 geom-026','交叉项或平移；参数退化；截面空集/点/椭圆等分支'),
('解析几何','直线与二次曲面交点','geom-027','参数下切割/相切/无交；非正定曲面；几何与代数相互验证'),
('解析几何','直纹性与母线','geom-028','构造母线与证否；曲面类型变化；局部与全局直线区别'),
('解析几何','等距变换','geom-029','合成与逆变换；旋转中心/轴；反射与保持量'),
('解析几何','仿射变换与曲面','geom-030','非对角剪切；可逆性边界；二次型变换及面积/体积因子'),
('解析几何','空间交线参数化','geom-031','分支覆盖；隐式到参数式；参数奇点与空间位置'),
('高等代数','线性变换的几何解释','linalg-048','剪切与不可对角化；核的几何意义；逆变换与复合'),
('高等代数','谱分解与对角化','linalg-049 linalg-064 linalg-068','重根不可对角化；维数变化；特征方向随参数改变'),
('高等代数','行列式几何意义','linalg-050 linalg-053','有向面积与体积；秩亏退化；符号变化与体积因子'),
('高等代数','多项式因式分解与根','linalg-051','重根；复根配对；含参根分类与重数证明'),
('高等代数','多项式平移展开','linalg-052','基变换系数；逆向重建；高阶余项与适用范围辨析'),
('高等代数','克拉默法则','linalg-054','奇异参数分支；存在性与唯一性；分母为零时改用秩'),
('高等代数','线性方程组解空间','linalg-055 linalg-056','参数相容性；齐次与非齐次关联；基础解系与仿射解空间'),
('高等代数','矩阵求逆与可逆性','linalg-057','分块/初等变换；含参奇异边界；右逆与左逆区别'),
('高等代数','初等矩阵与操作','linalg-058','左乘与右乘；操作顺序；矩阵分解及逆操作'),
('高等代数','二次型标准形与惯性','linalg-059','退化与不定分支；合同与相似区别；维数变化'),
('高等代数','二次型正定性','linalg-060','半正定边界；不同判别法；参数全范围与反例构造'),
('高等代数','基与坐标变换','linalg-061','抽象多项式空间；变换方向；复合过渡与线性相关辨析'),
('高等代数','子空间和与交','linalg-062','不同维数；交集基构造；维数公式及约束变化'),
('高等代数','线性映射核与像','linalg-063','非单射/非满射；多项式微分映射；复合映射的秩零度'),
('高等代数','λ矩阵不变因子','linalg-065','非对角项；互素与非互素分支；行列式因子到不变因子'),
('高等代数','若尔当标准形','linalg-066','重根分块；核维数序列；广义特征向量链'),
('高等代数','正交变换','linalg-067','反射与旋转；合成；保持内积与行列式符号'),
('高等代数','对偶基与线性泛函','linalg-069','非标准基；维数变化；泛函坐标与配对不变性'),
('高等代数','辛形式与保持变换','linalg-070','保持条件验证；四维形式；退化交替形式与反例'),
('概率论','条件概率与独立性','prob-038','独立与互斥辨析；三事件条件化；不相容数据的可行性'),
('概率论','几何概型','prob-039','非均匀抽样不适用；区域切割；构造不同样本空间'),
('概率论','二项到泊松近似','prob-040','稀有事件极限条件；精确概率对照；不适用情形'),
('概率论','正态分布与参数','prob-041','标准化；区间概率与对称性；线性组合'),
('概率论','大数定律','prob-042','频率与概率区别；收敛方式；相关样本的适用条件'),
('概率论','中心极限定理','prob-043','中心化缩放；非正态总体；退化或无限方差时的限制'),
('概率论','贝叶斯后验','prob-044','多阶段观测；多类别；条件独立的成立与不成立'),
('概率论','随机变量函数的分布','prob-045','非单调多分支变换；原子与连续混合；联合变换及边界'),
('概率论','可列可加性','prob-046','重叠需先拆分；可列与不可列区别；极限事件与单调连续性')]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load_rows(p):
 return [(json.loads(line),line) for line in p.read_bytes().splitlines(keepends=True) if line.strip()]
m=json.loads((ROOT/'data/manifest.json').read_text('utf8'))
guards=['data/manifest.json','data/eval-v2.lock.json','data/test-v2.lock.json','data/asset_evidence.json','src/animtrain/kp_rule.py','src/animtrain/structural_leakage.py']+[str((Path('data')/e['path']).as_posix()) for e in m['entries']]
guards += [str(p.relative_to(ROOT).as_posix()) for d in ['data/b5-annotation-set','data/b5-calibration-report'] for p in (ROOT/d).rglob('*') if p.is_file()]
before={p:sha(ROOT/p) for p in guards}
active={};original={};sources={};catalog=[]
for e in m['entries']:
 if e['split']!='train':continue
 p=ROOT/'data'/e['path'];assert sha(p)==e['sha256']
 for n,(rec,line) in enumerate(load_rows(p),1):
  assert rec['id'] not in active;active[rec['id']]=(rec,line);sources[rec['id']]={'path':p.relative_to(ROOT).as_posix(),'line':n,'row_sha256':hashlib.sha256(line).hexdigest(),'file_sha256':sha(p)}
for p in sorted((ROOT/'data/v1/raw').glob('dataset_*.jsonl')):
 if p.stem not in ['dataset_calc','dataset_geom','dataset_linalg','dataset_prob']:continue
 for n,(rec,line) in enumerate(load_rows(p),1):
  assert rec['id'] not in original;original[rec['id']]=(rec,line)
  if rec['id'] not in sources:sources[rec['id']]={'path':p.relative_to(ROOT).as_posix(),'line':n,'row_sha256':hashlib.sha256(line).hexdigest(),'file_sha256':sha(p)}
assert len(active)==47 and len(original)==63 and set(active)<=set(original)
proposal=json.loads((ROOT/'reviews/codex-supervision/2026-10-05-leakage-policy-reassessment/REASSESSMENT_PROPOSAL.json').read_text('utf8'))
risks=set(proposal['proposed_isolated_ids']);restore=set(proposal['proposed_restore_ids']);assert len(risks)==14 and len(restore)==2
assert set(original)-set(active)==risks|restore
candidate={k:active.get(k,v) for k,v in original.items()}
assigned={};groups=[]
for n,(cat,label,ids,direction) in enumerate(G,1):
 members=ids.split();assert all(k in candidate and candidate[k][0]['category']==cat and k not in assigned for k in members)
 concept_id=f'C{n:02d}'
 for k in members:assigned[k]=concept_id
 active_ids=[k for k in members if k in active];known_risk_ids=[k for k in members if k in risks];unflagged=[k for k in members if k not in risks]
 groups.append({'concept_id':concept_id,'category':cat,'concept':label,'record_ids':members,'active_ids':active_ids,'candidate_ids':members,'known_risk_ids':known_risk_ids,'not_flagged_by_this_review_ids':unflagged,'active_count':len(active_ids),'candidate_count':len(members),'unflagged_count':len(unflagged),'active_gap_to_5':max(0,5-len(active_ids)),'active_gap_to_8':max(0,8-len(active_ids)),'candidate_gap_to_5':max(0,5-len(members)),'candidate_gap_to_8':max(0,8-len(members)),'unflagged_gap_to_5':max(0,5-len(unflagged)),'unflagged_gap_to_8':max(0,8-len(unflagged)),'draft_reserve_new':[5,8],'diversity_direction':direction,'grouping_status':'human_operational_taxonomy_not_calibrated','effective_diversity_verified':False})
assert set(assigned)==set(candidate)
pack=OUT/'candidate-recovery';pack.mkdir(exist_ok=False)
for family in ['calc','geom','linalg','prob']:
 path=pack/f'dataset_{family}.jsonl';members=[k for k in original if k.startswith(family+'-')]
 path.write_bytes(b''.join(candidate[k][1] for k in members));catalog.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'records':len(members),'active':False})
records=[]
for k in original:
 p=candidate[k][0];legacy_decimals=[]
 import re
 for field in ['problem','solution','answer']:
  if re.search(r'(?<![\w])\d+\.\d+',p.get(field,'')):legacy_decimals.append(field)
 records.append({'id':k,'concept_id':assigned[k],'source':sources[k],'active_before':k in active,'risk_status':'known_direct_template_overlap' if k in risks else ('proposed_restore_without_remaining_known_pair' if k in restore else 'not_flagged_in_existing_review'),'active_after':k in active,'candidate_only':True,'legacy_decimal_fields':legacy_decimals,'new_revision_must_use_fractions':True,'math_semantic_asset_verification':'not_granted_by_recovery'})
dump(pack/'candidate_catalog.json',{'schema':1,'active':False,'in_manifest':False,'records':records,'files':catalog,'count':63,'restored_candidate_only_ids':sorted(risks|restore),'known_risk_ids':sorted(risks),'user_per_question_review_required_for_new_drafts':True})
legacy=collections.Counter(kp_signature(v[0]) for v in original.values())
totals={'concepts':len(groups),'active_records':47,'candidate_records':63,'known_risk_records':14,'unflagged_candidate_records':49,'candidate_singleton_concepts':sum(g['candidate_count']==1 for g in groups),'active_empty_concepts':sum(g['active_count']==0 for g in groups),'candidate_empty_concepts':sum(g['candidate_count']==0 for g in groups),'legacy_coarse_groups':len(legacy),'formal_target_total':[5*len(groups),8*len(groups)],'nominal_candidate_new_to_target':[sum(g['candidate_gap_to_5'] for g in groups),sum(g['candidate_gap_to_8'] for g in groups)],'unflagged_new_to_target':[sum(g['unflagged_gap_to_5'] for g in groups),sum(g['unflagged_gap_to_8'] for g in groups)],'draft_reserve_new':[5*len(groups),8*len(groups)]}
report={'schema':1,'time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'source_message':'msg_1791175953295_434','user_authority':'direct delegation of mail handling; not acceptance of bounded production gate scope','active_counts':{'train':47,'eval':300,'test':150,'total':497},'manifest_sha256':before['data/manifest.json'],'source_reassessment_sha256':sha(ROOT/'reviews/codex-supervision/2026-10-05-leakage-policy-reassessment/REASSESSMENT_PROPOSAL.json'),'totals':totals,'concept_groups':groups,'risk_pair_count':sum(p['proposed_label']=='泄漏' for p in proposal['pairs']),'risk_pairs':[p for p in proposal['pairs'] if p['proposed_label']=='泄漏'],'candidate_files':catalog,'data_recovery_applied_to_active_manifest':False,'known_overlap_cannot_be_cured_by_density':True,'formal_training_ready':False,'calibrated':False,'asset_progress':'1/497','production_certificate_written':False,'legacy_label_files_unchanged':True,'interpretation':'draft 5-8 new candidates per weak concept; formally admit 5-8 genuinely diverse reviewed records per concept; overflow remains candidate-only'}
dump(OUT/'DATA_DIVERSITY_PLAN.json',report)
lines=['# 训练多样性与来信处理计划','',f'2026-10-05，接 Claude msg_434；用户直接授权邮件处理。已将16条撤出的原记录恢复到本目录非活动候选包，连同现有47条共63条。活动清单仍是47/300/150，共497条，冻结评测、资产证据与旧标签不变。首批已通过 msg_435 委托现有 Claude 会话起草15道补充题。','',
'## 密度口径与数量', '',f'人工逐题分为{len(groups)}个工作考点；不是所有数学知识的最终分类，也未校准为泄漏判断器。原63条中{totals["candidate_singleton_concepts"]}个考点仅1条；活动47条中{totals["active_empty_concepts"]}个考点无记录。旧规则只有{len(legacy)}个粗组：按动词分组会合并级数/面积，也会错归中心极限定理，不能用粗组计数代替细考点覆盖。', '',
f'若最终每考点5–8条，名义目标为{totals["formal_target_total"][0]}–{totals["formal_target_total"][1]}条；全部63条均计入时需新增{totals["nominal_candidate_new_to_target"][0]}–{totals["nominal_candidate_new_to_target"][1]}条。保留已知14条风险的隔离，只有49条未被本复核标记的候选，则至少需新增{totals["unflagged_new_to_target"][0]}–{totals["unflagged_new_to_target"][1]}条；未被标记不代表全量已证明无泄漏。', '',
f'邮件同时说“每薄弱考点补充5–8条”与“最终每考点5–8条”。执行时每考点可起草5–8道新增备选，共{totals["draft_reserve_new"][0]}–{totals["draft_reserve_new"][1]}道，再择优入库到5–8条有效多样样本，超出者留在候选区。数量为工程覆盖目标，不承诺模型效果。不能把同一题多方法、换数字或换符号当作独立变体数。', '',
'## 恢复与泄漏风险', '', 'linalg-060、prob-045：按既有独立复核建议可恢复，但本次只恢复候选原字节。四对边界题建议不泄漏；019/021判定沿用复核结果。其余14条/15对直接套解风险保留；全部原记录均在候选包可审阅，绝不因增加变体将这些已知风险改写为“无泄漏”。正式恢复这14条须先解决训练/评测隔离：选择保留隔离，或另建并审核独立评测版本；冻结评测原字节不得改。仅从指标分母隐藏污染记录也不能证明其余记录独立。','',
'候选包四个JSONL均不在活动manifest，无入库/放行效力；逐行来源与SHA、已知风险、原记录小数待改标记见candidate_catalog.json。为保留证据复制原字节，新题与新版本的可用有理数必须写分数。候选恢复不授权数学、语义或动画验收。', '',
'## 逐考点密度与补充方向', '', '| 编号 | 考点 | 活动 | 原候选 | 已知风险 | 候选补至5/8 | 新变体方向 |','|---|---|---:|---:|---:|---|---|']
for g in groups:lines.append(f'| {g["concept_id"]} | {g["category"]}：{g["concept"]} | {g["active_count"]} | {g["candidate_count"]} | {len(g["known_risk_ids"])} | {g["candidate_gap_to_5"]}/{g["candidate_gap_to_8"]} | {g["diversity_direction"]} |')
lines += ['', '逐题ID及其归组、活动与风险集合均在同名JSON，可逐条审阅，禁止以总体均值掩盖空考点。每组方向是训练考点设计，不提供冻结评测的题文或答案。', '', '## 起草、独立复验与入库顺序', '',
'1. 首批导数/切线、二次型正定性、随机变量函数分布，各5题；只写reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl与DRAFT_REPORT.md。题干、解答、答案、方法、scene_spec完整，标明难度、形式变化、原训练父项；禁止只改数值。','2. 用户逐题审阅新题；Codex独立核对条件完整性、定义域、分支、证明/计算、分数、scene_spec数学语义与跨集合直接套解风险。已见评测材料的评审不冒充盲测。','3. 每个概念同时覆盖基础计算、换表示、边界/反例、方法重组、综合或逆向任务；不同表现形式必须带来实质解题链差异。题内多方法不重复计数。','4. 确认后的版本才增量入库；重建清单、正式冻结锁与资产绑定，旧数据/证据留档。校准采用未用于规则开发的独立留出，旧开发对不能冒充独立校准。','5. 全量数学/语义/动画资产验收、密度与泄漏验收通过后再考虑正式训练；本轮没有执行训练或生成代码入口放行。', '',
'## 当前门禁与监督', '', '结构屏仍未独立校准；资产仅1/497已验证；生产执行证据缺失，入口CLOSED。16项具名原生边界检查不是全面生产验收。尚未获得有限16项范围开门的明确批准，不代写execution_evidence.json。训练超参仍是提案，示例说明中确认字段不形成阻断的问题须在实际开训前修复。', '',
'旧观察器PID13204已不在，最后心跳03:34:13；已归档旧检查点并恢复隐藏窗口只读观察器，新增训练工具/清单/首批草稿监听，记录空窗且保留既有核心基线。观察器只记录进程与文件变化，不能自行阅读邮件、数学复审或批准放行；本会话处理来信并复验。']
(OUT/'DATA_DIVERSITY_PLAN.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
after={p:sha(ROOT/p) for p in guards};assert before==after
assert not (ROOT/'data/execution_evidence.json').exists()
dump(OUT/'data-unchanged-verification.json',{'guard_files_before':before,'guard_files_after':after,'unchanged':before==after,'candidate_record_count':sum(x['records'] for x in catalog),'every_original_id_once':len(assigned)==len(set(assigned))==63,'active_manifest_references_candidate':any('candidate-recovery' in e['path'] for e in m['entries']),'production_certificate_present':False})
print(json.dumps(totals,ensure_ascii=False));print('guard files unchanged',len(guards))
