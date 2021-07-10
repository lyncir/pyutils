# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2021-07-08 13:55:29 (+0800)
"""
import asyncio
import time


class Timer(object):
    """
    计时器
    """

    def __init__(self, timeout, callback):
        # 倒计时时间
        self.timeout = timeout
        # 回调函数
        self.callback = callback

        # 倒计时开始时间
        self.start_time = None
        # 暂停时间
        self.pause_time = None

    async def job(self):
        """
        异步执行任务

        1. 开始倒计时
        2. 倒计时结束执行回调
        """
        await asyncio.sleep(self.timeout)
        await self.callback()

    def start(self):
        """
        开始
        """
        # 记录开始时间
        self.start_time = time.time()
        # 开始进行倒计时
        self.task = asyncio.create_task(self.job())

    def cancel(self):
        """
        取消
        """
        self.task.cancel()

    def pause(self):
        """
        暂停
        """
        # 记录暂停时间
        self.pause_time = time.time()
        # 取消任务
        self.cancel()
        return self.get_remaining_time()

    def resume(self):
        """
        从暂停中恢复
        """
        self.timeout = self.get_remaining_time()
        # 清除暂停时间
        self.pause_time = None
        # 继续开始
        self.start()

    def get_remaining_time(self):
        """
        获取剩余时间
        """
        # 未开始
        if self.start_time is None:
            return self.timeout

        else:

            # 计时中
            if self.pause_time is None:
                return self.timeout - (time.time() - self.start_time)

            # 暂停中
            else:
                return self.timeout - (self.pause_time - self.start_time)
