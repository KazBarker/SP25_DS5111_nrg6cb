'''
Test to ensure the current OS is Linux.
'''
import platform

def test_linux_os():
    '''
    Test for Linux OS.
    '''
    assert platform.system() == 'Linux', f"""
    Platform should be Linux but {platform.system()} was detected."""
