from environment import Environment
from simulate import Simulate

def in_ipython():
    try:
        cfg = get_ipython().config
        return True
    except NameError:
        return False

if in_ipython():
    import plots.vpython_plots as plots
else:
    import plots.matplotlib_plots as plots

import robots
import objects
