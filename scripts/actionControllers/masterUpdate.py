#!/sv/venv/T-PLE/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal
import winStreakUpdate
import updateVSResults


def main():
    accumulativeDiff = False
    currentLog, winsLosses, ELOs = ELOCal.getLog(), ELOCal.getWL(), ELOCal.getELOs()

    unLoggedIndexes = ELOCal.findUnLoggedMatches(currentLog)

    if accumulativeDiff:
        for pIndex in ELOs:
            pIndex[2] = 0

    for index in unLoggedIndexes:
        ELOs = ELOCal.correctExpectedInt(
            ELOCal.calcHTHELO(
                ELOs,
                currentLog[index][0],
                currentLog[index][1],
                accumulativeDiff=accumulativeDiff
            )
        )

        winsLosses = ELOCal.updateWinLossTable(winsLosses, currentLog[index][0], currentLog[index][1])

        currentLog[index][2] = "TRUE"

    ELOCal.debugPrint("MU: Updated ELOs", ELOs)

    logCount = int(ELOCal.getLogCount()[0][0]) + 1

    if currentLog[0][0] != '':
        blankLog = [['', '', 'FALSE']]*100

        writeToRange = ELOCal.UPLOGRange.format(str(logCount), str(len(currentLog) + logCount))

        ELOCal.updateCells(blankLog, ELOCal.LOG_SPREADSHEET_ID, ELOCal.LOGRange, dataType="USER_ENTERED")
        ELOCal.updateCells(currentLog, ELOCal.LOG_SPREADSHEET_ID, writeToRange, dataType="USER_ENTERED")

        ELOCal.updateCells(winsLosses, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.WLRange)
        ELOCal.updateCells(ELOs, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.ELORange)

    updateVSResults.main()
    winStreakUpdate.main()

    ELOCal.log("Complete")


if __name__ == '__main__':
    main()
