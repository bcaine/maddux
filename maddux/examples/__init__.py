from arm_test import arm_test
from plot_arm_test import plot_arm_test
from plot_test import plot_test
from plot_obstacle_test import plot_obstacle_test
from animation_test import (ball_animation_test,
                            arm_animation_test,
                            arm_ball_animation_test,
)
from throwing_test import throwing_test
from obstacle_collision_test import obstacle_collision_test


examples = {
    'arm': arm_test,
    'ball_animation': ball_animation_test,
    'arm_animation': arm_animation_test,
    'arm_ball_animation': arm_ball_animation_test,
    'plot_arm': plot_arm_test,
    'plot': plot_test,
    'plot_obstacle': plot_obstacle_test,
    'throw': throwing_test,
    'obstacle_collision': obstacle_collision_test,
}


def run_example(example):
    if example in examples:
        examples[example]()
        return True
    return False
