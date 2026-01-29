# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - Main
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# To prevent decompiling strings, all comment strings must use a single-line comment, even if they cannot be recognized as __doc__.
# This is a great, never-ending project, always remain in awe. All for the benefit of the organization.
# Simulate a large-scale cyber intrusion and collect infection data for future research in the process.
# We will continue to improve this project and strive to collect more complete and analytical data.
# We also expect to take a shortcut with this approach.
# The github project is not fully synchronized in https://github.com/GVSADS/Termination


from TerminationLib import Termination
from TLib.T_imports import *
from TLib import *
from TLhread import *
import TLUI


if __name__ == "__main__":
    mp.freeze_support()
    Termination()
    os._exit(0)

    import cProfile
    import pstats
    profiler = cProfile.Profile()
    profiler.enable()
    Termination()
    profiler.disable()
    profiler.dump_stats(os.path.join(os.getenv("TEMP"), "TProFileResults.prof"))
    with open(os.path.join(os.getenv("TEMP"), "TProFileResults.txt"), "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumulative').print_stats()
        stats.print_callers("T_Process.py:85(ShouldStop)")
    os._exit(0)
