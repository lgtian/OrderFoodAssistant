# 工具类


# 判断字符串是否为空
def is_str_empty(string):
    return string is None or len(str(string).strip()) == 0