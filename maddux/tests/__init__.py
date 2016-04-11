from arm_test import arm_test
from animation_test import animation_test

tests = {
    'arm_test': arm_test,
    'animation_test': animation_test
}

def run_test(test):
    if test in tests:
        tests[test]()
        return True
    return False
    
