import sys
sys.path.append('simulations/')

import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tempfile
import tensorflow as tf

from tf_rl.controller import DiscreteDeepQ
from tf_rl.models import MLP
from planning import Planning
from maddux.predefined_environments import get_hard_environment_v2

def main(desired_iterations, save_path):
    # Define a log file to use with tensorboard
    # Not that we currently make use of tensorboard at all
    LOG_DIR = tempfile.mkdtemp()
    print "Tensorboard Log: " + LOG_DIR + '\n'

    # The directory to save the animations to
    SAVE_DIR = save_path

    # Define the simulation
    sim = Planning(get_hard_environment_v2())

    # Tensorflow!
    tf.reset_default_graph()
    session = tf.InteractiveSession()
    journalist = tf.train.SummaryWriter(LOG_DIR)
    brain = MLP([sim.observation_size,], [200, 200, sim.num_actions],
                [tf.tanh, tf.tanh, tf.identity])
    optimizer = tf.train.RMSPropOptimizer(learning_rate= 0.001, decay=0.9)

    # DiscreteDeepQ object
    current_controller = DiscreteDeepQ(sim.observation_size, sim.num_actions, brain,
                                       optimizer, session, random_action_probability=0.5,
                                       discount_rate=0.9, exploration_period=1000,
                                       max_experience=10000, store_every_nth=1,
                                       train_every_nth=5, summary_writer=journalist)

    # Initialize the session
    session.run(tf.initialize_all_variables())
    session.run(current_controller.target_network_update)
    journalist.add_graph(session.graph)

    # Run the simulation and let the robot learn
    num_simulations = 0

    iterations_needed = []
    total_rewards = []

    try:
        for game_idx in range(desired_iterations+1):
            current_random_prob = current_controller.random_action_probability
            update_random_prob = game_idx != 0 and game_idx % 200 == 0
            if update_random_prob and 0.01 < current_random_prob <= 0.1:
                current_controller.random_action_probability = current_random_prob - 0.01
            elif update_random_prob and 0.1 < current_random_prob:
                 current_controller.random_action_probability = current_random_prob - 0.1
            game = Planning(get_hard_environment_v2())
            game_iterations = 0

            observation = game.observe()
            while not game.is_over():
                action = current_controller.action(observation)
                reward = game.collect_reward(action)
                new_observation = game.observe()
                current_controller.store(observation, action, reward, new_observation)
                current_controller.training_step()
                observation = new_observation
                game_iterations += 1
            total_rewards.append(sum(game.collected_rewards))
            iterations_needed.append(game_iterations)
            rewards = []
            if game_idx % 50 == 0:
                print "\rGame %d:\nIterations before end: %d." % (game_idx, game_iterations)
                if game.collected_rewards[-1] == 10:
                    print "Hit target!"
                print "Total Rewards: %s\n" % (sum(game.collected_rewards))
                if SAVE_DIR is not None:
                    game.save_path(SAVE_DIR, game_idx)

    except KeyboardInterrupt:
        print "Interrupted"

    # Plot the iterations and reward
    plt.figure(figsize=(12, 8))
    plt.plot(total_rewards, label='Reward')
    plt.plot(iterations_needed, label='Iterations')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run RL on easy environment')
    parser.add_argument('--i', dest='iterations', metavar='N', default=5000, type=int, help='number of iterations of RL to run')
    parser.add_argument('--s', dest='save_path', metavar='S', default=None, help='the dir to save the joint config to animate later')
    args = parser.parse_args()
    main(args.iterations, args.save_path)
