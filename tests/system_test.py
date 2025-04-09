'''
Test to ensure the current OS is Linux.
'''
import platform
import pytest
from packaging.version import Version

def test_linux_os():
    '''
    Test for Linux OS.
    '''
    if not platform.system() == 'Linux':
        pytest.fail(f'Requires Linux but detected {platform.system()}')

def test_python_version():
    '''
    Test python is version 3.10 or 3.11
    '''
    my_python = Version(platform.python_version())

    if not (my_python >= Version('3.10')) & (my_python < Version('3.12')):
        # pytest.fail(f'Requires python>=3.10,<3.12 (currently using {my_python})')
        pytest.fail(f'Requires python>=3.12,<=3.13 (currently using {my_python})')
