# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U service-winrm 
```

# 服务配置

> config.yaml

```yaml
CONTEXT:
  - service_winrm.cli.subctxs.winrm:Winrm
WINRM:
  test:
    connect_options:
      transport: ntlm
      endpoint: http://127.0.0.1:5985/wsman
      username: cn\test
      password: test
```

# 入门案例

```yaml
├── config.yaml
├── facade.py
└── project
    ├── __init__.py
    └── service.py
```

> service.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from passlib.hash import nthash
from service_winrm.core.dependencies import Winrm
from service_croniter.core.entrypoints import croniter
from service_core.core.service import Service as BaseService

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    # 微服务名称
    name = 'demo'
    # 微服务简介
    desc = 'demo'

    # 远程PS管理
    winrm: Winrm = Winrm(alias='test')

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        # 此服务无需启动监听端口, 请初始化掉下面参数
        self.host = ''
        self.port = 0
        super(Service, self).__init__(*args, **kwargs)

    @croniter.cron('* * * * * */1')
    def test_winrm_whoami_with_cmd(self, *args, **kwargs) -> None:
        """ 测试执行cmd命令

        doc: https://docs.microsoft.com/en-us/windows/win32/winrm/portal
        @return: None
        """
        cmd = 'whoami'
        result = self.winrm.get_client().run_cmd(cmd)
        logger.debug(f'yeah~ yeah~ yeah~, cmd code={result.status_code} out={result.std_out} err={result.std_err}')

    @croniter.cron('* * * * * */1')
    def test_winrm_set_sam_account_password_hash_with_powershell(self, *args, **kwargs) -> None:
        """ 测试执行powershell脚本

        doc: https://docs.microsoft.com/en-us/windows/win32/winrm/portal
        @return: None
        """
        addomain = 'cn'
        adserver = '127.0.0.1'
        username = 'test'
        password = nthash.hash('test')
        ps = f'''
        Import-Module ActiveDirectory
        Import-Module C:\DSInternals
        Set-SamAccountPasswordHash -SamAccountName {username} -Domain {addomain} -NTHash {password} -Server {adserver}
        '''
        result = self.winrm.get_client().run_ps(ps)
        logger.debug(f'yeah~ yeah~ yeah~, ps code={result.status_code} out={result.std_out} err={result.std_err}')
```

> facade.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project import Service

service = Service()
```

# 运行服务

> core start facade --debug

# 接口调试

> core shell --shell `shell`

```shell
* eventlet 0.31.1
    - platform: macOS 10.15.7
      error  : changelist must be an iterable of select.kevent objects
      issue  : https://github.com/eventlet/eventlet/issues/670#issuecomment-735488189
    - platform: macOS 10.15.7
      error  : monkey_patch causes issues with dns .local #694
      issue  : https://github.com/eventlet/eventlet/issues/694#issuecomment-806100692

2021-09-10 10:19:21,051 - 193432 - DEBUG - load subcmd service_core.cli.subcmds.debug:Debug succ
2021-09-10 10:19:21,053 - 193432 - DEBUG - load subcmd service_core.cli.subcmds.config:Config succ
2021-09-10 10:19:21,053 - 193432 - DEBUG - load subcmd service_core.cli.subcmds.shell:Shell succ
2021-09-10 10:19:21,053 - 193432 - DEBUG - load subcmd service_core.cli.subcmds.start:Start succ
2021-09-10 10:19:21,331 - 193432 - DEBUG - load subctx service_winrm.cli.subctxs.winrm:Winrm succ
2021-09-10 10:19:21,331 - 193432 - DEBUG - load subctx service_core.cli.subctxs.config:Config succ
CPython - 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)]
>>> s.winrm.proxy(alias='test').run_ps('whoami')
<Response code 0, out "b'cn\\wbchange\r\n'", err "b''">
```

# 运行调试

> core debug --port `port`
