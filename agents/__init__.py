from .agent import Agent

loaded_agents = {}


def agent_class_filter(x):
    import inspect
    return inspect.isclass(x) and issubclass(x, Agent) and x not in [Agent]


def import_agents():
    from importlib import import_module
    import os
    import inspect

    print("Agents", os.listdir(os.path.dirname(__file__)))
    for d in os.listdir(os.path.dirname(__file__)):
        d_path = os.path.join(os.path.dirname(__file__), d)
        if os.path.isdir(d_path) and \
                not d.startswith("_") and \
                not d.startswith(".") and \
                os.path.exists(os.path.join(d_path, "agent.py")):
            print("Importing '{}'...".format(d))
            import_module("agents.{}.agent".format(d))
            mod = getattr(globals()[d], "agent")
            mems = inspect.getmembers(mod, agent_class_filter)
            if len(mems) == 1:
                AgentClass = inspect.getmembers(mod, agent_class_filter)[0][1]
                loaded_agents[d] = AgentClass
            else:
                print("Error loading agent '{}'.".format(d))


import_agents()
