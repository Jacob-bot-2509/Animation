# batch-15 精确数学修订文档

版本：codex-repair-v4-final。15题；原编号、题数和顺序全部保留，删除0题。题目、推导、答案及场景文本已复验。未正式准入，动画尚未渲染验收。

前身v3 SHA-256：`9aa72cf2aedb69a797b1df5a9abe5b5f14ccc447e9460725bccc1b8f815d0bbb`。

## draft-c40-01 · C40

**题目**

令$f=\lambda-1$，$A(\lambda)=\operatorname{diag}(f,f^2)$、$B(\lambda)=\operatorname{diag}(1,f^3)$。两矩阵行列式相同，判断是否多项式可逆等价；比较在有理函数域与代入实参数后的秩、核，说明行列式为何不足。

**推导**

两者行列式都为$f^3$，但一阶子式首一gcd分别为$f$与$1$，不变因子分别$f,f^2$与$1,f^3$，所以不unimodular等价。在有理函数域$\mathbb R(\lambda)$，$f$是可逆非零元素，两矩阵秩都为$2$、核都为零；在多项式环中核也都为零，因为环无零因子。在实数$a\ne1$代入时两者仍秩$2$、核零。代入$a=1$，$A(1)=0$，秩$0$、核$\mathbb R^2$；$B(1)=\operatorname{diag}(1,0)$，秩$1$、核$\operatorname{span}(e_2)$。同一行列式零点及其阶数不能确定特殊参数的核维数，通用域的核也不能直接代入当作特殊核。

**答案**

不等价；一般域及$a\ne1$均秩$2$，$a=1$时秩分别$0,1$；行列式相同不足以确定特殊核。

**场景对象**

- 令$f=\lambda-1$，$A(\lambda)=\operatorname{diag}(f,f^2)$、$B(\lambda)=\operatorname{diag}(1,f^3)$。两矩阵行列式相同，判断是否多项式可逆等价；比较在有理函数域与代入实参数后的秩、核，说明行列式为何不足。
- 不等价；一般域及$a\ne1$均秩$2$，$a=1$时秩分别$0,1$；行列式相同不足以确定特殊核。

**场景步骤**

- 第一步:两者行列式都为$f^3$，但一阶子式首一gcd分别为$f$与$1$，不变因子分别$f,f^2$与$1,f^3$，所以不unimodular等价。
- 第二步:在有理函数域$\mathbb R(\lambda)$，$f$是可逆非零元素，两矩阵秩都为$2$、核都为零；在多项式环中核也都为零，因为环无零因子。
- 第三步:在实数$a\ne1$代入时两者仍秩$2$、核零。
- 第四步:代入$a=1$，$A(1)=0$，秩$0$、核$\mathbb R^2$；$B(1)=\operatorname{diag}(1,0)$，秩$1$、核$\operatorname{span}(e_2)$。
- 第五步:同一行列式零点及其阶数不能确定特殊参数的核维数，通用域的核也不能直接代入当作特殊核。

## draft-c40-02 · C40

**题目**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda&1\\0&\lambda\end{pmatrix}$ 的行列式因子、不变因子与初等因子。

**推导**

$A(\lambda)$ 的全部一阶子式为 $\lambda,1,0,\lambda$,其最大公因式 $D_1(\lambda)=1$。二阶行列式因子 $D_2(\lambda)=\det A(\lambda)=\lambda^2$。不变因子:$d_1=D_1=1$,$d_2=\frac{D_2}{D_1}=\lambda^2$。初等因子:$\lambda^2$(由 $d_2$ 给出)。

**答案**

$D_1=1$,$D_2=\lambda^2$;不变因子 $d_1=1$,$d_2=\lambda^2$;初等因子 $\lambda^2$。

**场景对象**

- 求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda&1\\0&\lambda\end{pmatrix}$ 的行列式因子、不变因子与初等因子。
- $D_1=1$,$D_2=\lambda^2$;不变因子 $d_1=1$,$d_2=\lambda^2$;初等因子 $\lambda^2$。

**场景步骤**

- 第一步:$A(\lambda)$ 的全部一阶子式为 $\lambda,1,0,\lambda$,其最大公因式 $D_1(\lambda)=1$。
- 第二步:二阶行列式因子 $D_2(\lambda)=\det A(\lambda)=\lambda^2$。
- 第三步:不变因子:$d_1=D_1=1$,$d_2=\frac{D_2}{D_1}=\lambda^2$。
- 第四步:初等因子:$\lambda^2$(由 $d_2$ 给出)。

