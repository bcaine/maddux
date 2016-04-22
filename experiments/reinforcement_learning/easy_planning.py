import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tempfile
import tensorflow as tf

# TODO: Make sure these import correctly for Rob!
from tf_rl.controller import DiscreteDeepQ
from tf_rl.models import MLP
import Planning
from maddux.rl_experiments.predefined_environments import get_easy_environment

# Define a log file to use with tensorboard
# Not that we currently make use of tensorboard at all
LOG_DIR = tempfile.mkdtemp()
print LOG_DIR

# The directory to save the animations to
# TODO: Take this as input
SAVE_DIR = "/home/colin/robots/maddux/saved_experiments"

# Define the simulation
sim = Planning(get_easy_environment())

# Tensorflow!
tf.reset_default_graph()
session = tf.InteractiveSession()
journalist = tf.train.SummaryWriter(LOG_DIR)

# Brain maps from observation to Q values for different actions.
brain = MLP([sim.observation_size,], [200, 200, sim.num_actions],
            [tf.tanh, tf.tanh, tf.identity])
optimizer = tf.train.RMSPropOptimizer(learning_rate= 0.001, decay=0.9)

# DiscreteDeepQ object
current_controller = DiscreteDeepQ(sim.observation_size, sim.num_actions, brain,
                                   optimizer, session, random_action_probability=0.1,
                                   discount_rate=0.99, exploration_period=1000,
                                   max_experience=10000, store_every_nth=1,
                                   train_every_nth=1, summary_writer=journalist)

# Initialize the session
session.run(tf.initialize_all_variables())
session.run(current_controller.target_network_update)
journalist.add_graph(session.graph)

# Run the simulation and let the robot learn
num_simulations = 0

iterations_needed = []
total_rewards = []

try:
    for game_idx in range(3000):
        current_random_prob = current_controller.random_action_probability
        update_random_prob = game_idx != 0 and game_idx % 100 == 0 and current_random_prob > 0.01
        if update_random_prob:
            current_controller.random_action_probability = current_random_prob - 0.01
        game = Planning(get_easy_environment())
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
            game.save_path(SAVE_DIR, game_idx)


except KeyboardInterrupt:
    print "Interrupted"
