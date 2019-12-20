#!/usr/bin/python2.7
import sys
import math
from scripts.apiController.SheetsAPIController import SheetsAPIController

SAC = SheetsAPIController()
sheet = SAC.service.spreadsheets()

MAIN_SPREADSHEET_ID = '11QxgM2EySs3vbZkxoKJfbLUo7ccfD-fAC06-raQ9gQ8'
LOG_SPREADSHEET_ID = '1sRy44EPpzkcV1HUAc4x1pvM4Erp4j9nfGgHH_yUXlo8'
JFactor = 32
ELORange = "ELO!A1:C18"  # NOTE: Increment with new player
WLRange = "Primary!B3:D19"  # NOTE: Increment with new player
streakRange = "Primary!T3:W19"  # NOTE: Increment with new player
LOGRange = "WLLog!B3:D102"
PLOGRange = "WLLog_Processed!B3:C{0}"
UPLOGRange = "WLLog_Processed!B{0}:D{1}"
PLOGCount = "WLLog_Processed!H3"
vsResultRange = "WLLog_Processed!L4:AB20"  # NOTE: Increment with new player and update second letter

DEBUG = True
logCount, logActions = 0, True

streakDict = {}

nameList = ['Chris', 'Luke', 'James', 'Simone', 'Callum', 'Michael', 'Barry', 'Olly', 'Gaffer', 'Alistair', 'Tom', 'Marc', 'Katie', 'Paulina', 'Lucas', 'Lauren', 'Becca']   # NOTE: Add new player here


def calcBatchELOs(ELOs, winsLosses):

    log("Batch updating all ELOs")

    maxIndex = len(ELOs)
    tempELOList = []

    if maxIndex != len(winsLosses):
        print("Ranges are of uneven length (ELOs - winsLosses). Exiting")
        sys.exit()

    for index in range(maxIndex):

        nameMatch(index=index, first=ELOs[index][0], second=winsLosses[index][0])

        tempELOList.append([
            ELOs[index][0],
            calcSingleELO(
                ELO=ELOs[index][1],
                wins=winsLosses[index][1],
                losses=winsLosses[index][2]
            )
        ])

    return tempELOList


def calcHTHELO(ELOs, winner, loser, accumulativeDiff=False):

    log("Calculating head to head result")

    wIndex, lIndex = None, None

    for index in range(len(ELOs)):

        if not wIndex and ELOs[index][0].lower() in winner.lower():
            wIndex = index

        elif not lIndex and ELOs[index][0].lower() in loser.lower():
            lIndex = index

        if wIndex and lIndex:
            break

    if not wIndex or not lIndex:
        print("Player name not found, please try again. Exiting")
        sys.exit()

    wELO, lELO = int(ELOs[wIndex][1]), int(ELOs[lIndex][1])

    ELOs[wIndex][1], ELOs[lIndex][1] = calcVSELO(ELOs[wIndex][1], ELOs[lIndex][1])

    ELOs[wIndex][2] = int(ELOs[wIndex][2]) + ELOs[wIndex][1]-wELO if accumulativeDiff else ELOs[wIndex][1]-wELO
    ELOs[lIndex][2] = int(ELOs[lIndex][2]) + ELOs[lIndex][1]-lELO if accumulativeDiff else ELOs[lIndex][1]-lELO

    return ELOs


def calcVSELO(wELO, lELO):

    log("Processing ELO change for head to head result")

    wELO, lELO = map(int, [wELO, lELO])
    R1, R2 = rating(wELO, lELO)
    E1, E2 = expected(R1, R2)
    wELO = float(wELO + JFactor * (1 - E1))
    lELO = float(lELO + JFactor * (0 - E2))
    return round(wELO, 0), round(lELO, 0)


def calcSingleELO(ELO, wins, losses):
    """
    KFac = 32
    Rating - R1 = 10^ELO1/400
    Rating - R2 = 10^ELO2/400
    Expected Score - E1 = R1 / (R1 + R2)
    Expected Score - E2 = R2 / (R1 + R2)
    Actual Score - S1 = 1 (P1 Win) / 0.5 (Draw) / 0 (P2 Win)
    Actual Score - S2 = 0 (P1 Win) / 0.5 (Draw) / 1 (P2 Win)
    Updated ELO - uR1 = ELO1 + KFac * (S1 - E1)
    Updated ELO - uR2 = ELO2 + KFac * (S2 - E2)
    """

    log("Processing ELO change for default match up")

    ELO, wins, losses = map(int, [ELO, wins, losses])
    calcVal = wins - losses

    for i in range(calcVal if calcVal >= 0 else abs(calcVal)):
        R1, R2 = rating(ELO, 1000)
        E1, E2 = expected(R1, R2)
        ELO = float(ELO + JFactor * ((1 if calcVal >= 0 else 0) - E1))
        round(ELO, 2)

    return round(ELO, 0)