## draft-c40-03 · C40

**题目**

分别求 $A(\lambda)=\mathrm{diag}(\lambda,\lambda-1)$ 与 $B(\lambda)=\mathrm{diag}(\lambda,\lambda)$ 的不变因子与初等因子，并说明两者结构差异的原因。

**推导**

$A(\lambda)$:$D_1=\gcd(\lambda,\lambda-1)=1$,$D_2=\lambda(\lambda-1)$;不变因子 $d_1=1$,$d_2=\lambda(\lambda-1)$;初等因子 $\lambda$ 与 $\lambda-1$(均由 $d_2$ 分解得到)。$B(\lambda)$:$D_1=\lambda$,$D_2=\lambda^2$;不变因子 $d_1=\lambda$,$d_2=\lambda$;初等因子 $\lambda$ 与 $\lambda$($\lambda$ 出现两次)。差异原因:不变因子满足整除链 $d_1\mid d_2$。$A$ 的两个对角元互素,公因子为 $1$,$d_2$ 必须吞下全部两个因子;而 $B$ 的两个对角元有公因子 $\lambda$,可分摊到 $d_1$ 与 $d_2$。

**答案**

$A$:不变因子 $1,\lambda(\lambda-1)$,初等因子 $\lambda,\lambda-1$;$B$:不变因子 $\lambda,\lambda$,初等因子 $\lambda,\lambda$。差异源于互素与否影响整除链分配。

**场景对象**

- 分别求 $A(\lambda)=\mathrm{diag}(\lambda,\lambda-1)$ 与 $B(\lambda)=\mathrm{diag}(\lambda,\lambda)$ 的不变因子与初等因子，并说明两者结构差异的原因。
- $A$:不变因子 $1,\lambda(\lambda-1)$,初等因子 $\lambda,\lambda-1$;$B$:不变因子 $\lambda,\lambda$,初等因子 $\lambda,\lambda$。差异源于互素与否影响整除链分配。

**场景步骤**

- 第一步:$A(\lambda)$:$D_1=\gcd(\lambda,\lambda-1)=1$,$D_2=\lambda(\lambda-1)$;不变因子 $d_1=1$,$d_2=\lambda(\lambda-1)$;初等因子 $\lambda$ 与 $\lambda-1$(均由 $d_2$ 分解得到)。
- 第二步:$B(\lambda)$:$D_1=\lambda$,$D_2=\lambda^2$;不变因子 $d_1=\lambda$,$d_2=\lambda$;初等因子 $\lambda$ 与 $\lambda$($\lambda$ 出现两次)。
- 第三步:差异原因:不变因子满足整除链 $d_1\mid d_2$。
- 第四步:$A$ 的两个对角元互素,公因子为 $1$,$d_2$ 必须吞下全部两个因子;而 $B$ 的两个对角元有公因子 $\lambda$,可分摊到 $d_1$ 与 $d_2$。

## draft-c40-04 · C40

**题目**

求 λ-矩阵 $A(\lambda)=\mathrm{diag}(\lambda+1,\,\lambda(\lambda+1),\,(\lambda+1)^2(\lambda-2))$ 的行列式因子、不变因子与初等因子。

**推导**

一阶行列式因子:$D_1=\gcd(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))=\lambda+1$。二阶行列式因子:各二阶子式(对角情形即两两乘积)为 $\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$,最大公因式 $D_2=(\lambda+1)^2$。$D_3=\det=\lambda(\lambda+1)^4(\lambda-2)$。不变因子:$d_1=D_1=\lambda+1$;$d_2=\frac{D_2}{D_1}=\lambda+1$;$d_3=\frac{D_3}{D_2}=\lambda(\lambda+1)^2(\lambda-2)$。初等因子:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$。

**答案**

$D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$;不变因子 $\lambda+1,\lambda+1,\lambda(\lambda+1)^2(\lambda-2)$;初等因子 $\lambda+1,\lambda+1,\lambda,(\lambda+1)^2,\lambda-2$。

**场景对象**

- 求 λ-矩阵 $A(\lambda)=\mathrm{diag}(\lambda+1,\,\lambda(\lambda+1),\,(\lambda+1)^2(\lambda-2))$ 的行列式因子、不变因子与初等因子。
- $D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$;不变因子 $\lambda+1,\lambda+1,\lambda(\lambda+1)^2(\lambda-2)$;初等因子 $\lambda+1,\lambda+1,\lambda,(\lambda+1)^2,\lambda-2$。

**场景步骤**

