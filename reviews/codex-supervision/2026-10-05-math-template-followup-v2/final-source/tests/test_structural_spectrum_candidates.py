"""Candidate regression for geometry/spectrum wording, without sample-ID rules."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from animtrain.structural_leakage import compare,structure_keys

class SpectrumCandidateTests(unittest.TestCase):
    def matrix(self,a,b):return r'\begin{pmatrix}'+str(a)+'&'+str(b)+r'\\'+str(b)+'&'+str(a)+r'\end{pmatrix}'
    def test_geometry_to_spectrum_is_candidate_across_words(self):
        a='已知矩阵A='+self.matrix(4,2)+'，分析线性变换的几何影响。'
        b='求矩阵A='+self.matrix(3,1)+'的谱分解。'
        result=compare(a,b);self.assertTrue(result['candidate']);self.assertEqual(result['coverage'],'CANDIDATE')
    def test_projection_packaging_of_spectral_information_is_candidate(self):
        a='求矩阵A='+self.matrix(6,2)+'的特征值及特征向量。'
        b='求A='+self.matrix(5,3)+'的谱分解。'
        self.assertTrue(compare(a,b)['candidate'])
    def test_arbitrary_matrix_geometry_does_not_claim_fixed_directions(self):
        a=r'矩阵\begin{pmatrix}2&1\\3&4\end{pmatrix}对应线性变换的几何影响。'
        self.assertNotIn('spectrum-balanced-symmetric-2',structure_keys(a))
    def test_same_matrix_different_inverse_task_not_certified_overlap(self):
        a='求A='+self.matrix(3,1)+'的逆矩阵。';b='求A='+self.matrix(3,1)+'的谱分解。'
        result=compare(a,b);self.assertFalse(result['candidate']);self.assertEqual(result['coverage'],'UNKNOWN')
    def test_diagonal_ellipse_tangent_candidate(self):
        a=r'椭圆$x^2+4y^2=8$在点$(2,1)$处的切线。'
        b=r'椭圆$3x^2+2y^2=5$在点$(1,1)$处的切线。'
        self.assertTrue(compare(a,b)['candidate'])
    def test_ellipse_area_is_not_tangent_candidate(self):
        a=r'求椭圆$x^2+4y^2=8$的面积。'
        b=r'椭圆$3x^2+2y^2=5$在点$(1,1)$处的切线。'
        self.assertNotIn('given-point-diagonal-ellipse-tangent',structure_keys(a))
        self.assertEqual(compare(a,b)['coverage'],'UNKNOWN')
    def test_unit_uniform_sum_candidate_across_notation(self):
        a=r'X与Y独立且服从(0,1)上的均匀分布，求X+Y的密度。'
        b=r'X,Y独立且服从U(0,1)，求X+Y超过3/2的概率。'
        self.assertTrue(compare(a,b)['candidate'])
    def test_uniform_minimum_and_normal_sum_not_uniform_sum_family(self):
        minimum=r'X与Y独立且服从U(0,1)，求min(X,Y)的密度。'
        normal=r'X与Y独立且服从N(0,1)，求X+Y的密度。'
        for problem in (minimum,normal):
            self.assertNotIn('independent-unit-uniform-sum',structure_keys(problem))
if __name__=='__main__':unittest.main()
