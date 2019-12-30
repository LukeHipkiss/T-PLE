#!/sv/venv/T-PLE/bin/python2.7

from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal
from datetime import date


def main():

    hisLogCount = int(ELOCal.getHisLogCount()[0][0])
    today_date = date.today().strftime("%m/%d/%Y")

    if ELOCal.getLastLogDate(hisLogCount)[0][0] in today_date:
        ELOCal.log("HEU: Historic ELOs updated today. Exiting Historic ELO Update Call")
        return

    ELOs, historicELOs = ELOCal.getELOs(), ELOCal.getHistoricELOs(hisLogCount)

    historicLogEntry = [
        today_date
    ]

    for ELO in ELOs[1::]:
        historicLogEntry.append(ELO[1])

    historicELOs[len(historicELOs)-1] = historicLogEntry
    historicELOs.append(["=TODAY()", "=TRANSPOSE($C$3:$C$18)"])

    ELOCal.debugPrint("HEU: New Historic ELO List", historicELOs)

    ELOCal.updateCells(
        values=historicELOs,
        sheetRange=ELOCal.HIS_ELO_Range.format(str(ELOCal.HIS_LOG_OFFSET + len(historicELOs))),
        dataType="USER_ENTERED"
    )

    ELOCal.log("HEU: Historic ELOs Logged")


if __name__ == '__main__':
    main()