- 第一步:一阶行列式因子:$D_1=\gcd(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))=\lambda+1$。
- 第二步:二阶行列式因子:各二阶子式(对角情形即两两乘积)为 $\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$,最大公因式 $D_2=(\lambda+1)^2$。
- 第三步:$D_3=\det=\lambda(\lambda+1)^4(\lambda-2)$。
- 第四步:不变因子:$d_1=D_1=\lambda+1$;$d_2=\frac{D_2}{D_1}=\lambda+1$;$d_3=\frac{D_3}{D_2}=\lambda(\lambda+1)^2(\lambda-2)$。
- 第五步:初等因子:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$。

## draft-c40-05 · C40

**题目**

在$\mathbb R[\lambda]$中，证明多项式矩阵的各阶首一行列式因子在左右乘可逆多项式矩阵时不变。说明允许的行缩放是什么，并以一个非可逆多项式行缩放说明限制必要。

**推导**

环中的单位是非零实常数。可逆多项式矩阵的行列式是单位，逆仍为多项式矩阵。由Cauchy–Binet公式，$UA$的每个$k$阶子式是$A$的$k$阶子式的多项式线性组合，所以旧子式的首一最大公因子整除新子式的首一最大公因子；再乘$U^{-1}$得反向整除，因此两者相同。右乘同理，恒为零的子式族也保持。初等行缩放只能乘非零常数，行倍加可乘任意多项式。反例$A=\operatorname{diag}(\lambda,\lambda+1)$，将第一行乘$\lambda$得$B=\operatorname{diag}(\lambda^2,\lambda+1)$；二阶因子由$\lambda(\lambda+1)$变为$\lambda^2(\lambda+1)$，不保持，因为缩放矩阵行列式$\lambda$不是单位。

**答案**

左右unimodular等价保持全部首一行列式因子；行缩放限非零常数，非单位缩放可改变因子。

**场景对象**

- 在$\mathbb R[\lambda]$中，证明多项式矩阵的各阶首一行列式因子在左右乘可逆多项式矩阵时不变。说明允许的行缩放是什么，并以一个非可逆多项式行缩放说明限制必要。
- 左右unimodular等价保持全部首一行列式因子；行缩放限非零常数，非单位缩放可改变因子。

**场景步骤**

- 第一步:环中的单位是非零实常数。
- 第二步:可逆多项式矩阵的行列式是单位，逆仍为多项式矩阵。
- 第三步:由Cauchy–Binet公式，$UA$的每个$k$阶子式是$A$的$k$阶子式的多项式线性组合，所以旧子式的首一最大公因子整除新子式的首一最大公因子；再乘$U^{-1}$得反向整除，因此两者相同。
- 第四步:右乘同理，恒为零的子式族也保持。
- 第五步:初等行缩放只能乘非零常数，行倍加可乘任意多项式。
- 第六步:反例$A=\operatorname{diag}(\lambda,\lambda+1)$，将第一行乘$\lambda$得$B=\operatorname{diag}(\lambda^2,\lambda+1)$；二阶因子由$\lambda(\lambda+1)$变为$\lambda^2(\lambda+1)$，不保持，因为缩放矩阵行列式$\lambda$不是单位。

## draft-c41-01 · C41

**题目**

在基$e_{11},e_{12},e_{21},e_{22}$中，令$N=J_2(0)\otimes I_2+I_2\otimes J_2(0)$。从张量结构求Jordan形式，并给出实际Jordan链及换基矩阵。

**推导**

$Ne_{11}=0,Ne_{12}=Ne_{21}=e_{11},Ne_{22}=e_{12}+e_{21}$。所以$N^2e_{22}=2e_{11}$，$N^3=0$；秩序列$4,2,1,0$。取链$v_3=e_{22},v_2=e_{12}+e_{21},v_1=2e_{11}$及$w=e_{12}-e_{21}$，有$Nv_3=v_2,Nv_2=v_1,Nv_1=Nw=0$。$P=(v_1,v_2,v_3,w)=\begin{pmatrix}2&0&0&0\\0&1&0&1\\0&1&0&-1\\0&0&1&0\end{pmatrix}$可逆，$NP=P[J_3(0)\oplus J_1(0)]$。因此Jordan形式为$J_3(0)\oplus J_1(0)$。

**答案**

$J_3(0)\oplus J_1(0)$；链和$P$如上。

**场景对象**

- 在基$e_{11},e_{12},e_{21},e_{22}$中，令$N=J_2(0)\otimes I_2+I_2\otimes J_2(0)$。从张量结构求Jordan形式，并给出实际Jordan链及换基矩阵。
- $J_3(0)\oplus J_1(0)$；链和$P$如上。

