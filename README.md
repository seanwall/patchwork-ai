# patchwork-ai
Patchwork model &amp; learned AI for CS 4150

## Installation
This program was built using Python 3.7

I haven't made an executable yet but this can be run from the Patchwork.py file in the top level directory if you have python installed.

### Patchwork.py cmd line args
If no arguments are specified Patchwork.py will default to a Player vs AI run.

-m {pp, pa, aa} or --mode {pp, pa, aa} : "pp" designates a Player vs Player run, "pa" designates Player vs AI, "aa" designates AI vs AI

-s {int} or --sample {int} : given in addition to "-m aa", will run the designated number of sample games AI v AI. Used to calculate win % for different AI implementations

An additional flag will be added in the future to designate if the run should be used as training data for AI learning
