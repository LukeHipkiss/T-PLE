#!/sv/venv/T-PLE/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal


def main(logCount=None):
    if not logCount:
        logCount = ELOCal.getLogCount()[0][0]

    processedLog = ELOCal.getLog(processed=True, newLogCount=logCount)

    for result in processedLog:
        winner, loser = result[0], result[1]

        ELOCal.calcWLStreak(winner, loser)

    streaks = ELOCal.buildStreakListForSheet()

    ELOCal.updateCells(streaks, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.streakRange)


if __name__ == '__main__':
    main()