**场景步骤**

- 第一步:$Ne_{11}=0,Ne_{12}=Ne_{21}=e_{11},Ne_{22}=e_{12}+e_{21}$。
- 第二步:所以$N^2e_{22}=2e_{11}$，$N^3=0$；秩序列$4,2,1,0$。
- 第三步:取链$v_3=e_{22},v_2=e_{12}+e_{21},v_1=2e_{11}$及$w=e_{12}-e_{21}$，有$Nv_3=v_2,Nv_2=v_1,Nv_1=Nw=0$。
- 第四步:$P=(v_1,v_2,v_3,w)=\begin{pmatrix}2&0&0&0\\0&1&0&1\\0&1&0&-1\\0&0&1&0\end{pmatrix}$可逆，$NP=P[J_3(0)\oplus J_1(0)]$。
- 第五步:因此Jordan形式为$J_3(0)\oplus J_1(0)$。

## draft-c41-02 · C41

**题目**

设$B=\begin{pmatrix}1&-2\\2&1\end{pmatrix}$、$A=\begin{pmatrix}B&I_2\\0&B\end{pmatrix}$。求复域Jordan形式和实最小多项式，说明实域是否可以写成实对角阵。

**推导**

$B$有不同复根$\lambda_\pm=1\pm2i$，特征向量$q_+=(1,-i)^{\mathsf T},q_-=(1,i)^{\mathsf T}$。对各根令$v_\pm=(q_\pm,0)$、$w_\pm=(0,q_\pm)$，则$(A-\lambda_\pm I)w_\pm=v_\pm$、$(A-\lambda_\pm I)v_\pm=0$。因$q_+,q_-$独立，四向量组成复基，所以Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$。两个二阶块使复最小多项式为$(\lambda-1-2i)^2(\lambda-1+2i)^2=[(\lambda-1)^2+4]^2$，它也是实最小多项式。非实特征值且存在二阶块，不能写成实对角阵，也不能在复域对角化。

**答案**

复Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$；实最小多项式$[(\lambda-1)^2+4]^2$；不可对角化。

**场景对象**

- 设$B=\begin{pmatrix}1&-2\\2&1\end{pmatrix}$、$A=\begin{pmatrix}B&I_2\\0&B\end{pmatrix}$。求复域Jordan形式和实最小多项式，说明实域是否可以写成实对角阵。
- 复Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$；实最小多项式$[(\lambda-1)^2+4]^2$；不可对角化。

**场景步骤**

- 第一步:$B$有不同复根$\lambda_\pm=1\pm2i$，特征向量$q_+=(1,-i)^{\mathsf T},q_-=(1,i)^{\mathsf T}$。
- 第二步:对各根令$v_\pm=(q_\pm,0)$、$w_\pm=(0,q_\pm)$，则$(A-\lambda_\pm I)w_\pm=v_\pm$、$(A-\lambda_\pm I)v_\pm=0$。
- 第三步:因$q_+,q_-$独立，四向量组成复基，所以Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$。
- 第四步:两个二阶块使复最小多项式为$(\lambda-1-2i)^2(\lambda-1+2i)^2=[(\lambda-1)^2+4]^2$，它也是实最小多项式。
- 第五步:非实特征值且存在二阶块，不能写成实对角阵，也不能在复域对角化。

## draft-c41-03 · C41

**题目**

设四阶矩阵 $A$ 的特征值全为 $2$，且 $\dim\ker(A-2I)=2$，$\dim\ker(A-2I)^2=3$，$\dim\ker(A-2I)^3=4$。求 $A$ 的若尔当标准形。

**推导**

若尔当块数 $=$ 特征子空间维数 $=\dim\ker(A-2I)=2$。各阶块数由核维数差给出:大小至少为 $2$ 的块数 $=\dim\ker(A-2I)^2-\dim\ker(A-2I)=3-2=1$;大小至少为 $3$ 的块数 $=\dim\ker(A-2I)^3-\dim\ker(A-2I)^2=4-3=1$。故块为:一个三阶块与一个一阶块($3+1=4$)。若尔当标准形为 $J_3(2)\oplus J_1(2)=\begin{pmatrix}2&1&0&0\\0&2&1&0\\0&0&2&0\\0&0&0&2\end{pmatrix}$。

**答案**

$J=J_3(2)\oplus J_1(2)$,即一个三阶块与一个一阶块。

**场景对象**

