from commUtils.webutils import WebBrowser
from commUtils.webutils import IWeb
from commUtils.webutils import WebRequest
from commUtils.webutils import WebContent
from commUtils import webutils
from commUtils.dataOps.updateOps import UpdateOps
from commUtils.dataOps.dictOps import merge
if __name__ == '__main__':
    # 输出结果分别为
    # ===============================================================================
    #     {'a': 1, 'b': 2}
    #     {'a': 1, 'b': 2, 'c': 4}
    #     {'a': 1, 'b': 3}
    #     {'a': 1, 'b': 3, 'c': 4}
    # ===============================================================================

    x = {'a': 1, 'b': 2, 'c': None}
    y = {'b': 3, 'c': 4}

    z = merge(x, y, ops=UpdateOps.whileEmpty, joinFlag=False)
    print(z)
    z = merge(x, y, ops=UpdateOps.whileEmpty, joinFlag=True)
    print(z)
    z = merge(x, y, ops=UpdateOps.override, joinFlag=False)
    print(z)
    z = merge(x, y, ops=UpdateOps.override, joinFlag=True)
    print(z)

    # ===========================================================================
    # {'a': 1, 'b': 3, 'c': 4}
    # {'a': 1, 'b': 2, 'c': 'c'}
    # {'a': 1, 'b': 2, 'c': 'c', 4: 4}
    # {'a': 1, 'b': 2, 'c': 'd'}
    # {'a': 1, 'b': 2, 'c': 'd', 4: 4}
    # ===========================================================================
    k = {'a': None, 'b': '', 'c': 'c'}
    l = {'a': 1, 'b': 2, 'c': 'd', 4: 4}
    z = merge(k, l, ops=UpdateOps.whileEmpty, joinFlag=False)
    print(z)
    z = merge(k, l, ops=UpdateOps.whileEmpty, joinFlag=True)
    print(z)
    z = merge(k, l, ops=UpdateOps.override, joinFlag=False)
    print(z)
    z = merge(k, l, ops=UpdateOps.override, joinFlag=True)
    print(z)

    pass
