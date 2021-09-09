#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_winrm.core.proxy import WinrmProxy
from service_core.cli.subctxs import BaseContext
from service_core.core.configure import Configure


class Winrm(BaseContext):
    """ 用于调试Winrm接口 """

    name: t.Text = 'winrm'

    def __init__(self, config: Configure) -> None:
        """ 初始化实例

        @param config: 配置对象
        """
        super(Winrm, self).__init__(config)
        self.proxy = WinrmProxy(config=config)
