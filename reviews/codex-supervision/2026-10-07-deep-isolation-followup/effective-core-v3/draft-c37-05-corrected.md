# draft-c37-05 精确修订候选

设 $V$ 是非零有限维实线性空间。证明不存在 $S,T\in\operatorname{End}(V)$ 使 $ST-TS=I_V$。再在无限维实多项式空间 $\mathbb R[x]$ 上给出满足该恒等式的两个线性算子，说明有限维假设的必要性。

## 证明与过程

记 $n=\dim V\ge1$。任选一组基，把 $S,T$ 写成矩阵 $(s_{ij}),(t_{ij})$。有限求和可交换顺序，故 $\operatorname{tr}(ST)=\sum_{i,j}s_{ij}t_{ji}=\sum_{i,j}t_{ij}s_{ji}=\operatorname{tr}(TS)$。若 $ST-TS=I_V$，取迹得到 $0=\operatorname{tr}(ST-TS)=\operatorname{tr}I_V=n$，与 $n\ge1$ 且实数域矛盾。无限维情形取 $D(p)=p'$、$M(p)=xp$。二者均为 $\mathbb R[x]$ 上的线性算子，乘积求导恒等式给出 $(DM-MD)(p)=(xp)'-xp'=p$，即 $DM-MD=I$。这里不能使用有限矩阵的迹论证；$\mathbb R[x]$ 为无限维，因而不与前述结论矛盾。

## 答案

非零有限维实空间上不存在这样的 $S,T$；在 $\mathbb R[x]$ 上 $D(p)=p'$、$M(p)=xp$ 满足 $DM-MD=I$。

## 场景文字

逐项展示有限矩阵乘积的迹相等。

假设交换子为单位算子，取迹得到矛盾。

在实多项式空间展示导数与乘法算子。

利用乘积求导规则验证 $(DM-MD)(p)=p$，说明维数假设。
