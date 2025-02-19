'''
A simple test file for setting up pytest.
'''
from bin import sample_adder as adder

def test_04_lab():
    '''
    Testing pytest.
    '''
    assert 5 == adder.add(2, 3), "Adder failed with 2 + 3, expected 5"
