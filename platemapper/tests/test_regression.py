from skbio.stats.ordination import OrdinationResults
import sys

def test_ordination_ok():
    exp = OrdinationResults.read("test/ordination_Kurth_JIA_.txt")
    assert len(exp.eigvals) == 2
    assert len(exp.samples) == 56

# def test_ordination_fail():
#     exp = OrdinationResults.read("test/ordination_Kurth_JIA_.txt")
#     assert len(exp.eigvals) == 3
