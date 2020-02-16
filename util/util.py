# 工具类


def is_str_empty(string):
    """判断字符串是否为空"""
    return string is None or len(str(string).strip()) == 0


def join_dict_elems(elem_dict, key_val_separator, elem_separator):
    """
    拼接

    :param dict:
    :param key_val_separator:
    :param elem_separator:
    :return:
    """
    res = ''
    for key, val in elem_dict.items():
        res = res + elem_separator + (str(key) + key_val_separator + str(val))

    return res[1:len(res)]


def get_week_day(date):
    """
    判断周几

    :param date:
    :return:
    """
    week_day_dict = {
        0: '周一',
        1: '周二',
        2: '周三',
        3: '周四',
        4: '周五',
        5: '周六',
        6: '周日',
    }
    day = date.weekday()
    return week_day_dict[day]