- 设四阶矩阵 $A$ 的特征值全为 $2$，且 $\dim\ker(A-2I)=2$，$\dim\ker(A-2I)^2=3$，$\dim\ker(A-2I)^3=4$。求 $A$ 的若尔当标准形。
- $J=J_3(2)\oplus J_1(2)$,即一个三阶块与一个一阶块。

**场景步骤**

- 第一步:若尔当块数 $=$ 特征子空间维数 $=\dim\ker(A-2I)=2$。
- 第二步:各阶块数由核维数差给出:大小至少为 $2$ 的块数 $=\dim\ker(A-2I)^2-\dim\ker(A-2I)=3-2=1$;大小至少为 $3$ 的块数 $=\dim\ker(A-2I)^3-\dim\ker(A-2I)^2=4-3=1$。
- 第三步:故块为:一个三阶块与一个一阶块($3+1=4$)。
- 第四步:若尔当标准形为 $J_3(2)\oplus J_1(2)=\begin{pmatrix}2&1&0&0\\0&2&1&0\\0&0&2&0\\0&0&0&2\end{pmatrix}$。

## draft-c41-04 · C41

**题目**

对$A=\begin{pmatrix}4&2&1\\0&4&3\\0&0&4\end{pmatrix}$，构造实际广义特征向量链和$P$，验证$P^{-1}AP$，而非直接读出现成Jordan块。

**推导**

令$N=A-4I$，取$v_3=e_3$，$v_2=Nv_3=(1,3,0)^{\mathsf T}$，$v_1=Nv_2=(6,0,0)^{\mathsf T}$，则$Nv_1=0$。$P=(v_1,v_2,v_3)=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，行列式$18\ne0$。链给$AP=P\begin{pmatrix}4&1&0\\0&4&1\\0&0&4\end{pmatrix}$，所以Jordan形式为$J_3(4)$，最小多项式$(\lambda-4)^3$；$N^2\ne0,N^3=0$确保不能误分成较短链。

**答案**

$P=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，$P^{-1}AP=J_3(4)$。

**场景对象**

- 对$A=\begin{pmatrix}4&2&1\\0&4&3\\0&0&4\end{pmatrix}$，构造实际广义特征向量链和$P$，验证$P^{-1}AP$，而非直接读出现成Jordan块。
- $P=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，$P^{-1}AP=J_3(4)$。

**场景步骤**

- 第一步:令$N=A-4I$，取$v_3=e_3$，$v_2=Nv_3=(1,3,0)^{\mathsf T}$，$v_1=Nv_2=(6,0,0)^{\mathsf T}$，则$Nv_1=0$。
- 第二步:$P=(v_1,v_2,v_3)=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，行列式$18\ne0$。
- 第三步:链给$AP=P\begin{pmatrix}4&1&0\\0&4&1\\0&0&4\end{pmatrix}$，所以Jordan形式为$J_3(4)$，最小多项式$(\lambda-4)^3$；$N^2\ne0,N^3=0$确保不能误分成较短链。

## draft-c41-05 · C41

**题目**

证明:若尔当块 $J_m(\lambda)$ 的幂零部分 $N=J_m(0)$ 满足 $\dim\ker N^k=\min(k,m)$；并说明这一公式如何由核维数序列唯一确定若尔当块的个数与大小。

**推导**

$N=J_m(0)$ 是把基向量向前推一位的位移算子:$Ne_1=0$,$Ne_i=e_{i-1}$($i\ge2$)。于是 $N^k$ 把 $e_i$ 映为 $e_{i-k}$($i>k$)或 $0$($i\le k$),即 $N^k$ 的像由 $e_1,\dots,e_{m-k}$ 张成(当 $k<m$),秩为 $m-k$;当 $k\ge m$ 时 $N^k=0$,秩为 $0$。由秩-零度,$\dim\ker N^k=m-(m-k)=k$($k<m$),$\dim\ker N^k=m$($k\ge m$),即 $\min(k,m)$。块结构:对一般矩阵,设 $r_k=\dim\ker(A-\lambda I)^k$,则大小至少为 $k$ 的 $\lambda$ 块数为 $r_k-r_{k-1}$(每个 $m$ 阶块对 $r_k$ 贡献 $\min(k,m)$,相邻差即 $\min(k,m)-\min(k-1,m)$,恰好是大小为 $\ge k$ 的块数贡献的 $1$)。故核维数序列 $r_0=0,r_1,r_2,\dots$ 的差分解唯一确定各阶块数。

**答案**

证明见解法(位移算子的核维数 $\min(k,m)$;块数 $=r_k-r_{k-1}$ 的差分解唯一确定块结构)。

