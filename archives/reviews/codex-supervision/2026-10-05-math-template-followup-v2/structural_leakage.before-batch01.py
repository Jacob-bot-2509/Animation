"""Structural leak candidate screen, independent of category/signature metadata.

Candidates require semantic review. Unknown structures are not certified negatives.
No sample IDs, hashes or label tables are used in the detector. Scores are fractions.
"""
from __future__ import annotations
import hashlib
import re
from fractions import Fraction
VERSION='structure-candidates-v3'


def normalize(text):
    text=re.sub(r'\s+','',text)
    text=text.replace(r'\dfrac',r'\frac').replace(r'\displaystyle','')
    text=text.replace('（','(').replace('）',')')
    # Keep powers: x^2 and x^3 are different mathematical objects.
    text=re.sub(r'(?<![\^\d])\d+(?:\.\d+)?', '#', text)
    return text


def _matrix(text):
    match=re.search(r'\\begin\{[pb]matrix\}(.*?)\\end\{[pb]matrix\}',text)
    if not match:return None
    rows=match[1].split(r'\\')
    cells=[re.sub(r'\s+','',row).split('&') for row in rows]
    if len(cells)==2 and all(len(row)==2 for row in cells):
        numeric=all(re.fullmatch(r'[+-]?\d+(?:\.\d+)?',x) for row in cells for x in row)
        if not numeric:return None
        return 'balanced-symmetric-2' if cells[0][0]==cells[1][1] and cells[0][1]==cells[1][0] else 'numeric-2'
    return None


def structure_keys(problem):
    if not isinstance(problem,str) or not problem.strip():return set()
    t=re.sub(r'\s+','',problem);keys=set();matrix=_matrix(t)
    if '平面' in t and '距离' in t and ('点' in t or re.search(r'P\(',t)):
        keys.add('point-plane-distance')
    if '异面' in t and '距离' in t:keys.add('skew-lines-distance')
    if '直线' in t and ('球面' in t or '椭球' in t) and ('交点' in t or '相交' in t):
        keys.add('line-positive-quadric-intersection')
    if '二次曲面' in t and ('类型' in t or '形状' in t):
        # Diagonal classification keeps signature of signs, not numerical magnitudes.
        if not re.search(r'xy|xz|yz',t):
            negative=len(re.findall(r'-(?:\d*)[xyz]\^2',t))
            keys.add('diagonal-quadric-negative-count-'+str(negative))
    if matrix and ('逆矩阵' in t or re.search(r'A\^\{-1\}',t)):
        keys.add('inverse-numeric-matrix-2')
    if matrix=='balanced-symmetric-2' and (any(w in t for w in ('特征','对角化','谱分解')) or ('线性变换' in t and '几何' in t)):
        keys.add('spectrum-balanced-symmetric-2')
    if ('泰勒' in t or '按' in t and '展开' in t) and 'x^3' in t and not re.search(r'sin|cos|exp|ln|log',t):
        keys.add('taylor-cubic-polynomial')
    if '基' in t and '坐标' in t and (r'R^2' in t or r'R}^2' in t):
        keys.add('coordinate-change-2')
    if ('sum' in t or '级数' in t) and (re.search(r'n(?:\\cdot|\*)?\d+\^n',t) or re.search(r'\\frac\{x\^n\}\{n\}',t)):
        keys.add('logarithmic-power-series-and-evaluation')
    if ('sum' in t or '级数' in t) and (re.search(r'n\(n\+\d+\)',t) or re.search(r'n\^2\+n',t)):
        keys.add('telescoping-constant-gap-series')
    if ('二次型' in t or '二次曲线' in t or '二次曲面' in t) and re.search(r'xy|xz|yz',t):
        if any(w in t for w in ('标准','惯性','正定','类型','主轴')):
            dim=3 if 'z' in re.sub(r'\\[a-zA-Z]+','',t) else 2
            keys.add('quadratic-form-reduction-'+str(dim))
    if ('阳性' in t and '患病' in t) or ('车间' in t and '次品' in t and '来自' in t):
        keys.add('two-latent-class-bayes-posterior')
    if ('均匀分布' in t or re.search(r'U\(0,1\)',t)) and '密度' in t and ('X^' in t or r'\sqrt{X}' in t):
        keys.add('uniform-monotone-power-transform')
    return keys


def compare(left,right):
    if not all(isinstance(x,str) and x.strip() for x in (left,right)):
        return {'candidate':False,'coverage':'UNKNOWN','reasons':[],'score':'0'}
    shared=structure_keys(left)&structure_keys(right)
    a,b=normalize(left),normalize(right)
    # Exact normalized object-and-task wording handles pure numerical substitutions.
    numeric_clone=a==b and len(a)>=15
    sa={a[i:i+3] for i in range(max(0,len(a)-2))}
    sb={b[i:i+3] for i in range(max(0,len(b)-2))}
    score=Fraction(len(sa&sb),len(sa|sb)) if sa|sb else Fraction(0)
    return {'candidate':bool(shared or numeric_clone),'coverage':'CANDIDATE' if shared or numeric_clone else 'UNKNOWN',
            'reasons':sorted(shared)+(['numeric-normalized-object-and-task'] if numeric_clone else []),
            'score':str(score),'rule':VERSION}


def implementation_sha256():
    from pathlib import Path
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
