#!/sv/venv/perscripts/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal

vsDict = {}

for index, pName in enumerate(ELOCal.nameList):
    vsDict[pName] = {'index': index, "wins": [0]*len(ELOCal.nameList)}


def main(logCount=None):
    if not logCount:
        logCount = ELOCal.getLogCount()[0][0]

    ELOCal.debugPrint("UVR: Found Log Count", logCount)

    processedLog = ELOCal.getLog(processed=True, newLogCount=logCount)

    ELOCal.debugPrint("UVR: Processed Log", processedLog)

    for result in processedLog:
        vsDict[result[0]]["wins"][vsDict[result[1]]["index"]] = vsDict[result[0]]["wins"][vsDict[result[1]]["index"]] + 1

    vsResults = []

    for name in ELOCal.nameList:
        vsResults.append(vsDict[name]["wins"])

    ELOCal.debugPrint("UVR: vs List Results", vsResults)

    ELOCal.updateCells(vsResults, ELOCal.LOG_SPREADSHEET_ID, ELOCal.vsResultRange)


if __name__ == '__main__':
    main()
