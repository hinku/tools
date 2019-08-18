from commUtils.dataOps.excelOps import ExcelOps
if __name__ == '__main__':
    xls = ExcelOps('test.xlsx', sheetNameOrIndex=0, keyName='a')
    print(xls.dataDict)

    xls = ExcelOps('test.xlsx', sheetNameOrIndex=0, keyName=None)
    print(xls.dataDict)