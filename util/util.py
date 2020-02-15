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

    return res


def get_week_day(date):
    """
    判断星期几

    :param date:
    :return:
    """
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]
