#!/usr/bin/python3
from typing import List, Callable

import gym
from gym_gomoku import GomokuEnv

from agents import Agent, loaded_agents


def play_game(env_gen: Callable[[], GomokuEnv], agents: List[Agent], seed: int=None, debug: bool=False):
    assert len(agents) == 2, "You must pass two agents."

    env = env_gen()
    if seed is not None:
        env.seed(seed)

    for agent in agents:
        agent.start_game(env.action_space.valid_spaces)

    cur_agent, o_agent = agents  # type: Agent
    env.reset()
    if debug:
        env.render()
    while not env.done:
        action = cur_agent.move(env.state)
        _, reward, done, _ = env.step(action)
        if debug:
            env.render()

        if done:
            cur_agent.end_game(reward == 1)
            o_agent.end_game(reward != 1)
            break

        # switch players
        cur_agent, o_agent = o_agent, cur_agent


def main():
    def create_env():
        return gym.make('Gomoku19x19-v1')
    agents = [loaded_agents["random"](), loaded_agents["random"]()]
    play_game(create_env, agents, debug=True)


if __name__ == '__main__':
    main()
