# -*- coding: UTF-8 -*-
"""ShadowGrid-Next 模块系统 API"""

import abc
from typing import Dict, List, Optional


class ModuleBase(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def description(self):
        pass

    @property
    @abc.abstractmethod
    def author(self):
        pass

    @property
    @abc.abstractmethod
    def version(self):
        pass

    @abc.abstractmethod
    def handle(self, cmd):
        pass

    @abc.abstractmethod
    def get_commands(self):
        pass

    def get_help(self):
        return self.description


class ModuleRegistry:
    def __init__(self):
        self._modules = {}

    def register(self, module):
        for cmd in module.get_commands():
            self._modules[cmd] = module

    def get_module(self, command):
        return self._modules.get(command)

    def get_all_modules(self):
        return dict(self._modules)


registry = ModuleRegistry()


def load_modules_from_dir(modules_dir, enabled_list=None):
    import os
    import sys
    import importlib.util

    if not os.path.exists(modules_dir):
        return {}

    modules = {}
    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            
            if enabled_list is not None and module_name not in enabled_list:
                continue

            try:
                module_path = os.path.join(modules_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                if hasattr(module, 'module') and isinstance(module.module, ModuleBase):
                    for cmd in module.module.get_commands():
                        registry.register(module.module)
                    modules[module_name] = module.module
            except Exception:
                pass

    return modules


def handle_module_command(cmd):
    if not cmd:
        return {"status": "error", "result": "Empty command", "result_type": "error"}

    command_type = cmd.get("type")
    if not command_type:
        return {"status": "error", "result": "Missing command type", "result_type": "error"}

    module = registry.get_module(command_type)
    if module:
        return module.handle(cmd)

    return {"status": "error", "result": f"Unknown command: {command_type}", "result_type": "error"}
