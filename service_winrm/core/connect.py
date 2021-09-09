#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from winrm import Session


class Connection(Session):
    """ Winrm通用连接 """

    def __init__(self, endpoint: t.Text, username: t.Text, password: t.Text, **kwargs: t.Dict[t.Text, t.Any]) -> None:
        """ 初始化实例

        @param endpoint: 入口地址
        @param username: 认证账户
        @param password: 认证密码
        @param kwargs: 其它参数
        """
        super(Connection, self).__init__(target=endpoint, auth=(username, password), **kwargs)