def rating(ELO1, ELO2):
    ELO1, ELO2 = float(ELO1), float(ELO2)
    return math.pow(10, ELO1/400.00), math.pow(10, ELO2/400.00)


def expected(R1, R2):
    return float(R1 / (R1 + R2)), float(R2 / (R1 + R2))


def nameMatch(index, first, second):
    """ Ensures the names are in the correct order between the ELO and Primary Sheet Tables"""

    log("Ensuring name correlation")

    if first not in second:
        print("Names within the returned ranges did not match (Index:{0} - F: {1} - S: {2}). Exiting".format(index, first, second))
        sys.exit()


def getELOs():

    log("Retrieving ELOs")

    return SAC.queryAndValidate(
        sheet=sheet,
        spreadsheetID=MAIN_SPREADSHEET_ID,
        sheetRange=ELORange
    )


def getWL():

    log("Retrieving Win Loss Table")

    return SAC.queryAndValidate(
        sheet=sheet,
        spreadsheetID=MAIN_SPREADSHEET_ID,
        sheetRange=WLRange
    )


def getLog(processed=False, newLogCount=None):

    log("Retrieving Match Logs")

    return SAC.queryAndValidate(
        sheet=sheet,
        spreadsheetID=LOG_SPREADSHEET_ID,
        sheetRange=LOGRange if not processed else PLOGRange.format(newLogCount)
    )


def getLogCount():

    log("Retrieving Processed Log Count")

    return SAC.queryAndValidate(
        sheet=sheet,
        spreadsheetID=LOG_SPREADSHEET_ID,
        sheetRange=PLOGCount
    )


def correctExpectedInt(ELOs):
    for row in ELOs[1::]:
        for i in range(1, 3):

            if isinstance(row[i], str):
                row[i] = row[i].replace('\'', '')

            row[i] = int(row[i])

    return ELOs


def updateCells(values, sheetID, sheetRange, dataType="RAW"):

    log("Updating Cells in range {}".format(sheetRange))

    SAC.sendWrite(
        sheet=sheet,
        values=values,
        spreadsheetID=sheetID,
        sheetRange=sheetRange,
        valueInputOption=dataType
    )


def findUnLoggedMatches(currentLog):

    log("Finding unprocessed matches")

    indexesToUpdate = []

    for index in range(len(currentLog)):
        if not currentLog[index][0] or not currentLog[index][1]:
            break

        if currentLog[index][2] in "FALSE":
            indexesToUpdate.append(index)

    return indexesToUpdate


def updateWinLossTable(wlTable, winner, loser):

    log("Updating Win Loss Table")

    wlTable = [
        [
            Name,
            int(Wins) + 1 if Name.lower() in winner.lower() else int(Wins),
            int(Losses) + 1 if Name.lower() in loser.lower() else int(Losses)
        ] for Name, Wins, Losses in wlTable]

    return wlTable


def genStreakDict():
    for num, player in enumerate(nameList):
        streakDict[player] = {'index': num, 'BWS': 0, 'CWS': 0, 'BLS': 0, 'CLS': 0}


def calcWLStreak(winner, loser):

    log("Calculating Win/Loss Streaks for head to head match up")

    if not streakDict:
        genStreakDict()

    streakDict[winner]['CWS'] = streakDict[winner]['CWS'] + 1

    if streakDict[winner]['CLS'] > streakDict[winner]['BLS']:
        streakDict[winner]['BLS'] = streakDict[winner]['CLS']

    streakDict[winner]['CLS'] = 0

    streakDict[loser]['CLS'] = streakDict[loser]['CLS'] + 1

    if streakDict[loser]['CWS'] > streakDict[loser]['BWS']:
        streakDict[loser]['BWS'] = streakDict[loser]['CWS']

    streakDict[loser]['CWS'] = 0


def buildStreakListForSheet():

    log("Building Streak List")

    streaks = []

    for name in nameList:
        streaks.append([
            streakDict[name]["BWS"],
            streakDict[name]["CWS"],
            streakDict[name]["BLS"],
            streakDict[name]["CLS"]
        ])

    return streaks


def debugPrint(message="DEBUG", item=None):
    if DEBUG:
        print("\n\n{0} {1} - \n{2}".format("#" * 30, message, item if item else ''))


def log(message):
    if logActions:
        global logCount
        print("\n{0} {1} - {2}".format("#" * 10, logCount, message))
        logCount += 1
