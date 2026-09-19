#
# Lets the example scripts import the simulator modules in ../src, from any working directory
#
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'src'))
