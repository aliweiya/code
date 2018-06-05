from .config import AppConfig
from .registry import apps

# Python 没有语言原生的可见性控制，而是靠一套需要大家自觉遵守的”约定“下工作。比如下划线开头的应该对外部不可见
# __all__ 提供了暴露接口用的”白名单“。
# 一些不以下划线开头的变量（比如从其他地方 import 到当前模块的成员）可以同样被排除出去。
# import * 就只会导入 __all__ 列出的成员。
__all__ = ['AppConfig', 'apps']
