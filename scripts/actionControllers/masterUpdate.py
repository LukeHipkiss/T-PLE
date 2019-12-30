#!/sv/venv/T-PLE/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal
import winStreakUpdate
import updateVSResults
import historicELOUpdate


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

    logCount = int(ELOCal.getLogCount()[0][0]) + ELOCal.P_LOG_Range_Offset + 1

    if currentLog[0][0] != '':
        blankLog = [['', '']]*100

        writeToRange = ELOCal.UP_LOG_Range.format(str(logCount), str(len(unLoggedIndexes) + logCount))

        # BLANK LOG OVER UNPROCESSED GAMES
        ELOCal.updateCells(
            values=blankLog,
            sheetRange=ELOCal.LOG_Range,
            dataType="USER_ENTERED"
        )

        # WRITE NEW PROCESSED GAMES
        ELOCal.updateCells(
            values=unLoggedIndexes,
            sheetRange=writeToRange,
            dataType="USER_ENTERED"
        )

        # UPDATE WINS AND LOSSES IN PRIMARY SHEET
        ELOCal.updateCells(
            values=winsLosses,
            sheetRange=ELOCal.WL_Range
        )

        # UPDATE ELOs
        ELOCal.updateCells(
            values=ELOs,
            sheetRange=ELOCal.ELO_Range
        )

    updateVSResults.main()
    winStreakUpdate.main()
    historicELOUpdate.main()

    ELOCal.log("Complete")


if __name__ == '__main__':
    main()
