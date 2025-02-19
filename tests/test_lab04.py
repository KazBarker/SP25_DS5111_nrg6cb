'''
Simple module for testing pytest.
'''

import sys
sys.path.append('.')
import bin.sample_adder as adder

def test_04_lab():
    '''
    Testing pytest.
    '''
    assert 5 == adder.add(2, 3), "Adder failed with 2 + 3, expected 5"
