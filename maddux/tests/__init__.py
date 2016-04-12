from arm_tests import ArmTest

armTest = ArmTest()
tests = {
    'fkine': armTest.test_fkine,
}


def run_test(test):
    if test in tests:
        tests[test]()
        return True
    return False
