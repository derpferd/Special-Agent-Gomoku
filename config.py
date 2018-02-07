# Author: Jonathan Beaulieu
from enum import Enum, auto, IntEnum
from typing import List

import os

from agents import AgentConfig


class ConfigType(Enum):
    test = auto()
    train = auto()


class Verbosity(IntEnum):
    error = auto()
    warning = auto()
    info = auto()
    debug = auto()

    def at_level(self, level):
        return self >= level


class AgentTestConfig(AgentConfig):
    id: str
    name: str
    load: bool
    load_id: int

    defaults = {"load": False}

    @classmethod
    def from_json(cls, obj):
        assert "id" in obj, "Agent must have an id"
        assert "name" in obj, "Agent must have a name"
        config = cls()
        config.id = obj.pop("id")
        config.name = obj.pop("name")
        config.load = cls.defaults["load"]
        if "load_id" in obj:
            config.load = True

        if config.load:
            assert "load_id" in obj
            config.load_id = obj.pop("load_id")

        assert len(obj) == 0, "Agent Test Config had unknown key(s): [{}]".format(", ".join(obj.keys()))
        return config

    @property
    def model_dir_name(self):
        return "{}-{}".format(self.name, self.load_id)


class Config:
    type: ConfigType
    env: str
    rounds: int
    models_dir: str
    verbose: Verbosity
    defaults = {"env": "Gomoku19x19-v1", "rounds": 1}

    # Test type only
    agents: List[AgentTestConfig]

    @classmethod
    def from_json(cls, obj):
        assert "type" in obj, "Json config must have a type!"
        t = obj["type"]
        assert t in ["train", "test"], "Type must be 'train' or 'test'!"
        config = None
        if t == "train":
            config = cls.from_train(obj)
        if t == "test":
            config = cls.from_test(obj)

        config.type = ConfigType[obj.pop("type")]

        # load values with defaults
        for name, value in cls.defaults.items():
            if name in obj:
                value = obj.pop(name)
            setattr(config, name, value)

        assert len(obj) == 0, "Config had unknown key(s): [{}]".format(", ".join(obj.keys()))

        return config

    @classmethod
    def from_train(cls, obj):
        config = cls()
        return config

    @classmethod
    def from_test(cls, obj):
        config = cls()
        assert "agents" in obj
        assert len(obj["agents"]) == 2, "Config must have two agents"
        config.agents = []
        for agent_obj in obj.pop("agents"):
            config.agents += [AgentTestConfig.from_json(agent_obj)]
        assert len(set([x.id for x in config.agents])) == len(config.agents), "Each agent id must be unique."
        return config


def get_model_dir(model_dir, model_dir_name):
    return os.path.join(model_dir, model_dir_name)
