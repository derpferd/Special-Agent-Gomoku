#!/usr/bin/python3
# Author: Jonathan Beaulieu
import json
from typing import List, Callable, Optional

import click
import gym
import os

from collections import defaultdict
from gym_gomoku import GomokuEnv

from agents import Agent, load_agents
from config import Config, ConfigType, Verbosity, get_model_dir
from error import ModelNotFound


def play_game(env_gen: Callable[[], GomokuEnv], agents: List[Agent], seed: int=None, verbose: Verbosity=Verbosity.error) -> Optional[str]:
    """Plays a single game between two agents.

    Args:
        env_gen:
        agents:
        seed:
        verbose:

    Returns: The id of the winning player. If "cats" game returns None.
    """
    assert len(agents) == 2, "You must pass two agents."

    env = env_gen()
    if seed is not None:
        env.seed(seed)

    for agent in agents:
        agent.start_game(env.action_space.valid_spaces)

    cur_agent, o_agent = agents  # type: Agent
    env.reset()
    winner = None
    while not env.done:
        if verbose.at_level(Verbosity.debug) or cur_agent.config.is_human:
            env.render()
        action = cur_agent.move(env.state)
        _, reward, done, _ = env.step(action)

        if done:
            cur_agent.end_game(reward == -1)
            o_agent.end_game(reward == 1)
            if reward == -1:
                winner = cur_agent.config.id
            else:
                winner = o_agent.config.id

        # switch players
        cur_agent, o_agent = o_agent, cur_agent
    if verbose.at_level(Verbosity.debug) or cur_agent.config.is_human:
        env.render()
    return winner


def test(config: Config):
    def create_env():
        return gym.make(config.env)
    agent_clss = load_agents(verbose=config.verbose.at_level(Verbosity.info), warn=config.verbose.at_level(Verbosity.warning))

    agents = []
    for agent_config in config.agents:
        assert agent_config.name in agent_clss, "Could find agent by the name of '{}'.\nJonathan probably spelt something wrong :(".format(agent.name)
        agent_cls = agent_clss[agent_config.name]
        agent = agent_cls(agent_config)
        if agent_config.load:
            model_dir = get_model_dir(config.models_dir, agent_config.model_dir_name)
            if not os.path.exists(model_dir):
                raise ModelNotFound("The is no Model @ '{}'".format(model_dir))
            agent.load_model(model_dir)
        agents += [agent]

    scores = defaultdict(int)
    for round in range(config.rounds):
        winner = play_game(create_env, agents, verbose=config.verbose)
        scores[winner] += 1
        if config.verbose.at_level(Verbosity.info):
            print("Winner for round {}: {}".format(round + 1, winner))

    print("==== Scores ====")
    for agent, score in scores.items():
        print("{}: {} of {}".format(agent, score, config.rounds))


def train(config: Config):
    raise NotImplemented("The training feature isn't implemented yet.")


@click.command()
@click.argument('config', type=click.File('r'))
@click.option('-m', '--model-dir', type=click.Path(file_okay=False), default="models")
@click.option('-v', '--verbose', count=True, help="This is a flag to control how much is output.\n"
                                                  "Default is only Errors, "
                                                  "(-v) for Warnings, "
                                                  "(-vv) for Info or "
                                                  "(-vvv) for Debug ")
def main(config, model_dir, verbose):
    """This is a program to run agents vs each other in Gomoku."""
    config = Config.from_json(json.load(config))
    config.verbose = Verbosity(verbose + 1)
    if config.verbose.at_level(Verbosity.warning):
        print("Verbosity level is {}".format(config.verbose.name))

    if not os.path.exists(model_dir):
        if config.verbose.at_level(Verbosity.info):
            print("Creating models directory: '{}'".format(model_dir))
        os.mkdir(model_dir)
    config.models_dir = model_dir

    if config.type == ConfigType.test:
        test(config)
    elif config.type == ConfigType.train:
        train(config)
    else:
        raise NotImplemented("Sorry currently only support for 'test' and 'train' configs is available. "
                             "Maybe check your config type or update this package.")


if __name__ == '__main__':
    main()
