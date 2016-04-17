from environment import Environment
from simulate import Simulate
plot_type = "matplotlib"

if plot_type == "vpython":
    import plots.vpython_plots as plots
elif plot_type == "matplotlib":
    import plots.matplotlib_plots as plots
else:
    raise ValueError("Please provide either matplotlib or" +\
                     " vpython as plot_type")

import robots
import objects
