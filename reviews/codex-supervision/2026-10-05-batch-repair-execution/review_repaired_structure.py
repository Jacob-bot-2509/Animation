from pathlib import Path
import json,hashlib,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];PRIOR=ROOT/'reviews/codex-supervision/2026-10-05-strict-batch-audit'
sys.path.insert(0,str(OUT));import build_repaired_batches as B
rows={r['id']:r for p in sorted((OUT/'staged').glob('*.jsonl')) for r in map(json.loads,p.read_text(encoding='utf-8').splitlines())}
reason={
'draft-c11-02':'改为非零展开中心、复递推根、周期零系数与根值上极限；不再含活动训练的交错平方根端点任务。',
'draft-c11-03':'改为稀疏指数的非线性重编号与连续解唯一性；未保留对数生成函数或固定间隔有理裂项子任务。',
'draft-c11-04':'改为两根线性递推与有理生成函数，边界通项独立检查；未含指数级数及y′=y的冻结实例。',
'draft-c11-05':'中心二项式系数产生变量系数微分方程，并需组合下界与条件端点；与对数反射级数、指数初值问题均非只改数值。',
'draft-c51-02':'恢复参数后验任务，加入多次计数似然和后验预测；与给定单次检测率的Bayes代值区别在证据生成与预测任务。',
'draft-c35-02':'四元路径能量差分合同变换、零模和固定端点x4=0的受限正定；不保留冻结二维块精确谱，也不采用冻结的零和超平面/常数向量子空间对。',
'draft-c37-03':'三维对称矩阵空间的坐标与Gram度量共同转换；不包含冻结向量(2,3)的二维基变换，也不含冻结矩阵[[1,2],[3,4]]的范数任务。',
'draft-c33-05':'改为加权三周期矩阵多项式逆和唯一奇异参数的全部相容解；核为span(6,3,1)、像条件b1+2b2+6b3=0，避开冻结固定零和/常数向量子空间对，也不再是同批三角矩阵的数值/符号系数变体。',
'draft-c13-01':'反正切差的恒等式须检验主值分支，并给精确反正切尾项；冻结题是一阶有理部分分式、间隔二的两个尾项，不是同一序列数字替换。',
'draft-c13-04':'平方根二阶差分须利用一阶差分递减判定绝对收敛，尾项符号为负；不是重编号后的1/[n(n+2)]序列。',
'draft-c18-01':'未知平面的归一化法向满足两点距离约束，需穷尽离散和平面族两分支；冻结题给定平面，只求单点距离/投影。公共距离定理不等于相同完整任务。',
'draft-c18-04':'度量改为正定W，投影移动方向W^{-1}n，需加权平方分解证明全局唯一；不是欧氏法向投影数值更换，也不再求同批两平面距离。',
'draft-c30-01':'未知多项式由两个节点重数、次数和归一化确定；有限平移展开是最后验证，核心重建条件不是冻结给定三次多项式的展开。',
'draft-c30-02':'求未知反射中心，须必要条件与所有奇次项的充分性核对；冻结中心已给定且只求有限系数。',
'draft-c30-03':'算子是有限平移差分，任务含精确降阶、幂零指数及规范化逆问题；不是冻结P2导数算子矩阵。',
'draft-c30-05':'对全部次数证明无非零周期与中心差分恒等式分类；不含对数无穷级数，符合有限多项式考点。',
'draft-c21-04':'曲面xy=1使首项能退化，必须新增常数/一次分支及重根切平面证明；固定正定球面与非零方向不存在这种首项退化。',
'draft-c28-01':'凹多边形有向扇分解有负项，并用凹口几何核对；不是三个三维向量行列式乘固定体积系数。',
'draft-c28-02':'秩一参数体积与取向、奇异投影核像一起证明；不含冻结二阶矩阵精确行列式子任务。',
'draft-c28-04':'R4的4x3坐标矩阵需Gram度量或薄QR，三维体积由正交高度核对；不能套R3混合积，未保留冻结共面题的数值张成空间。',
'draft-c46-01':'事件为乘积双曲线且被样本空间截断，面积有精确对数；不是冻结和变量的三角形面积，也不是同批差带换宽度。',
'draft-c46-03':'三点最近距离产生三个Voronoi区域，需比较三条平分线和零测平局；不属于仅差带事件互补。',
'draft-c46-04':'二维非均匀密度反例检验均匀面积假设，结果由密度加权；未保留冻结sqrt(U)变换密度子任务。',
'draft-c46-05':'三周期小数部分映射的原像面积与乘积联合分布证明；未保留Buffon条件和2l/(pi d)答案，也不含原始X+Y和变量密度链。',
'draft-c02-01':'振荡平方相位换元、分部尾界和绝对值分块下界；不是正项p积分的固定参数值，亦不计算冻结零点局部积分极限。',
'draft-c02-02':'构造无界可积尖峰，局部黎曼可积、面积几何和及两子列证明；不再含冻结p积分数值实例。',
'draft-c02-04':'两参数零端抵消、Tonelli交换和对数比；不再有冻结xe^{-x}积分的分部边界链。',
'draft-c02-05':'两个奇异端点相反约束，由二进几何块证明并计算特殊换元值；未逐项给出冻结全参数p积分原函数及其完整值链。',
'draft-c04-05':'带两孔区域、两奇点不同环流、内外边界方向共同进入Green；不是冻结椭圆面积或光滑实心区域积分。',
'draft-c07-02':'负极径产生内外两环，须换实际方向并证明嵌套，以并集面积纠正全周期重复覆盖；不是无内环心形线仅改系数。',
'draft-c08-01':'摆线开拱通过轴闭合，横坐标单调且有方向检查；不是闭合椭圆的一圈参数面积。',
'draft-c09-01':'区域穿轴，旋转像两圆盘嵌套并集决定半径；不是冻结抛物线绕纵轴所得同一实体。',
'draft-c09-02':'外部轴产生环面，圆环截面和非相交轴质心定理独立核对；不是旧直线柱壳题改外轴偏移。',
'draft-c09-04':'移动轴经过区域，内外两种拓扑和唯一全局最优需要完整分段；与固定轴体积任务不同。',
'draft-c09-05':'两个平面分量的旋转像重叠，三段径向并集及容斥为核心；没有冻结正弦区域绕纵轴的壳层积分子任务。'
}
assert set(reason)==set(B.NEW)
old=json.loads((PRIOR/'candidate-semantic-review.json').read_text(encoding='utf-8'));oldpairs={(p['train_id'],p['query_id']):p for p in old['pairs']}
screen=json.loads((OUT/'structural-screen-repaired.json').read_text(encoding='utf-8'));pairs=[]
for p in screen['candidate_pairs']:
 key=p['train_id'],p['query_id']
 if p['train_id'] in B.NEW:judge='REVISED_TASK_HAS_ESSENTIAL_NEW_CONSTRAINTS';why=reason[p['train_id']]
 else:
  assert key in oldpairs,key
  judge=oldpairs[key]['judgment'];why=oldpairs[key]['reason']
 pairs.append({**p,'judgment':judge,'reason':why,'admitted':False,'review_basis':'NEW_PROBLEM_AND_PROOF' if p['train_id'] in B.NEW else 'PRIOR_PAIR_REVIEW_MATH_CONTENT_UNCHANGED'})