**场景对象**

- 证明:若尔当块 $J_m(\lambda)$ 的幂零部分 $N=J_m(0)$ 满足 $\dim\ker N^k=\min(k,m)$；并说明这一公式如何由核维数序列唯一确定若尔当块的个数与大小。
- 证明见解法(位移算子的核维数 $\min(k,m)$;块数 $=r_k-r_{k-1}$ 的差分解唯一确定块结构)。

**场景步骤**

- 第一步:$N=J_m(0)$ 是把基向量向前推一位的位移算子:$Ne_1=0$,$Ne_i=e_{i-1}$($i\ge2$)。
- 第二步:于是 $N^k$ 把 $e_i$ 映为 $e_{i-k}$($i>k$)或 $0$($i\le k$),即 $N^k$ 的像由 $e_1,\dots,e_{m-k}$ 张成(当 $k<m$),秩为 $m-k$;当 $k\ge m$ 时 $N^k=0$,秩为 $0$。
- 第三步:由秩-零度,$\dim\ker N^k=m-(m-k)=k$($k<m$),$\dim\ker N^k=m$($k\ge m$),即 $\min(k,m)$。
- 第四步:块结构:对一般矩阵,设 $r_k=\dim\ker(A-\lambda I)^k$,则大小至少为 $k$ 的 $\lambda$ 块数为 $r_k-r_{k-1}$(每个 $m$ 阶块对 $r_k$ 贡献 $\min(k,m)$,相邻差即 $\min(k,m)-\min(k-1,m)$,恰好是大小为 $\ge k$ 的块数贡献的 $1$)。
- 第五步:故核维数序列 $r_0=0,r_1,r_2,\dots$ 的差分解唯一确定各阶块数。

## draft-c42-01 · C42

**题目**

设$u\in\mathbb R^m$为单位向量，$m\ge1$。证明$H=I-2uu^{\mathsf T}$是正交矩阵，求几何意义、行列式与特征空间。

**推导**

$H^{\mathsf T}=H$，且$H^2=I-4uu^{\mathsf T}+4u(u^{\mathsf T}u)u^{\mathsf T}=I$。$Hu=-u$；若$v\perp u$，$Hv=v$。由直和$\mathbb R^m=\operatorname{span}(u)\oplus u^{\perp}$，这是关于超平面$u^{\perp}$的反射；特征值$-1$空间为$\operatorname{span}(u)$，特征值$1$空间为$u^{\perp}$，维数分别$1,m-1$，行列式$-1$。

**答案**

$H$为超平面反射，$\det H=-1$；两特征空间$\operatorname{span}(u)$与$u^{\perp}$。

**场景对象**

- 设$u\in\mathbb R^m$为单位向量，$m\ge1$。证明$H=I-2uu^{\mathsf T}$是正交矩阵，求几何意义、行列式与特征空间。
- $H$为超平面反射，$\det H=-1$；两特征空间$\operatorname{span}(u)$与$u^{\perp}$。

**场景步骤**

- 第一步:$H^{\mathsf T}=H$，且$H^2=I-4uu^{\mathsf T}+4u(u^{\mathsf T}u)u^{\mathsf T}=I$。
- 第二步:$Hu=-u$；若$v\perp u$，$Hv=v$。
- 第三步:由直和$\mathbb R^m=\operatorname{span}(u)\oplus u^{\perp}$，这是关于超平面$u^{\perp}$的反射；特征值$-1$空间为$\operatorname{span}(u)$，特征值$1$空间为$u^{\perp}$，维数分别$1,m-1$，行列式$-1$。

## draft-c42-02 · C42

**题目**

令$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$。求两个乘积并说明三维不同轴旋转为何不交换，给两乘积的轴与精确角。

**推导**

$R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$，$R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$，不同。两者均正交、行列式$1$、迹$0$，由$\operatorname{tr}R=1+2\cos\theta$得$\theta=2\pi/3$。固定向量分别为$(1,1,1)$、$(1,1,-1)$；反对称部分的轴向量分别正比于这两个向量，因$\sin(2\pi/3)>0$，取对应单位向量即给右手角$2\pi/3$。不同轴使作用顺序改变结果，不能把平面旋转角相加律直接用于三维。

**答案**

两个乘积不同，轴分别$(1,1,1)/\sqrt3$与$(1,1,-1)/\sqrt3$，右手角均$2\pi/3$。

**场景对象**

- 令$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$。求两个乘积并说明三维不同轴旋转为何不交换，给两乘积的轴与精确角。
- 两个乘积不同，轴分别$(1,1,1)/\sqrt3$与$(1,1,-1)/\sqrt3$，右手角均$2\pi/3$。

