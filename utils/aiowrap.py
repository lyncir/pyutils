# -*- coding: utf-8 -*-
"""
    uitls.aiowrap
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-10 15:33:28 (+0800)
    :last modified date: 2018-12-15 22:42:02 (+0800)
    :last modified by: lyncir
"""
import os
import asyncio
import inspect
from functools import wraps, partial


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


class Wrapper:
    pass


def aiowrap(obj):
    if callable(obj):
        return wrap(obj)
    elif inspect.ismodule(obj) or inspect.isclass(obj):
        wrapped_obj = Wrapper()
        if getattr(obj, '__all__'):
            attrnames = obj.__all__
        else:
            attrnames = dir(obj)
        for attrname in attrnames:
            if attrname.startswith('__'):
                continue
            original_obj = getattr(obj, attrname)
            setattr(wrapped_obj, attrname, aiowrap(original_obj))
        return wrapped_obj
    else:
        return obj


"""
把os加入异步。支持的操作有:

* os.stat
* os.close
* os.fstat
* os.read
* os.write
* os.unlink
* os.listdir
* os.path.exists
* os.rmdir
"""
aios = aiowrap(os)


if __name__ == '__main__':

    async def foo():
        print(await aios.path.exists('/'))

    asyncio.run(foo())
