#!/sv/venv/T-PLE/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal
import winStreakUpdate
import updateVSResults


def main():
    accumulativeDiff = False
    currentLog, winsLosses, ELOs = ELOCal.getLog(), ELOCal.getWL(), ELOCal.getELOs()

    unLoggedIndexes = ELOCal.cleanEmptyIndexes(currentLog)

    if accumulativeDiff:
        for pIndex in ELOs:
            pIndex[2] = 0

    for index in unLoggedIndexes:
        ELOs = ELOCal.correctExpectedInt(
            ELOCal.calcHTHELO(
                ELOs,
                index[0],
                index[1],
                accumulativeDiff=accumulativeDiff
            )
        )

        winsLosses = ELOCal.updateWinLossTable(winsLosses, index[0], index[1])

    ELOCal.debugPrint("MU: Updated ELOs", ELOs)

    logCount = int(ELOCal.getLogCount()[0][0]) + ELOCal.PLOGRange_Offset + 1

    if currentLog[0][0] != '':
        blankLog = [['', '']]*100

        writeToRange = ELOCal.UPLOGRange.format(str(logCount), str(len(unLoggedIndexes) + logCount))

        ELOCal.updateCells(blankLog, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.LOGRange, dataType="USER_ENTERED")
        ELOCal.updateCells(unLoggedIndexes, ELOCal.MAIN_SPREADSHEET_ID, writeToRange, dataType="USER_ENTERED")

        ELOCal.updateCells(winsLosses, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.WLRange)
        ELOCal.updateCells(ELOs, ELOCal.MAIN_SPREADSHEET_ID, ELOCal.ELORange)

    updateVSResults.main()
    winStreakUpdate.main()

    ELOCal.log("Complete")


if __name__ == '__main__':
    main()
