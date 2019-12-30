from __future__ import print_function
from scripts.baseController import baseELOCalculations as ELOCal


def main():
    ELOs, winsLosses = ELOCal.getELOs(), ELOCal.getWL()

    batchUpdatedELOS = ELOCal.calcBatchELOs(ELOs, winsLosses)

    ELOCal.updateCells(
        values=batchUpdatedELOS,
        sheetRange=ELOCal.ELO_Range
    )


if __name__ == '__main__':
    main()
