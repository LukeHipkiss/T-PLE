#!/usr/bin/python2.7
from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='VS ELO Calculator')
    parser.add_argument('-w', '--winner', nargs="?", help='The winner', type=float)
    parser.add_argument("-l", '--loser', nargs="?", help="The looser", type=float)
    args = parser.parse_args(sys.argv[1:])

    winner = args.winner
    if not winner:
        winner = raw_input("Winner's name: ")

    loser = args.loser
    if not loser:
        loser = raw_input("Loser's name: ")

    ELOs = ELOCal.getELOs()

    updatedELOs = ELOCal.calcHTHELO(ELOs, winner, loser)

    updatedELOs = ELOCal.correctExpectedInt(updatedELOs)

    # ELOCal.updateCells(updatedELOs, ELOCal.ELORange)
    print(updatedELOs)


if __name__ == '__main__':
    main()
