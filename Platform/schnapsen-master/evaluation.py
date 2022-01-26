#!usr/bin/env python3 
"""
A custom command line program for running a long series of games between 
two bots for the purposes of evaluation.

Based on tournament.py, but optimized for a high number of games, and providing
a usable text output. 
"""

from argparse import ArgumentParser
from datetime import datetime
from turtle import write_docstringdict
from api import State, util, engine 
import random, time, os

def run_evaluation(options):

    n_of_games = options.sample_size
    write_out_enabled = options.write_out

    if write_out_enabled:
        localtime = datetime.localtime()
        filename = ""

        filename += localtime

        # TODO: Finish opening the file

    subject =  util.load_player(options.subject)

    opponents = []
    for botname in options.opponents.split(","):
        opponents.append(util.load_player(botname))

    for opponent, opponent_name in zip(opponents, options.opponents.split(",")):

        print(f"Playing games between {options.subject} and {opponent_name}.")
        wins = [0, 0]
        score_total = [0, 0]

        for n in range(n_of_games):

            print(f"\rPlaying game [{n + 1}/{n_of_games}]", end="")

            state = State.generate(startingPlayer=1, )

            if n % 2 == 0:
                winner, score = engine.play(subject, opponent, state, verbose=False, fast=True)
                if winner == 1:
                    wins[0] += 1
                    score_total[0] += score
                else:
                    wins[1] += 1
                    score_total[1] += score
            else:
                winner, score = engine.play(opponent, subject, state, verbose=False, fast=True)
                if winner == 1:
                    wins[1] += 1
                    score_total[1] += score
                else:
                    wins[0] += 1
                    score_total[0] += score

        print(f"\nThe subject ({options.subject}) has won {wins[0]}/{n_of_games} games against {opponent_name}.")
        print(f"Win percentage: {(wins[0]/n_of_games)*100:.2f}%")
        print(f"Average score: {score_total[0]/n_of_games}")

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("subject",
                        help="The name of the bot to be evaluated")

    parser.add_argument("-n", "--sample-size",
                        dest="sample_size",
                        help="The number of games to be played between each pair",
                        type=int, default=1000)

    parser.add_argument("-w", "--write-out",
                        dest="write_out",
                        help="This option will create an output file in the \"reports\" directory, marked with the time and botnames.",
                        action="store_true")

    parser.add_argument("-o", "--opponents",
                        dest="opponents",
                        help="Comma-separated list of opponent bot names (enclose with quotes).",
                        default="rand,bully,rdeep")

    run_evaluation(parser.parse_args())