from .agent import Agent
from .agent import AgentConfig


def agent_class_filter(x):
    import inspect
    return inspect.isclass(x) and issubclass(x, Agent) and x not in [Agent]


loaded_agents = None


def load_agents(verbose=False, warn=False):
    global loaded_agents
    if loaded_agents is not None:
        return loaded_agents
    from importlib import import_module
    import os
    import inspect

    loaded_agents = {}

    for d in os.listdir(os.path.dirname(__file__)):
        d_path = os.path.join(os.path.dirname(__file__), d)
        if os.path.isdir(d_path) and \
                not d.startswith("_") and \
                not d.startswith(".") and \
                os.path.exists(os.path.join(d_path, "agent.py")):
            if verbose:
                print("Importing '{}'...".format(d))
            import_module("agents.{}.agent".format(d))
            mod = getattr(globals()[d], "agent")
            mems = inspect.getmembers(mod, agent_class_filter)
            if len(mems) == 1:
                AgentClass = inspect.getmembers(mod, agent_class_filter)[0][1]
                loaded_agents[d] = AgentClass
            else:
                if warn:
                    print("Error loading agent '{}'.".format(d))
    return loaded_agents


def reload_agents():
    global loaded_agents
    loaded_agents = None
    return load_agents()
