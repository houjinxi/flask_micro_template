# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 10:46
# @Author  : HoxHou
# @File    : params_type.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
import inspect
from functools import wraps
from app.utils.data_handler import DataChecker


def type_interceptor():
    """
    参数类型拦截器
    :return:
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            checker = DataChecker()
            if len(args) > 0 and checker.option(kwargs).is_empty:
                return func(*args, **kwargs)
            arg_spec = inspect.getfullargspec(func)
            params_defaults = None
            params_value = None

            if arg_spec.defaults:  # 函数缺省值判断
                params_defaults = dict(
                    zip(arg_spec.args[-len(arg_spec.defaults):], arg_spec.defaults)
                )
                for k, v in params_defaults.items():
                    arg_index = arg_spec.args.index(k)
                    err_msg = f"参数缺省值类型为 {type(v)} "
                    if v is None:  # 缺省值为None时，不校验
                        continue
                    try:
                        assert isinstance(args[arg_index], type(v)), err_msg
                    except IndexError:
                        pass

            for key in arg_spec.annotations:
                # 只处理参数的类型注解，忽略返回值
                if key == "return":
                    continue
                arg_index = arg_spec.args.index(key)
                try:
                    params_value = args[arg_index]
                except IndexError:
                    try:  # 当参数以具名方式传入时, 会被放置在kwargs 此时从args中取值会出现IndexError
                        params_value = kwargs[key]
                    except KeyError:  # 处理当指定参数限定了参数类型同时具有默认值的情况
                        if params_defaults and key in params_defaults:
                            params_value = params_defaults[key]
                            if params_value is None:
                                continue
                try:  # 参数为单个数据类型
                    err_msg = f"函数 {func.__name__} 的参数 {key} 必须是 {arg_spec.annotations[key]} 类型"
                    assert isinstance(params_value, arg_spec.annotations[key]), err_msg
                except TypeError:  # 参数可能为多种数据类型
                    if len(arg_spec.annotations[key].__args__) > 1:
                        type_msg = "或者".join(
                            [str(a) for a in arg_spec.annotations[key].__args__]
                        )
                        err_msg = f"函数 {func.__name__} 的参数 {key} 必须是 {type_msg} 类型"
                        assert isinstance(
                            params_value, arg_spec.annotations[key].__args__
                        ), err_msg
            return func(*args, **kwargs)

        return inner

    return wrapper