**场景步骤**

- 第一步:$R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$，$R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$，不同。
- 第二步:两者均正交、行列式$1$、迹$0$，由$\operatorname{tr}R=1+2\cos\theta$得$\theta=2\pi/3$。
- 第三步:固定向量分别为$(1,1,1)$、$(1,1,-1)$；反对称部分的轴向量分别正比于这两个向量，因$\sin(2\pi/3)>0$，取对应单位向量即给右手角$2\pi/3$。
- 第四步:不同轴使作用顺序改变结果，不能把平面旋转角相加律直接用于三维。

## draft-c42-03 · C42

**题目**

给定$u,v\in\mathbb R^3$，分类将$u$映到$v$的单个过原点平面反射。证明存在性与唯一性条件，并求将$(1,2,2)$映到$(2,1,2)$的反射矩阵。

**推导**

反射保持范数，故必要$\|u\|=\|v\|$。若$u\ne v$且等范数，令$n=(u-v)/\|u-v\|$；由$\|u-v\|^2=2(\|u\|^2-u\cdot v)$得$2(n\cdot u)n=u-v$，所以$H=I-2nn^{\mathsf T}$满足$Hu=v$。反过来任何满足条件的反射都有$u-v=2(n\cdot u)n$，法线必须平行$u-v$，故矩阵唯一。若$u=v\ne0$，任意单位$n\perp u$都给反射，故不唯一；若均为零，任意单位法线都可以。范数不等时无解。指定数据法线$(-1,1,0)/\sqrt2$，得到$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$。

**答案**

等范数且不同则唯一；相同则有多种；范数不等无解。指定矩阵交换$x,y$。

**场景对象**

- 给定$u,v\in\mathbb R^3$，分类将$u$映到$v$的单个过原点平面反射。证明存在性与唯一性条件，并求将$(1,2,2)$映到$(2,1,2)$的反射矩阵。
- 等范数且不同则唯一；相同则有多种；范数不等无解。指定矩阵交换$x,y$。

**场景步骤**

- 第一步:反射保持范数，故必要$\|u\|=\|v\|$。
- 第二步:若$u\ne v$且等范数，令$n=(u-v)/\|u-v\|$；由$\|u-v\|^2=2(\|u\|^2-u\cdot v)$得$2(n\cdot u)n=u-v$，所以$H=I-2nn^{\mathsf T}$满足$Hu=v$。
- 第三步:反过来任何满足条件的反射都有$u-v=2(n\cdot u)n$，法线必须平行$u-v$，故矩阵唯一。
- 第四步:若$u=v\ne0$，任意单位$n\perp u$都给反射，故不唯一；若均为零，任意单位法线都可以。
- 第五步:范数不等时无解。
- 第六步:指定数据法线$(-1,1,0)/\sqrt2$，得到$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$。

## draft-c42-04 · C42

**题目**

判断矩阵 $A=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}&0\\-\frac{\sqrt3}{2}&\frac12&0\\0&0&-1\end{pmatrix}$ 是否为正交矩阵；若是，说明其对应的几何变换。

**推导**

前两维块为$R(-\pi/3)$，第三维为$-1$，故$A^{\mathsf T}A=I$、$\det A=-1$。它是绕$z$轴旋转$-\pi/3$与关于$xy$平面反射的可交换复合。特征值为$1/2\pm i\sqrt3/2,-1$，没有$1$，所以没有非零逐点固定向量；$z$轴仍是旋转因子的轴并被整个变换作为集合保持，轴上点变号。不能把“没有逐点固定轴”误说为复合中没有旋转轴。

**答案**

正交、行列式$-1$；绕$z$轴旋转$-\pi/3$与$xy$平面反射的复合，无非零固定点。

**场景对象**

- 判断矩阵 $A=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}&0\\-\frac{\sqrt3}{2}&\frac12&0\\0&0&-1\end{pmatrix}$ 是否为正交矩阵；若是，说明其对应的几何变换。
- 正交、行列式$-1$；绕$z$轴旋转$-\pi/3$与$xy$平面反射的复合，无非零固定点。

**场景步骤**

- 第一步:前两维块为$R(-\pi/3)$，第三维为$-1$，故$A^{\mathsf T}A=I$、$\det A=-1$。
- 第二步:它是绕$z$轴旋转$-\pi/3$与关于$xy$平面反射的可交换复合。
- 第三步:特征值为$1/2\pm i\sqrt3/2,-1$，没有$1$，所以没有非零逐点固定向量；$z$轴仍是旋转因子的轴并被整个变换作为集合保持，轴上点变号。
- 第四步:不能把“没有逐点固定轴”误说为复合中没有旋转轴。

