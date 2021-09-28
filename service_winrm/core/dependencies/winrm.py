#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_winrm.core.client import WinrmClient
from service_winrm.constants import WINRM_CONFIG_KEY
from service_core.core.service.dependency import Dependency


class Winrm(Dependency):
    """ Winrm依赖类

    1. 主要用于Windows远程管理,基于PowerShell的PSRemoting模式工作的
    doc: https://docs.microsoft.com/en-us/windows/win32/winrm/portal
    """

    def __init__(self, alias: t.Text, connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None, **kwargs: t.Any):
        """ 初始化实例

        @param alias: 配置别名
        @param connect_options: 连接配置
        @param kwargs: 其它配置
        """
        self.alias = alias
        self.client = None
        self.connect_options = connect_options or {}
        super(Winrm, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        connect_options = self.container.config.get(f'{WINRM_CONFIG_KEY}.{self.alias}.connect_options', default={})
        # 防止YAML中声明值为None
        self.connect_options = (connect_options or {}) | self.connect_options
        # 设置默认的读写的超时时间
        self.connect_options.setdefault('read_timeout_sec', 15)
        self.connect_options.setdefault('operation_timeout_sec', 10)

    def get_client(self) -> WinrmClient:
        """ 获取一个独立的会话

        @return: WinrmClient
        """
        return WinrmClient(**self.connect_options)
