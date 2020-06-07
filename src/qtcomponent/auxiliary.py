# _*_ coding:utf-8 _*_
from functools import singledispatch


@singledispatch
def parse_pix_width(arg):
    """

    :rtype: int
    """
    pass


@parse_pix_width.register(str)
def pix_width(arg):
    result = 0
    str_list = arg.upper().split("PX")
    if len(str_list) > 0 and str_list[0].isdigit():
        result = abs(int(str_list[0]))
    return result


@parse_pix_width.register(int)
def pix_width(arg):
    return abs(arg)