relations=[]
for p in json.loads((PRIOR/'cross-split-method-review-v2.json').read_text(encoding='utf-8'))['known_relations']:
 i=p['train_id'];relations.append({'train_id':i,'query_id':p['query_id'],'original_relation':p['judgment'],'new_reason':reason[i] if i in reason else '既有严格副本已去除源稿的附加混合积数值链；本版数学内容仅规范公式转义，既有复核结论继续按原范围适用。','new_math_sha256':hashlib.sha256(json.dumps({f:rows[i][f] for f in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'historical_risk_evidence_preserved':True,'formal_version_bound_admission':'PENDING'})
local=[]
for p in screen['draft_and_active_candidates']:
 ids={p['left'],p['right']}
 if ids=={'draft-c13-02','draft-c13-03'}:why='一题是三个连续线性因子的部分分式消去两个尾项，另一题是阶乘倒数一阶递推消去单尾项；不能由常数换值或重编号互相得到。共享有限和抵消定理不单独认定为数值克隆。'
 elif ids=={'draft-c03-01','draft-c03-05'}:why='前者是矩形可分离乘积直接积分；后者指定非分离线性坐标替换、菱形变换域及Jacobian。积分对象与域变换任务不是数值更换。'
 else:raise AssertionError(p)
 local.append({**p,'judgment':'ESSENTIAL_TASK_DIFFERENCE','reason':why,'admitted':False})
result={'revised_questions':[{'id':i,'reason':reason[i],'math_sha256':hashlib.sha256(json.dumps({f:rows[i][f] for f in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()} for i in B.NEW],'candidate_pairs':pairs,'known_relations_rechecked':relations,'remaining_draft_and_active_candidates_reviewed':local,'all_250_unique_heldout_problem_statements_read':True,'450_method_records_screened':True,'generic_theorem_sharing_alone_not_leakage':True,'all_detector_candidates_have_pair_specific_review':True,'UNKNOWN_is_not_no_leakage':True,'claim_scope':'KNOWN_FOUND_OVERLAPS_AND_CURRENT_CANDIDATE_PAIRS; NOT_PRODUCTION_CERTIFICATE','training_gate_released':False,'frozen_eval_test_unchanged':True}
(OUT/'structure-repair-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'revised':len(reason),'candidate_pairs_reviewed':len(pairs),'known_relations_rechecked':len(relations),'local_candidates_reviewed':len(local)},ensure_ascii=False))
