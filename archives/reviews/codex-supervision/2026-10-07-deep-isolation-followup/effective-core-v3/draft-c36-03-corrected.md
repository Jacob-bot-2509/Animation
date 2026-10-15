# draft-c36-03 精确修订候选

设 $A=\operatorname{diag}(1,-1,0)$、$C=\begin{pmatrix}1&1&0\\0&2&0\\0&0&3\end{pmatrix}$、$B=C^{\mathsf T}AC$。计算 $B$，求其秩与惯性三元组 $(n_+,n_-,n_0)$；证明 $A$ 与 $B$ 合同但不相似，并用可逆变量替换说明合同为何保持惯性。

## 证明与过程

$\det C=6\ne0$，直接相乘得 $B=\begin{pmatrix}1&1&0\\1&-3&0\\0&0&0\end{pmatrix}$，所以合同关系成立。对任意 $v$，$v^{\mathsf T}Bv=(Cv)^{\mathsf T}A(Cv)$；映射 $v\mapsto Cv$ 为双射，正定子空间、负定子空间分别被一一对应且保持维数，因此最大正、负子空间维数不变。又可逆矩阵左右乘不改变秩，故 $\operatorname{rank}B=\operatorname{rank}A=2$，零惯性指数为 $3-2=1$。$A$ 的惯性三元组为 $(1,1,1)$，$B$ 亦然。若存在可逆 $S$ 使 $B=S^{-1}AS$，利用 $\operatorname{tr}(UV)=\operatorname{tr}(VU)$ 就有 $\operatorname{tr}B=\operatorname{tr}A$；但本例 $\operatorname{tr}A=0$、$\operatorname{tr}B=-2$，矛盾。因此二者不相似。合同保持惯性与秩，却不必保持特征值或迹。

## 答案

$B=\begin{pmatrix}1&1&0\\1&-3&0\\0&0&0\end{pmatrix}$，$\operatorname{rank}B=2$、$(n_+,n_-,n_0)=(1,1,1)$；$A,B$ 合同而不相似（迹分别为 $0,-2$）。

## 场景文字

展示矩阵相乘得到 $B$，验证 $\det C\ne0$。

用双射运输正、负子空间，说明惯性保持。

由可逆左右乘得到秩和零惯性指数。

用相似的迹不变性与本例不同迹得出反证。
