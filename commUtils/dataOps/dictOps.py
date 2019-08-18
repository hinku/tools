'''
Created on 2019年4月13日

@author: Administrator
'''

from .updateOps import UpdateOps


def trans_from_list(src, key=None):
    if not src or not isinstance(src, list) or not isinstance(src[0], list):
        raise TypeError('src is not a double list')

    col_names = src.value[0]
    print(col_names)

    if key:
        key_indexs = [i for i, v in enumerate(col_names) if v == key]
        if not key_indexs:
            print('has no col Named: %s' % key)
            return None
        key_index = key_indexs[0]

    data_dict = {}
    max_key = None
    for i, data in enumerate(src.value[1:]):
        row = {col_names[i]: v for i, v in enumerate(data)}
        if key:
            cur_key = data[key_index]
        else:
            cur_key = i + 1

        data_dict[cur_key] = row
        # 记录最大的key值
        if not max_key or cur_key > max_key:
            max_key = cur_key

    # print(data_dict)
    return data_dict, max_key


def update(dst, src, ops=UpdateOps.whileEmpty):
    """
    对两条单条记录的的数据字典进行更新操作，ops
    :param dst:
    :param src:
    :param ops:
    :return:
    """
    x = dst.copy()
    for key in x.keys():
        # 只有源数据为空时才覆盖
        if ops == UpdateOps.whileEmpty:
            dst_v = x.get(key)
            if not dst_v or not str(dst_v).strip():
                x[key] = src.get(key)
        # 覆盖时，要先判断新数据是否有key，如果没有，则不需要覆盖
        elif ops == UpdateOps.override and key in src:
            x[key] = src.get(key)
        else:
            pass

    return x


def appendNotExistKeys(dst, src):
    x = {k: v for k, v in src.items() if k not in dst}
    return {**dst, **x}


def merge(dst, src, ops=UpdateOps.whileEmpty, joinFlag=False):
    # 合并时覆盖且需要连接，直接使用dict update方法
    if ops == UpdateOps.override and joinFlag:
        return {**dst, **src}

    x = update(dst, src, ops)
    if joinFlag:
        # 以 | 保证orig的优先顺序，保证updateOps可信
        x = appendNotExistKeys(x, src)

    return x


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