## draft-c42-05 · C42

**题目**

证明:实正交矩阵的特征值的模长为 $1$(实特征值只能为 $\pm1$),且 $\det A=\pm1$;由此说明三维正交变换的分类:行列式为 $+1$ 时是旋转(绕特征值 $1$ 的轴),行列式为 $-1$ 时是旋转与反射的复合。

**推导**

模长:设 $Av=\lambda v$($v$ 为复特征向量)。取共轭转置:$v^{\mathsf H}A^{\mathsf T}Av=\bar\lambda\lambda v^{\mathsf H}v$,而 $A^{\mathsf T}A=I$,故 $v^{\mathsf H}v=|\lambda|^2v^{\mathsf H}v$,得 $|\lambda|=1$。实特征值只能为 $\pm1$。行列式:特征值之积,每个模长为 $1$,而 $\det A$ 为实数,故 $\det A=\pm1$(实矩阵的复特征值共轭成对,乘积为正实数)。三维分类:奇数维实矩阵至少有一个实特征值(实系数特征多项式次数为 $3$,必有实根),即 $\pm1$。若 $\det A=1$:特征值组合(计重数)为 $(1,1,1)$、$(1,-1,-1)$ 或 $(1,e^{i\theta},e^{-i\theta})$,特征值 $1$ 必出现;其对应的特征方向为不动轴,$A$ 在其正交补平面上的限制是行列式为 $+1$ 的二维正交矩阵,即旋转(含 $-I$,即 $180^\circ$ 旋转的情形),故 $A$ 是绕该轴的旋转。若 $\det A=-1$:特征值 $-1$ 必出现(类似枚举),设其单位特征向量为 $v$;在 $v^\perp$ 上,$\det(A|_{v^\perp})=\det A/(-1)=+1$,故 $A|_{v^\perp}$ 是旋转。于是 $A$ 是关于平面 $v^\perp$ 的反射与绕轴 $v$ 旋转的复合。

**答案**

证明见解法(模长 $1$ 由 $A^{\mathsf T}A=I$ 得;分类由实特征值存在性与行列式符号得)。

**场景对象**

- 证明:实正交矩阵的特征值的模长为 $1$(实特征值只能为 $\pm1$),且 $\det A=\pm1$;由此说明三维正交变换的分类:行列式为 $+1$ 时是旋转(绕特征值 $1$ 的轴),行列式为 $-1$ 时是旋转与反射的复合。
- 证明见解法(模长 $1$ 由 $A^{\mathsf T}A=I$ 得;分类由实特征值存在性与行列式符号得)。

**场景步骤**

- 第一步:模长:设 $Av=\lambda v$($v$ 为复特征向量)。
- 第二步:取共轭转置:$v^{\mathsf H}A^{\mathsf T}Av=\bar\lambda\lambda v^{\mathsf H}v$,而 $A^{\mathsf T}A=I$,故 $v^{\mathsf H}v=|\lambda|^2v^{\mathsf H}v$,得 $|\lambda|=1$。
- 第三步:实特征值只能为 $\pm1$。
- 第四步:行列式:特征值之积,每个模长为 $1$,而 $\det A$ 为实数,故 $\det A=\pm1$(实矩阵的复特征值共轭成对,乘积为正实数)。
- 第五步:三维分类:奇数维实矩阵至少有一个实特征值(实系数特征多项式次数为 $3$,必有实根),即 $\pm1$。
- 第六步:若 $\det A=1$:特征值组合(计重数)为 $(1,1,1)$、$(1,-1,-1)$ 或 $(1,e^{i\theta},e^{-i\theta})$,特征值 $1$ 必出现;其对应的特征方向为不动轴,$A$ 在其正交补平面上的限制是行列式为 $+1$ 的二维正交矩阵,即旋转(含 $-I$,即 $180^\circ$ 旋转的情形),故 $A$ 是绕该轴的旋转。
- 第七步:若 $\det A=-1$:特征值 $-1$ 必出现(类似枚举),设其单位特征向量为 $v$;在 $v^\perp$ 上,$\det(A|_{v^\perp})=\det A/(-1)=+1$,故 $A|_{v^\perp}$ 是旋转。
- 第八步:于是 $A$ 是关于平面 $v^\perp$ 的反射与绕轴 $v$ 旋转的复合。
