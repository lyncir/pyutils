# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2019-07-12 11:25:01 (+0800)
    :last modified date: 2019-07-13 15:56:41 (+0800)
    :last modified by: lyncir
"""
import grapheme


def test_width_chars():
    """
    测试字符的元素
    """
    chars = {
        # 泰语
        'ผ': 1,
        'ผู': 1, 
        'ผู้': 1,
        # 中文
        '国': 1,
        '國': 1,
        # 日语
        'ｱ': 1,
        'あ': 1,
        # 韩语
        '한': 1,
        '헤': 1,
        '후': 1,
        '훼': 1,
        # 越南
        'ế': 1,
        # Emoji
        "🏳️‍🌈": 1,
    }

    for char, length in chars.items():
        assert length == grapheme.length(char)

