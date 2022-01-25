#!usr/bin/env python3 
"""
A custom command line program for running a long series of games between 
two bots for the purposes of evaluation.

Based on tournament.py, but optimized for a high number of games, and providing
a usable text output. 
"""

from argparse import ArgumentParser
from api import State, util, engine 
import random, time, os

def run_evaluation(options):
    return

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("bot",
                        dest="bot",
                        help="The name of the bot to be evaluated")

    parser.add_argument("-n", "--sample-size",
                        dest="sample_size",
                        help="The number of games to be played in each")

    run_evaluation(parser.parse_args())

