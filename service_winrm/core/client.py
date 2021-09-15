#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from winrm import Session


class WinrmClient(Session):
    """ Winrm通用连接类 """

    def __init__(self, endpoint: t.Text, username: t.Text, password: t.Text, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param endpoint: 入口地址
        @param username: 认证用户
        @param password: 认证密码
        @param kwargs: 其它选项
        """
        super(WinrmClient, self).__init__(target=endpoint, auth=(username, password), **kwargs)
