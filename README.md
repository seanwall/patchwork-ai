# patchwork-ai
Patchwork model &amp; learned AI for CS 4150

## Rules Overview
https://boardgamegeek.com/boardgame/163412/patchwork

## Project Structure

All ai implementation is in the ai folder.

PatchworkAI contains the overall controller for each AI (random, hand crafted, learned), while Features.py has the learning specific information: a model of the current state (as it is needed by the learner/feature weights), and a representation of the feature weights.

## Installation
This program was built using Python 3.7

I haven't made an executable yet but this can be run from the Patchwork.py file in the top level directory if you have python installed.

### Patchwork.py cmd line args
If no arguments are specified Patchwork.py will default to a Player vs AI run.

-m {pp, pa, aa} or --mode {pp, pa, aa} : "pp" designates a Player vs Player run, "pa" designates Player vs AI, "aa" designates AI vs AI

-s {int} or --sample {int} : given in addition to "-m aa", will run the designated number of sample games AI v AI and provide an output outlining win/lose and certain averages calculated over the course of the game
