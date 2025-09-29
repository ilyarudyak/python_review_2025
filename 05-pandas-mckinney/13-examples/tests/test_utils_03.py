import pytest
from pathlib import Path
import sys

# Add the parent directory (13-examples) to sys.path to import utils_03
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils_03 import BabyNames

def test_data_shape():
    bn = BabyNames()
    assert bn.names.shape == (1690784, 4)

def test_total_births_2006():
    bn = BabyNames()
    assert bn.total_births.loc[2006, 'F'] == 1896468
    assert bn.total_births.loc[2006, 'M'] == 2050234

def test_names_with_prop_shape():
    bn = BabyNames()
    assert bn.names_with_prop.shape == (1690784, 5)

def test_prop_sum():
    bn = BabyNames()
    prop_sums = bn.names_with_prop.groupby([bn.YEAR, bn.SEX])[bn.PROP].sum()
    assert all(prop_sums == 1.0)