#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_core.core.context import WorkerContext
from service_winrm.constants import WINRM_CONFIG_KEY
from service_winrm.core.connect import Connection
from service_core.core.service.dependency import Dependency


class Winrm(Dependency):
    """ Winrm依赖类

    1. 主要用于Windows远程管理,基于PowerShell的PSRemoting模式工作的
    doc: https://docs.microsoft.com/en-us/windows/win32/winrm/portal
    """

    def __init__(self, alias: t.Text, protocol_options: t.Optional[t.Dict[t.Text, t.Any]] = None, **kwargs: t.Text):
        """ 初始化实例

        @param alias: 配置别名
        @param protocol_options: 协议配置
        @param kwargs: 其它配置
        """
        self.alias = alias
        self.client = None
        self.protocol_options = protocol_options or {}
        super(Winrm, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        protocol_options = self.container.config.get(f'{WINRM_CONFIG_KEY}.{self.alias}.protocol_options', default={})
        # 防止YAML中声明值为None
        self.protocol_options = (protocol_options or {}) | self.protocol_options
        self.client = Connection(**self.protocol_options)

    def get_instance(self, context: WorkerContext) -> t.Any:
        """ 获取注入对象

        @param context: 上下文对象
        @return: t.Any
        """
        return self.client
