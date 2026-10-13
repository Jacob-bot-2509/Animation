from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent
screen=json.loads((OUT/'structural-screen.json').read_text(encoding='utf-8'))
review=json.loads((OUT/'per-question-review.json').read_text(encoding='utf-8'))
rows={r['id']:r for p in (OUT/'staged').glob('*.jsonl') for r in map(json.loads,p.read_text(encoding='utf-8').splitlines())}
reasons={
 'draft-c10-02':'目标是非单调扰动的条件收敛，没有求1/[n(n+2)]的和，也没有裂项及尾项消去；解法只用公共绝对可和比较。分母模式不是同一核心解题任务。',
 'draft-c20-01':'训练方程z=x²-y²含一次z项，是秩退化的图形抛物面；冻结4x²-y²+z²=1是满秩中心型双曲面。负平方项个数不能忽略线性项后当作结构等价。另与冻结test-geom-014共享常见曲面，但本题不构造其全部母线及直线系数算法。',
 'draft-c49-03':'目标是非等权均值的L2充要条件和最大权条件，没有无限裂项级数。n(n+1)来自归一化权而不是固定间隔求和对象。'}
held=[]
for p in screen['candidate_pairs']:
 assert p['train_id'] in reasons
 held.append({'train_id':p['train_id'],'query_id':p['query_id'],'decision':'DISTINCT_CORE_TASK_SHARED_PUBLIC_LEMMA_ALLOWED','reason':reasons[p['train_id']],'query_source':p['query_source'],'score':p['score']})
drafts=[]
for p in screen['draft_and_active_candidates']:
 assert (p['left'],p['right'])==('draft-c40-02','linalg-065')
 drafts.append({'left':p['left'],'right':p['right'],'decision':'DISTINCT_PRIMARY_FACTOR_COUPLING','reason':'草稿有非对角单位1，重复根λ被耦合成唯一初等因子λ²；活动题为对角λ及λ²-1，三个互素不同实根。单位耦合与互素分裂是不同结构条件；不是把同一矩阵参数或根数字换掉。两题共享一般多项式gcd定义。','score':p['score']})
extra={
 'draft-c24-01':'多边形顶点和边方向的正向映射，不包含冻结剪切圆的逆换元方程。',
 'draft-c26-05':'旋转与非等比例伸缩的顺序效应，不求冻结旋转矩阵特征值或任意幂。',
 'draft-c27-01':'相较本次前八批C28秩一行列式题，本题新增零内积非零算子的幂零边界与可对角化分类；目标、条件、结论链不同。',
 'draft-c39-01':'半单两不同根的交换算子，其核像直和；冻结Jordan中心化题是非半单重根，结构不同，未提供其中心化矩阵。',
 'draft-c41-03':'输入是全部特征值同根与核维数序列，冻结逆问题输入最小多项式和迹并含两个根；不复用冻结候选Jordan枚举。',
 'draft-c47-01':'不等中奖率两组独立卷积，有限精确概率与非同分布稀有族极限分开，未用单二项点值的换数值替代。',
 'draft-c50-01':'连续高维立方体容斥与CLT尺度，冻结两个均匀变量的三角形概率未作为子题给出。',
 'draft-c50-02':'离散有界卷积的有限计数与整数阈值，非冻结等权骰子平均的Chebyshev数值替换。',
 'draft-c50-03':'不完整Gamma尾递推，区别于冻结完整积分的Exp矩n!；CLT不宣称有限误差。'}
records=[]
for note in review['records']:
 i=note['id'];r=rows[i]
 records.append({'id':i,'versioned_id':r['versioned_id'],'record_sha256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'manual_reviewed':True,'core_task':r['method'],'review_basis':note['note'],'additional_relation_review':extra.get(i),'decision':'NO_POSITIVE_NUMERIC_ONLY_CLONE_IDENTIFIED_IN_REVIEW','formal_admission':False})
result={'records':records,'heldout_candidate_adjudications':held,'draft_candidate_adjudications':drafts,'resolved_during_revision':[{'id':'draft-c26-03','reason':'平衡二阶谱块可复用冻结完整谱步骤，已改为非正交对合反例。'},{'id':'draft-c27-01','reason':'与活动训练linalg-066同Jordan缺陷结构，已改为一般秩一扰动边界。'},{'id':'draft-c40-01','reason':'同对角gcd计算与C40-04重复，已改为同det不同特殊核及域区别。'},{'id':'draft-c43-03','reason':'旧对偶例的两个基向量暴露冻结正交补，已换成多项式矩配对。'}],'reviewed_heldout_pairs':len(held),'reviewed_draft_pairs':len(drafts),'unresolved_positive_candidates':0,'calibrated':False,'detector_negative_or_UNKNOWN_is_not_certification':True,'policy':'同核心仅换数据按泄漏或重复处理；通用定理共享本身不算泄漏；不得以文字低相似代替结构审阅。','limits':'人工审阅与未校准候选筛查是本次草稿复核，不生成准入证书。所有正式训练证据仍须绑定当前文件哈希。'}
(OUT/'structural-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'records':len(records),'heldout_adjudications':len(held),'draft_adjudications':len(drafts),'unresolved':0}))
